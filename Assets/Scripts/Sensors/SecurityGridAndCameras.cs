using UnityEngine;
using System.Collections;

namespace TacticalStealthCore
{
    public class SecurityGridAndCameras : MonoBehaviour
    {
        [SerializeField] private Transform[] cameraPivots;
        [SerializeField] private float sweepSpeed = 30f;
        [SerializeField] private float sweepRange = 90f;
        [SerializeField] private float lockOnWarningDuration = 2.0f;
        [SerializeField] private AudioClip lockOnWarningSound;
        [SerializeField] private GameObject[] linkedDevices;
        [SerializeField] private GameObject[] turretTerminals;
        
        private bool[] isCameraActive;
        private bool[] isTurretActive;
        private AudioSource audioSource;
        
        private void Start()
        {
            audioSource = GetComponent<AudioSource>();
            isCameraActive = new bool[cameraPivots.Length];
            isTurretActive = new bool[turretTerminals.Length];
            
            for (int i = 0; i < cameraPivots.Length; i++)
            {
                isCameraActive[i] = true;
                StartCoroutine(SweepCamera(i));
            }
            
            for (int i = 0; i < turretTerminals.Length; i++)
            {
                isTurretActive[i] = true;
            }
        }
        
        private IEnumerator SweepCamera(int index)
        {
            while (true)
            {
                if (isCameraActive[index])
                {
                    float startAngle = cameraPivots[index].localEulerAngles.y;
                    float endAngle = startAngle + sweepRange;
                    
                    while (cameraPivots[index].localEulerAngles.y < endAngle)
                    {
                        cameraPivots[index].localEulerAngles += new Vector3(0, sweepSpeed * Time.deltaTime, 0);
                        yield return null;
                    }
                    
                    endAngle = startAngle - sweepRange;
                    
                    while (cameraPivots[index].localEulerAngles.y > endAngle)
                    {
                        cameraPivots[index].localEulerAngles -= new Vector3(0, sweepSpeed * Time.deltaTime, 0);
                        yield return null;
                    }
                }
                else
                {
                    yield return null;
                }
            }
        }
        
        public void ToggleCameraPower(int index)
        {
            isCameraActive[index] = !isCameraActive[index];
        }
        
        public void ToggleAllCamerasPower()
        {
            for (int i = 0; i < isCameraActive.Length; i++)
            {
                isCameraActive[i] = !isCameraActive[i];
            }
        }
        
        public void ToggleTurretPower(int index)
        {
            isTurretActive[index] = !isTurretActive[index];
        }
        
        public void ToggleAllTurretsPower()
        {
            for (int i = 0; i < isTurretActive.Length; i++)
            {
                isTurretActive[i] = !isTurretActive[i];
            }
        }
        
        public void TriggerLockOnWarning()
        {
            if (audioSource != null && lockOnWarningSound != null)
            {
                audioSource.PlayOneShot(lockOnWarningSound);
            }
        }
    }
}