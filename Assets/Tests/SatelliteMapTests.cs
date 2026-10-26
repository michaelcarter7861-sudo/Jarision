using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TacticalStealthCore.Tests
{
    public class IGISatelliteMapComputerTests
    {
        private GameObject testObject;
        private IGISatelliteMapComputer satelliteMapComputer;

        [SetUp]
        public void SetUp()
        {
            testObject = new GameObject();
            satelliteMapComputer = testObject.AddComponent<IGISatelliteMapComputer>();
        }

        [TearDown]
        public void TearDown()
        {
            Object.DestroyImmediate(testObject);
        }

        [Test]
        public void IGISatelliteMapComputer_InitializesCorrectly()
        {
            Assert.IsNotNull(satelliteMapComputer);
        }

        [Test]
        public void ToggleZoomLevel_ChangesZoomLevel()
        {
            int initialZoomLevel = satelliteMapComputer.currentZoomLevel;
            satelliteMapComputer.ToggleZoomLevel();
            Assert.AreNotEqual(initialZoomLevel, satelliteMapComputer.currentZoomLevel);
        }

        [Test]
        public void ToggleWireframeMode_TogglesWireframeMode()
        {
            bool initialWireframeMode = satelliteMapComputer.isWireframeMode;
            satelliteMapComputer.ToggleWireframeMode();
            Assert.AreNotEqual(initialWireframeMode, satelliteMapComputer.isWireframeMode);
        }

        [Test]
        public void AddVisionCone_AddsVisionCone()
        {
            int initialCount = satelliteMapComputer.activeVisionCones.Count;
            satelliteMapComputer.AddVisionCone(Vector3.zero, 10f, 90f, Color.green);
            Assert.AreEqual(initialCount + 1, satelliteMapComputer.activeVisionCones.Count);
        }

        [Test]
        public void AddBlip_AddsBlip()
        {
            int initialCount = satelliteMapComputer.activeBlips.Count;
            satelliteMapComputer.AddBlip(Vector3.zero, Color.red, true);
            Assert.AreEqual(initialCount + 1, satelliteMapComputer.activeBlips.Count);
        }

        [Test]
        public void AddObjectiveMarker_AddsObjectiveMarker()
        {
            int initialCount = satelliteMapComputer.activeObjectiveMarkers.Count;
            satelliteMapComputer.AddObjectiveMarker(Vector3.zero, 1);
            Assert.AreEqual(initialCount + 1, satelliteMapComputer.activeObjectiveMarkers.Count);
        }

        [Test]
        public void AddPowerGridLine_AddsPowerGridLine()
        {
            int initialCount = satelliteMapComputer.activePowerGridLines.Count;
            satelliteMapComputer.AddPowerGridLine(Vector3.zero, Vector3.one);
            Assert.AreEqual(initialCount + 1, satelliteMapComputer.activePowerGridLines.Count);
        }
    }
}