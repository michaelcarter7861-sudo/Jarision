using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

namespace TacticalStealthCore
{
    public class OutsideHandlerAndBaseIntelSystem : MonoBehaviour
    {
        public GameObject radioCommsBox;
        public AudioClip[] voiceClips;
        public Text satelliteWarningsText;
        public Button jammerButton;
        public GameObject greenScreenTerminal;
        public GameObject officerClipboard;
        
        private Queue<AudioClip> voiceClipQueue = new Queue<AudioClip>();
        private bool isJammerActive = false;
        private float jammerDuration = 15f;
        private float jammerTimer = 0f;
        
        void Start()
        {
            // Initialize radio comms box
            radioCommsBox.SetActive(true);
            
            // Initialize jammer button
            jammerButton.onClick.AddListener(ActivateJammer);
            
            // Initialize green screen terminal and officer clipboard
            greenScreenTerminal.SetActive(false);
            officerClipboard.SetActive(false);
        }
        
        void Update()
        {
            // Handle voice clip queue
            if (voiceClipQueue.Count > 0 && !AudioSource.isPlaying)
            {
                AudioSource.PlayClipAtPoint(voiceClipQueue.Dequeue(), transform.position);
            }
            
            // Handle jammer timer
            if (isJammerActive)
            {
                jammerTimer -= Time.deltaTime;
                if (jammerTimer <= 0f)
                {
                    isJammerActive = false;
                    jammerButton.interactable = true;
                }
            }
        }
        
        public void AddVoiceClip(AudioClip clip)
        {
            voiceClipQueue.Enqueue(clip);
        }
        
        public void SetSatelliteWarning(string warning)
        {
            satelliteWarningsText.text = warning;
        }
        
        public void ActivateJammer()
        {
            isJammerActive = true;
            jammerTimer = jammerDuration;
            jammerButton.interactable = false;
        }
        
        public void UnlockGreenScreenTerminal()
        {
            greenScreenTerminal.SetActive(true);
        }
        
        public void UnlockOfficerClipboard()
        {
            officerClipboard.SetActive(true);
        }
    }
}