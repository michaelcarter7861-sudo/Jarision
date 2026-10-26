using NUnit.Framework;
using UnityEngine;

namespace TacticalStealthCore.Tests
{
    [TestFixture]
    public class WeaponTests
    {
        [Test]
        public void CombatKnifeFireTest()
        {
            var knife = new CombatKnife();
            int initialAmmo = knife.CurrentAmmo;
            knife.Fire();
            Assert.AreEqual(initialAmmo - 1, knife.CurrentAmmo);
        }

        [Test]
        public void Glock17ReloadTest()
        {
            var glock = new Glock17();
            glock.CurrentAmmo = 0;
            glock.Reload();
            Assert.AreEqual(glock.AmmoCapacity, glock.CurrentAmmo);
        }

        // Add tests for other weapons similarly

        [Test]
        public void ThermalBinocularsPropertiesTest()
        {
            var binoculars = new ThermalBinoculars();
            Assert.AreEqual(0.5f, binoculars.SniperBreathSway);
            Assert.AreEqual(0.2f, binoculars.WoodPenetration);
            Assert.AreEqual(0.1f, binoculars.SheetMetalPenetration);
            Assert.AreEqual(0.8f, binoculars.AcousticShotMasking);
        }
    }
}