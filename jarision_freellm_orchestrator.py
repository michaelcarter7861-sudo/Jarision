import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

# ==============================================================================
# 100% DEDICATED TASHFEENAHMED/FREELLMAPI ENDPOINT (PORT 3001)
# All model routing, quota tracking, and 34-provider failover is handled by FreeLLMAPI!
# ==============================================================================
FREELLM_API_BASE = os.environ.get("FREELLM_API_BASE", "http://localhost:3001/v1")
FREELLM_CHAT_URL = f"{FREELLM_API_BASE}/chat/completions"
FREELLM_MASTER_KEY = os.environ.get("FREELLM_MASTER_KEY", "freellmapi-jarision-master-key")

BACKLOG_FILE = "spark_backlog.json"
SCRIPTS_DIR = "Assets/Scripts"
SKILLS_DIR = ".agent/skills"
RULES_DIR = ".agent/rules"
IGI_ECOSYSTEM_DIR = "reference/igi-ecosystem"

SYSTEM_PROMPT = """You are the Autonomous Multi-Agent Game Studio (CrewAI + Aider + Unity-Technologies/skills + obra/superpowers) powered by tashfeenahmed/freellmapi.
You are building 'Jarision', a 500MB-800MB Heavy Project I.G.I. Tactical Stealth FPS with 14 Mega-Missions.
Strictly obey:
1. All loaded SKILL.md playbooks (Unity-Technologies/skills, obra/superpowers, addyosmani/agent-skills, Common-ka/ai-agent-unity-rules).
2. All reference schemas from heaven-hm/project-igi-toolkit, project-igi-editor, project-igi-internals-data, and project-igi-research.
3. Zero-GC Unity C# rules inside namespace 'TacticalStealthCore'.
Return ONLY valid JSON with this exact structure:
{
  "architectPlan": "step-by-step plan following obra/superpowers writing-plans skill",
  "mainFileContent": "complete production-ready C#, Blender Python, JSON blueprint, or Markdown content",
  "testFileContent": "complete NUnit test script string (or empty string if not applicable)",
  "qaReviewNotes": "verification notes from addyosmani/agent-skills code review",
  "commitSummary": "concise 1-line git commit summary"
}"""

