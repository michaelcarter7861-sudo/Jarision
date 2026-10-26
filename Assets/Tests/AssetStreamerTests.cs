using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Cysharp.Threading.Tasks;

namespace TacticalStealthCore.Tests
{
    public class HeavyMissionAssetStreamerTests
    {
        [UnityTest]
        public async UniTask TestSectorLoading()
        {
            var gameObject = new GameObject();
            var streamer = gameObject.AddComponent<HeavyMissionAssetStreamer>();
            
            // Test loading a sector
            await streamer.LoadMissionSector("Assets/Missions/Sector1.glb");
            
            // Verify the sector was loaded
            Assert.IsTrue(streamer.GetLoadedAssets().ContainsKey("Assets/Missions/Sector1.glb"));
            
            // Clean up
            Object.Destroy(gameObject);
        }
        
        [UnityTest]
        public async UniTask TestMemoryUsage()
        {
            var gameObject = new GameObject();
            var streamer = gameObject.AddComponent<HeavyMissionAssetStreamer>();
            
            // Load multiple sectors and verify memory usage
            await streamer.LoadMissionSector("Assets/Missions/Sector1.glb");
            await streamer.LoadMissionSector("Assets/Missions/Sector2.glb");
            
            // Check memory usage is within limits
            Assert.LessOrEqual(Profiler.GetTotalAllocatedMemoryLong(), 160 * 1024 * 1024);
            
            // Clean up
            Object.Destroy(gameObject);
        }
    }
}