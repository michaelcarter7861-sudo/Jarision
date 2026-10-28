using UnityEditor;
using UnityEngine;
using System.IO;
using System.Collections.Generic;

namespace TacticalStealthCore
{
    public class JarisionHeadlessAndroidBuilder : MonoBehaviour
    {
        [MenuItem("Build/Build Android APK")]
        public static void BuildAndroidAPK()
        {
            // Set build target to Android
            EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.Android, BuildTarget.Android);

            // Set build options
            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            buildPlayerOptions.target = BuildTarget.Android;
            buildPlayerOptions.options = BuildOptions.None;

            // Set output path
            string outputPath = Path.Combine(Application.dataPath, "../Builds/Android/Jarision.apk");
            buildPlayerOptions.locationPathName = outputPath;

            // Set scenes to include in build
            List<string> scenes = new List<string>();
            foreach (EditorBuildSettingsScene scene in EditorBuildSettings.scenes)
            {
                if (scene.enabled)
                {
                    scenes.Add(scene.path);
                }
            }
            buildPlayerOptions.scenes = scenes.ToArray();

            // Set Android build options
            EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;
            EditorUserBuildSettings.androidBuildType = AndroidBuildType.Release;
            EditorUserBuildSettings.androidMinimumSdkVersion = AndroidSdkVersions.AndroidApiLevel28;
            EditorUserBuildSettings.androidTargetSdkVersion = AndroidSdkVersions.AndroidApiLevel28;
            EditorUserBuildSettings.androidTargetArchitectures = AndroidArchitecture.ARM64;

            // Set scripting backend to IL2CPP
            PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);

            // Build the APK
            BuildPipeline.BuildPlayer(buildPlayerOptions);

            // Log build completion
            Debug.Log("Android APK build completed: " + outputPath);
        }
    }
}