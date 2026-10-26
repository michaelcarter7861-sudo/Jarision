import json
import os
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.error

RAW_CONFIG = os.environ.get("FREEAPI_CONFIG_JSON", "").strip()
PORT = int(os.environ.get("PORT", "3001"))

# Provider Endpoint Registry (OpenAI-Compatible & Native Endpoints)
PROVIDER_ENDPOINTS = {
    "groq": ("https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile"),
    "mistral": ("https://api.mistral.ai/v1/chat/completions", "codestral-latest"),
    "cerebras": ("https://api.cerebras.ai/v1/chat/completions", "llama-3.3-70b"),
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "meta-llama/llama-3.3-70b-instruct:free"),
    "sambanova": ("https://api.sambanova.ai/v1/chat/completions", "Meta-Llama-3.3-70B-Instruct"),
    "github_models": ("https://models.inference.ai.azure.com/chat/completions", "gpt-4o"),
    "nvidia_nim": ("https://integrate.api.nvidia.com/v1/chat/completions", "meta/llama-3.3-70b-instruct"),
    "siliconflow": ("https://api.siliconflow.cn/v1/chat/completions", "Qwen/Qwen2.5-72B-Instruct"),
    "hyperbolic": ("https://api.hyperbolic.xyz/v1/chat/completions", "meta-llama/Llama-3.3-70B-Instruct"),
    "fireworks": ("https://api.fireworks.ai/inference/v1/chat/completions", "accounts/fireworks/models/llama-v3p3-70b-instruct"),
    "together": ("https://api.together.xyz/v1/chat/completions", "meta-llama/Llama-3.3-70B-Instruct-Turbo"),
    "deepinfra": ("https://api.deepinfra.com/v1/openai/chat/completions", "meta-llama/Llama-3.3-70B-Instruct"),
    "novita": ("https://api.novita.ai/v3/openai/chat/completions", "meta-llama/llama-3.3-70b-instruct"),
    "scaleway": ("https://api.scaleway.ai/v1/chat/completions", "llama-3.3-70b-instruct"),
    "upstage": ("https://api.upstage.ai/v1/solar/chat/completions", "solar-pro"),
    "glhf": ("https://glhf.chat/api/openai/v1/chat/completions", "hf:meta-llama/Llama-3.3-70B-Instruct"),
    "kluster": ("https://api.kluster.ai/v1/chat/completions", "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo"),
    "nebius": ("https://api.studio.nebius.ai/v1/chat/completions", "meta-llama/Llama-3.3-70B-Instruct"),
    "featherless": ("https://api.featherless.ai/v1/chat/completions", "meta-llama/Llama-3.3-70B-Instruct"),
    "arliai": ("https://api.arliai.com/v1/chat/completions", "Mistral-Nemo-12B-Instruct-2407"),
    "zhipu_glm": ("https://open.bigmodel.cn/api/paas/v4/chat/completions", "glm-4-flash"),
    "moonshot": ("https://api.moonshot.cn/v1/chat/completions", "moonshot-v1-8k"),
    "chutes": ("https://llm.chutes.ai/v1/chat/completions", "deepseek-ai/DeepSeek-V3")
}

def sanitize_and_parse_json(raw_str):
    """Automatically fixes trailing commas or minor syntax edits when user deletes providers."""
    if not raw_str:
        return {"providers": {}}
    # Remove trailing commas before } or ]
    cleaned = re.sub(r",\s*([}\]])", r"\1", raw_str)
    try:
        return json.loads(cleaned)
    except Exception as e:
        print(f"[JSON-HEALER] Warning: Standard parse failed ({e}). Attempting key extraction...")
        providers = {}
        pattern = re.compile(r'"([a-zA-Z0-9_]+)"\s*:\s*\{[^}]*?"apiKeys"\s*:\s*\[\s*"([^"]+)"', re.DOTALL)
        for match in pattern.finditer(raw_str):
            p_name, p_key = match.group(1), match.group(2)
            providers[p_name] = {"enabled": True, "apiKeys": [p_key]}
        return {"providers": providers}

