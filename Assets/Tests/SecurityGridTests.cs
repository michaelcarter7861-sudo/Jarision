using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TacticalStealthCore.Tests
{
    public class SecurityGridAndCamerasTests
    {
        [Test]
        public void SecurityGridAndCameras_InitializesCorrectly()
        {
            GameObject testObject = new GameObject();
            SecurityGridAndCameras securityGrid = testObject.AddComponent<SecurityGridAndCameras>();
            
            Assert.IsNotNull(securityGrid);
        }
        
        [UnityTest]
        public IEnumerator SecurityGridAndCameras_SweepsCameraCorrectly()
        {
            GameObject testObject = new GameObject();
            SecurityGridAndCameras securityGrid = testObject.AddComponent<SecurityGridAndCameras>();
            GameObject cameraPivot = new GameObject();
            cameraPivot.transform.parent = testObject.transform;
            securityGrid.cameraPivots = new Transform[] { cameraPivot.transform };
            
            yield return new WaitForSeconds(1f);
            
            Assert.AreNotEqual(0f, cameraPivot.transform.localEulerAngles.y);
        }
    }
}