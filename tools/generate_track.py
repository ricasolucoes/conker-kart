#!/usr/bin/env python3
"""
Procedural 3D Track Generator for Conker-Kart: Windy Barnyard
Generates track mesh, windmill, barn and props in Blender.
"""

import sys
import os
import math

try:
    import bpy
    import bmesh
    sys.path.append('/Users/sierra/Dev/Jogos/OpenSources/stk-blender/io_scene_spm')
    import export_spm
except ImportError:
    print("Error: Run inside Blender: blender --background --python generate_track.py")
    sys.exit(1)

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_mat(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
    return mat

def export_spm_mesh(obj, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    spm_params = {
        'selection-type': 'selected',
        'local-space': False,
        'apply-modifiers': True,
        'keyframes-only': True,
        'export-normal': True,
        'export-vcolor': False,
        'export-tangent': False,
        'static-mesh-frame': 1
    }
    export_spm.writeSPMFile(filepath, spm_params)
    print(f"Exported Track SPM: {filepath}")

def build_windy_track():
    clear_scene()
    
    mat_grass = create_mat("GrassGreen", (0.2, 0.6, 0.15, 1.0), roughness=0.9)
    mat_road = create_mat("DirtRoad", (0.45, 0.35, 0.2, 1.0), roughness=0.85)
    mat_wood = create_mat("FenceWood", (0.5, 0.3, 0.15, 1.0), roughness=0.7)
    mat_barn = create_mat("BarnRed", (0.75, 0.15, 0.1, 1.0), roughness=0.6)
    mat_roof = create_mat("BarnRoof", (0.2, 0.2, 0.22, 1.0), roughness=0.5)

    # 1. Ground Plane (Rolling Hills)
    bpy.ops.mesh.primitive_plane_add(size=300, location=(0, -0.5, 0))
    ground = bpy.context.active_object
    ground.data.materials.append(mat_grass)

    # 2. Race Track Circuit (Large loop: straightaways at X = +/- 40, semicircular turns at Z = +/- 60)
    # Build track mesh using a segmented closed curve / extruded ribbon
    # Straight 1 (East)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(40, 0, 0), scale=(12, 0.2, 100))
    bpy.context.active_object.data.materials.append(mat_road)

    # Straight 2 (West)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-40, 0, 0), scale=(12, 0.2, 100))
    bpy.context.active_object.data.materials.append(mat_road)

    # North Turn
    bpy.ops.mesh.primitive_cylinder_add(radius=46, depth=0.2, vertices=32, location=(0, 0, 50))
    bpy.context.active_object.data.materials.append(mat_road)

    # South Turn
    bpy.ops.mesh.primitive_cylinder_add(radius=46, depth=0.2, vertices=32, location=(0, 0, -50))
    bpy.context.active_object.data.materials.append(mat_road)

    # Cutout center island for North & South turns
    bpy.ops.mesh.primitive_cylinder_add(radius=34, depth=0.3, vertices=32, location=(0, 0.05, 50))
    bpy.context.active_object.data.materials.append(mat_grass)

    bpy.ops.mesh.primitive_cylinder_add(radius=34, depth=0.3, vertices=32, location=(0, 0.05, -50))
    bpy.context.active_object.data.materials.append(mat_grass)

    # Center Field
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.05, 0), scale=(68, 0.3, 100))
    bpy.context.active_object.data.materials.append(mat_grass)

    # 3. Scenery: Windy Mill (The iconic windmill on the hill)
    bpy.ops.mesh.primitive_cylinder_add(radius=8, depth=24, vertices=16, location=(0, 12, 0))
    windmill_body = bpy.context.active_object
    windmill_body.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cone_add(radius1=9, depth=8, location=(0, 28, 0))
    bpy.context.active_object.data.materials.append(mat_roof)

    # 4 Windmill Blades
    for rot in [0, 90, 180, 270]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 24, 8.5), scale=(1.8, 16, 0.2), rotation=(0, 0, math.radians(rot)))
        bpy.context.active_object.data.materials.append(mat_wood)

    # 4. Scenery: Red Barn (Classic Barnyard)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(65, 6, 20), scale=(16, 12, 24))
    bpy.context.active_object.data.materials.append(mat_barn)

    bpy.ops.mesh.primitive_cylinder_add(radius=9, depth=24, vertices=8, location=(65, 15, 20), rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_roof)

    # 5. Wooden fences along straightaway
    for fz in range(-45, 46, 15):
        for fx in [33, 47, -33, -47]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=2.0, location=(fx, 1.0, fz))
            bpy.context.active_object.data.materials.append(mat_wood)

    # Join into single track mesh
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = ground
    bpy.ops.object.join()
    ground.name = "WindyBarnyardTrack"
    return ground

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    track_dir = os.path.join(root_dir, "tracks", "windy_barnyard")
    os.makedirs(track_dir, exist_ok=True)
    
    print("Building Windy Barnyard 3D track mesh...")
    track_mesh = build_windy_track()
    export_spm_mesh(track_mesh, os.path.join(track_dir, "windy_track.spm"))
    print("Track 3D mesh generated successfully!")

if __name__ == "__main__":
    main()