CONFIG = sanitize_and_parse_json(RAW_CONFIG)

def get_active_keys():
    active = []
    providers = CONFIG.get("providers", {})
    for p_name, p_data in providers.items():
        if not isinstance(p_data, dict) or not p_data.get("enabled", True):
            continue
        keys = p_data.get("apiKeys", [])
        for k in keys:
            if k and not k.startswith("YAHAN_") and not k.startswith("PASTE_"):
                active.append((p_name.lower(), k.strip()))
    # Also inject built-in GITHUB_TOKEN if available
    gh_tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if gh_tok:
        active.append(("github_models", gh_tok))
    return active

ACTIVE_POOL = get_active_keys()
print(f"[FREELLMAPI-ROUTER] Loaded {len(ACTIVE_POOL)} active API keys across providers: {[p[0] for p in ACTIVE_POOL]}")

# Save cleaned config for tashfeenahmed/freellmapi repo
os.makedirs("config/freellmapi", exist_ok=True)
with open("config/freellmapi/runtime_config.json", "w", encoding="utf-8") as f:
    json.dump(CONFIG, f, indent=2)

def call_google_gemini(api_key, messages):
    system_text = ""
    user_text = ""
    for m in messages:
        if m.get("role") == "system":
            system_text += m.get("content", "") + "\n"
        else:
            user_text += m.get("content", "") + "\n"

    for model in ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": system_text}]},
            "contents": [{"parts": [{"text": user_text}]}],
            "generationConfig": {"temperature": 0.15, "responseMimeType": "application/json"}
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text, f"google_ai_studio/{model}"
        except Exception as e:
            print(f"[FAILOVER] Google {model} skipped: {e}")
    raise RuntimeError("All Google AI Studio models exhausted for this key.")

def call_cohere(api_key, messages):
    url = "https://api.cohere.com/v2/chat"
    payload = {
        "model": "command-r-plus-08-2024",
        "messages": messages,
        "temperature": 0.15,
        "response_format": {"type": "json_object"}
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["message"]["content"][0]["text"], "cohere/command-r-plus"

def call_openai_provider(provider_name, api_key, messages):
    if provider_name not in PROVIDER_ENDPOINTS:
        raise ValueError(f"Provider {provider_name} not in OpenAI endpoint map.")
    url, default_model = PROVIDER_ENDPOINTS[provider_name]
    payload = {
        "model": default_model,
        "messages": messages,
        "temperature": 0.15,
        "response_format": {"type": "json_object"}
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/michaelcarter7861-sudo/Jarision",
            "User-Agent": "FreeLLMAPI-Jarision/1.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"], f"{provider_name}/{default_model}"

class FreeLLMAPIGatewayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/v1/models") or self.path.startswith("/health"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "active_keys": len(ACTIVE_POOL)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        messages = body.get("messages", [])

        for provider_name, api_key in ACTIVE_POOL:
            try:
                print(f"[FREELLMAPI] Trying provider: {provider_name}...")
                if provider_name in ("google_ai_studio", "gemini", "google"):
                    reply_text, used_model = call_google_gemini(api_key, messages)
                elif provider_name == "cohere":
                    reply_text, used_model = call_cohere(api_key, messages)
                else:
                    reply_text, used_model = call_openai_provider(provider_name, api_key, messages)

                print(f"[FREELLMAPI] SUCCESS via {used_model}!")
                response_payload = {
                    "id": "freellmapi-chatcmpl",
                    "object": "chat.completion",
                    "model": used_model,
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": reply_text}}]
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))
                return
            except Exception as err:
                print(f"[FREELLMAPI-FAILOVER] {provider_name} failed ({err}) -> switching to next provider immediately!")

        self.send_response(502)
        self.end_headers()
        self.wfile.write(b'{"error": "All configured providers exhausted"}')

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), FreeLLMAPIGatewayHandler)
    print(f"[FREELLMAPI] Unified /v1 Failover Server listening on http://localhost:{PORT}/v1")
    server.serve_forever()
