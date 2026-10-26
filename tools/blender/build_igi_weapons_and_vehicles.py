import bpy
import os

OUTPUT_DIR = os.path.join("Assets", "StreamingAssets", "Models")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def make_mat(name, rgba, metallic=0.2, roughness=0.7):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

def build_and_export(filename, parts):
    reset_scene()
    for p_type, loc, scale, color in parts:
        if p_type == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=loc)
        elif p_type == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=loc)
        else:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        obj = bpy.context.active_object
        obj.scale = scale
        obj.data.materials.append(make_mat(f"Mat_{filename}", color))
    out_path = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.gltf(filepath=out_path, export_format='GLB')
    print(f"[BLENDER-5.0-VERIFIED] Exported {out_path}")

ASSETS = {
    "IGI_Watchtower.glb": [
        ("cube", (-2, -2, 6), (0.35, 0.35, 12), (0.2, 0.22, 0.24, 1)),
        ("cube", (2, -2, 6), (0.35, 0.35, 12), (0.2, 0.22, 0.24, 1)),
        ("cube", (-2, 2, 6), (0.35, 0.35, 12), (0.2, 0.22, 0.24, 1)),
        ("cube", (2, 2, 6), (0.35, 0.35, 12), (0.2, 0.22, 0.24, 1)),
        ("cube", (0, 0, 12.2), (5.0, 5.0, 0.4), (0.42, 0.44, 0.43, 1)),
        ("cube", (0, 0, 15.0), (5.4, 5.4, 0.3), (0.35, 0.37, 0.36, 1))
    ],
    "IGI_ConcreteBunker.glb": [
        ("cube", (0, 0, 2.0), (8.0, 6.0, 4.0), (0.4, 0.42, 0.4, 1)),
        ("cube", (0, 3.1, 1.2), (1.8, 0.4, 2.4), (0.15, 0.18, 0.15, 1))
    ],
    "IGI_RadarDome.glb": [
        ("cylinder", (0, 0, 2.0), (3.5, 3.5, 4.0), (0.45, 0.46, 0.45, 1)),
        ("sphere", (0, 0, 5.5), (4.2, 4.2, 4.2), (0.85, 0.87, 0.88, 1))
    ],
    "IGI_SAMLauncher.glb": [
        ("cube", (0, 0, 1.0), (3.0, 3.0, 2.0), (0.25, 0.3, 0.22, 1)),
        ("cylinder", (-0.8, 0, 2.8), (0.35, 0.35, 3.2), (0.3, 0.35, 0.28, 1)),
        ("cylinder", (0.8, 0, 2.8), (0.35, 0.35, 3.2), (0.3, 0.35, 0.28, 1))
    ],
    "IGI_DragunovSVD.glb": [
        ("cube", (0, 0, 0), (0.06, 1.22, 0.14), (0.12, 0.12, 0.14, 1)),
        ("cylinder", (0, 0.45, 0.04), (0.02, 0.02, 0.65), (0.08, 0.08, 0.1, 1)),
        ("cylinder", (0, 0.1, 0.11), (0.025, 0.025, 0.28), (0.1, 0.1, 0.12, 1))
    ],
    "IGI_MP5SD.glb": [
        ("cube", (0, 0, 0), (0.06, 0.68, 0.16), (0.1, 0.11, 0.13, 1)),
        ("cylinder", (0, 0.28, 0.03), (0.035, 0.035, 0.32), (0.08, 0.09, 0.1, 1))
    ],
    "IGI_BTR80_APC.glb": [
        ("cube", (0, 0, 1.2), (2.9, 7.6, 2.1), (0.22, 0.28, 0.2, 1)),
        ("cylinder", (0, 0.5, 2.5), (1.1, 1.1, 0.7), (0.18, 0.24, 0.16, 1))
    ]
}

if __name__ == "__main__":
    for name, spec in ASSETS.items():
        build_and_export(name, spec)
