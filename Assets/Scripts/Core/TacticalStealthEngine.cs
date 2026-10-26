using System;
using UnityEngine;

namespace TacticalStealthCore
{
    public enum SurfaceType : byte { Concrete = 0, MetalGrate = 1, Gravel = 2, Grass = 3, Mud = 4, Snow = 5 }
    public enum GuardState : byte { Patrol = 0, Suspicious = 1, Investigating = 2, RadioTransmitting = 3, CombatSearch = 4, Engage = 5, Dead = 6, DraggedCorpse = 7 }
    public enum SoundCategory : byte { Footstep = 0, ThudOrDoor = 1, SuppressedShot = 2, UnsuppressedShot = 3, EnvironmentalMask = 4, Alarm = 5 }

    [Serializable]
    public struct SoundEvent
    {
        public Vector3 Position;
        public float RadiusSqr;
        public float Intensity;
        public SoundCategory Category;
    }

    [Serializable]
    public struct AnomalyNode
    {
        public int NodeID;
        public string NodeTag;
        public Vector3 Position;
        public bool DefaultState;
        public bool CurrentState;
        public bool IsBeingInvestigated;
    }

    public class StealthDirector : MonoBehaviour
    {
        public static StealthDirector Instance { get; private set; }
        public bool IsBaseAlarmActive { get; private set; }
        public bool IsRadioJammerActive { get; private set; }
        public Vector3 LastKnownPlayerPosition { get; private set; }

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
        }

        public void ActivateHandlerRadioJammer(float duration = 15f) => IsRadioJammerActive = duration > 0f;

        public void BroadcastRadioAlert(Vector3 playerPos, bool fullBaseAlarm)
        {
            if (IsRadioJammerActive) return;
            LastKnownPlayerPosition = playerPos;
            if (fullBaseAlarm) IsBaseAlarmActive = true;
        }
    }
}
