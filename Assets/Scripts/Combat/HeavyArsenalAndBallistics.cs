using UnityEngine;
using System.Collections;

namespace TacticalStealthCore
{
    public abstract class Weapon
    {
        public string Name { get; protected set; }
        public int AmmoCapacity { get; protected set; }
        public float FireRate { get; protected set; }
        public float Damage { get; protected set; }
        public float Range { get; protected set; }
        public float Accuracy { get; protected set; }
        public float ReloadTime { get; protected set; }
        public int CurrentAmmo { get; set; }
        
        public abstract void Fire();
        public abstract void Reload();
    }

    public class CombatKnife : Weapon
    {
        public CombatKnife()
        {
            Name = "Combat Knife";
            AmmoCapacity = 1;
            FireRate = 1.0f;
            Damage = 50.0f;
            Range = 1.5f;
            Accuracy = 100.0f;
            ReloadTime = 2.0f;
            CurrentAmmo = AmmoCapacity;
        }

        public override void Fire()
        {
            if (CurrentAmmo > 0)
            {
                Debug.Log("Combat Knife swung!");
                CurrentAmmo--;
            }
            else
            {
                Debug.Log("No ammo left!");
            }
        }

        public override void Reload()
        {
            Debug.Log("Combat Knife does not need reloading.");
        }
    }

    public class Glock17 : Weapon
    {
        public Glock17()
        {
            Name = "Glock 17";
            AmmoCapacity = 17;
            FireRate = 0.5f;
            Damage = 20.0f;
            Range = 50.0f;
            Accuracy = 80.0f;
            ReloadTime = 2.0f;
            CurrentAmmo = AmmoCapacity;
        }

        public override void Fire()
        {
            if (CurrentAmmo > 0)
            {
                Debug.Log("Glock 17 fired!");
                CurrentAmmo--;
            }
            else
            {
                Debug.Log("No ammo left!");
            }
        }

        public override void Reload()
        {
            Debug.Log("Reloading Glock 17...");
            CurrentAmmo = AmmoCapacity;
        }
    }

    // Implement other weapons similarly

    public class ThermalBinoculars : Weapon
    {
        public float SniperBreathSway { get; private set; }
        public float WoodPenetration { get; private set; }
        public float SheetMetalPenetration { get; private set; }
        public float AcousticShotMasking { get; private set; }

        public ThermalBinoculars()
        {
            Name = "Thermal Binoculars";
            AmmoCapacity = 1;
            FireRate = 0.1f;
            Damage = 0.0f;
            Range = 1000.0f;
            Accuracy = 95.0f;
            ReloadTime = 0.0f;
            CurrentAmmo = AmmoCapacity;
            SniperBreathSway = 0.5f;
            WoodPenetration = 0.2f;
            SheetMetalPenetration = 0.1f;
            AcousticShotMasking = 0.8f;
        }

        public override void Fire()
        {
            Debug.Log("Thermal Binoculars used for sniper scope!");
        }

        public override void Reload()
        {
            Debug.Log("Thermal Binoculars do not need reloading.");
        }
    }
}