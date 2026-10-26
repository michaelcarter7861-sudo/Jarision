using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TacticalStealthCore.Tests
{
    public class OutsideHandlerAndBaseIntelSystemTests
    {
        [UnityTest]
        public IEnumerator TestVoiceClipQueue()
        {
            var gameObject = new GameObject();
            var system = gameObject.AddComponent<OutsideHandlerAndBaseIntelSystem>();
            var clip1 = AudioClip.Create("Clip1", 44100, 1, 44100, false);
            var clip2 = AudioClip.Create("Clip2", 44100, 1, 44100, false);
            
            system.AddVoiceClip(clip1);
            system.AddVoiceClip(clip2);
            
            yield return new WaitForSeconds(1f);
            
            Assert.AreEqual(0, system.voiceClipQueue.Count);
        }
        
        [UnityTest]
        public IEnumerator TestJammerActivation()
        {
            var gameObject = new GameObject();
            var system = gameObject.AddComponent<OutsideHandlerAndBaseIntelSystem>();
            
            system.ActivateJammer();
            
            yield return new WaitForSeconds(1f);
            
            Assert.IsTrue(system.isJammerActive);
            
            yield return new WaitForSeconds(15f);
            
            Assert.IsFalse(system.isJammerActive);
        }
    }
}