def wait_for_freellmapi_health(timeout_sec=90):
    """Waits for the tashfeenahmed/freellmapi service on localhost:3001 to be ready."""
    models_url = f"{FREELLM_API_BASE}/models"
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            req = urllib.request.Request(
                models_url,
                headers={"Authorization": f"Bearer {FREELLM_MASTER_KEY}"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    print("[FREELLMAPI] Router is ONLINE at http://localhost:3001/v1 (34-Provider Failover Active).")
                    return True
        except Exception:
            time.sleep(2)
    print("[WARN] FreeLLMAPI /models health check timed out; proceeding directly to /chat/completions...")
    return False

def gather_all_repositories_context():
    """Aggregates context from all synced Skills, Unity Rules, IGI Toolkit repos, and existing C# scripts."""
    chunks = []

    # 1. Load Skills & Rules (Unity-Technologies/skills, obra/superpowers, addyosmani/agent-skills, Common-ka)
    for folder in [SKILLS_DIR, RULES_DIR]:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.endswith((".md", ".mdc", ".txt")):
                        p = os.path.join(root, f)
                        try:
                            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                                chunks.append(f"--- SKILL/RULE ({p}) ---\n" + fp.read()[:1200])
                        except Exception:
                            pass

    # 2. Load heaven-hm IGI Ecosystem (toolkit, editor, internals-data, research)
    if os.path.exists(IGI_ECOSYSTEM_DIR):
        igi_summary = []
        for root, _, files in os.walk(IGI_ECOSYSTEM_DIR):
            for f in files:
                if f.endswith((".cs", ".json", ".qsc", ".md")):
                    p = os.path.join(root, f)
                    igi_summary.append(p)
        chunks.append(
            f"--- IGI ECOSYSTEM REPOSITORIES LOADED ({len(igi_summary)} files) ---\n"
            + "\n".join(igi_summary[:60])
        )

    # 3. Load existing Unity C# signatures
    if os.path.exists(SCRIPTS_DIR):
        pattern = re.compile(r"^\s*(public|internal)\s+(class|struct|enum|interface|void|bool|int|float|Vector3|GuardState|SurfaceType)\s+.*$", re.MULTILINE)
        for root, _, files in os.walk(SCRIPTS_DIR):
            for f in files:
                if f.endswith(".cs"):
                    p = os.path.join(root, f)
                    try:
                        with open(p, "r", encoding="utf-8") as fp:
                            matches = [m.group(0).strip() for m in pattern.finditer(fp.read())]
                        if matches:
                            chunks.append(f"// Existing C#: {p}\n" + "\n".join(matches[:35]))
                    except Exception:
                        pass

    return "\n\n".join(chunks[:25])

def call_freellmapi(task_prompt, repo_context, is_csharp=False):
    """Sends the request strictly through tashfeenahmed/freellmapi on localhost:3001/v1."""
    full_user_prompt = (
        f"=== LOADED REPOSITORIES, SKILLS & IGI TOOLKIT CONTEXT ===\n{repo_context}\n\n"
        f"=== TASK TO EXECUTE ===\n{task_prompt}"
    )

    # FreeLLMAPI smart routing tags: auto:smart -> auto:fast -> auto
    for routing_profile in ["auto:smart", "auto:fast", "auto"]:
        payload = {
            "model": routing_profile,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": full_user_prompt}
            ],
            "temperature": 0.15,
            "response_format": {"type": "json_object"}
        }
        req = urllib.request.Request(
            FREELLM_CHAT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {FREELLM_MASTER_KEY}"
            },
            method="POST"
        )
        try:
            print(f"[FREELLMAPI] Dispatching request to {FREELLM_CHAT_URL} (profile: {routing_profile})...")
            with urllib.request.urlopen(req, timeout=240) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                if is_csharp:
                    code = parsed.get("mainFileContent", "")
                    if not code.strip() or code.count("{") != code.count("}"):
                        raise ValueError("Generated C# failed brace balance verification.")
                return parsed
        except Exception as err:
            print(f"[FREELLMAPI] Profile '{routing_profile}' reported: {err}. Retrying next FreeLLMAPI profile...")
            time.sleep(3)

    raise RuntimeError("tashfeenahmed/freellmapi could not complete the request. Verify FREEAPI_CONFIG_JSON in GitHub Secrets.")

def write_output_file(filepath, content):
    if not filepath or not content:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[STUDIO] Wrote file: {filepath}")

def main():
    wait_for_freellmapi_health()

    with open(BACKLOG_FILE, "r", encoding="utf-8") as f:
        backlog = json.load(f)

    batch_size = int(os.environ.get("SPARK_BATCH_SIZE", "2"))
    pending_tasks = [t for t in backlog["tasks"] if t["status"] == "pending"]

    if not pending_tasks:
        print("[STUDIO] All 24 tasks (Core Systems + 3D Assets + All 14 I.G.I. Missions) are 100% COMPLETED!")
        sys.exit(0)

    for task in pending_tasks[:batch_size]:
        print(f"\n=======================================================")
        print(f"⚡ EXECUTING {task['id']} -> {task['outputPath']}")
        print(f"=======================================================")
        repo_context = gather_all_repositories_context()
        is_cs = task["outputPath"].endswith(".cs")

        result = call_freellmapi(task["prompt"], repo_context, is_csharp=is_cs)

        write_output_file(task["outputPath"], result.get("mainFileContent", ""))
        if task.get("testPath"):
            write_output_file(task["testPath"], result.get("testFileContent", ""))

        # Run Headless Blender if a 3D generator script was created
        if task["outputPath"].startswith("tools/blender/") and task["outputPath"].endswith(".py"):
            print(f"[BLENDER-3D] Executing headless Blender on {task['outputPath']}...")
            subprocess.run(["blender", "--background", "--python", task["outputPath"]], check=False)

        task["status"] = "completed"
        with open(BACKLOG_FILE, "w", encoding="utf-8") as f:
            json.dump(backlog, f, indent=2)

        print(f"[STUDIO] Completed {task['id']}: {result.get('commitSummary', 'Success')}")
        time.sleep(3)

if __name__ == "__main__":
    main()
