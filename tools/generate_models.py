#!/usr/bin/env python3
"""
Procedural 3D Model Generator for all 10 Conker-Kart Characters & Karts using Blender (bpy).
1. Conker (Nitro Rod)
2. Berri (Pink Fury)
3. Panther King (Golden Royal Tank)
4. The Great Mighty Poo (Porcelain Sludge Throne)
5. Professor Von Kriplespac (Cyber Hovercraft)
6. Gregg the Grim Reaper (Bone Hearse)
7. Tediz Commander (War Half-Track)
8. Buga the Cavedude (Flintstone Smasher)
9. Franky the Pitchfork (Hay Bale Tractor)
10. King Bee (Honeycomb Stinger)
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
    print("Error: Run inside Blender: blender --background --python generate_models.py")
    sys.exit(1)

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_mat(name, color, roughness=0.4, metallic=0.0):
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
        'local-space': True,
        'apply-modifiers': True,
        'keyframes-only': True,
        'export-normal': True,
        'export-vcolor': False,
        'export-tangent': False,
        'static-mesh-frame': 1
    }
    export_spm.writeSPMFile(filepath, spm_params)
    print(f"Exported SPM: {filepath}")

def export_obj(obj, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.obj_export(
        filepath=filepath,
        export_selected_objects=True,
        export_materials=True,
        forward_axis='Y',
        up_axis='Z'
    )
    print(f"Exported: {filepath}")

def build_wheel():
    clear_scene()
    mat_tire = create_mat("WheelTire", (0.1, 0.1, 0.12, 1.0), roughness=0.8)
    mat_rim = create_mat("WheelRim", (0.9, 0.75, 0.1, 1.0), roughness=0.3, metallic=0.8)
    mat_hub = create_mat("WheelHub", (0.8, 0.1, 0.1, 1.0), roughness=0.4)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.22, vertices=24, rotation=(0, math.pi/2, 0))
    tire = bpy.context.active_object
    tire.data.materials.append(mat_tire)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.23, vertices=24, rotation=(0, math.pi/2, 0))
    rim = bpy.context.active_object
    rim.data.materials.append(mat_rim)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.25, vertices=16, rotation=(0, math.pi/2, 0))
    hub = bpy.context.active_object
    hub.data.materials.append(mat_hub)
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = tire
    bpy.ops.object.join()
    tire.name = "KartWheel"
    return tire

# 1. Conker
def build_conker():
    clear_scene()
    mat_red = create_mat("ConkerRed", (0.85, 0.1, 0.05, 1.0), roughness=0.3)
    mat_yellow = create_mat("ConkerYellow", (1.0, 0.8, 0.05, 1.0), roughness=0.3)
    mat_metal = create_mat("ChromeExhaust", (0.8, 0.8, 0.85, 1.0), roughness=0.15, metallic=0.9)
    mat_seat = create_mat("SeatBlack", (0.15, 0.15, 0.18, 1.0), roughness=0.7)
    mat_fur = create_mat("SquirrelFur", (0.92, 0.42, 0.08, 1.0), roughness=0.9)
    mat_hoodie = create_mat("ConkerHoodie", (0.08, 0.35, 0.85, 1.0), roughness=0.6)
    mat_leather = create_mat("AviatorLeather", (0.35, 0.2, 0.1, 1.0), roughness=0.5)
    mat_glass = create_mat("GogglesLens", (0.2, 0.8, 0.95, 1.0), roughness=0.1, metallic=0.5)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.15, 0), scale=(0.85, 0.12, 1.4))
    base = bpy.context.active_object
    base.data.materials.append(mat_seat)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.28, 0.65), scale=(0.7, 0.18, 0.7))
    bpy.context.active_object.data.materials.append(mat_red)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.38, 0.65), scale=(0.2, 0.02, 0.72))
    bpy.context.active_object.data.materials.append(mat_yellow)

    for px in [-0.42, 0.42]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0.22, 0), scale=(0.25, 0.15, 0.8))
        bpy.context.active_object.data.materials.append(mat_red)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.45, -0.3), scale=(0.45, 0.5, 0.12), rotation=(math.radians(-15), 0, 0))
    bpy.context.active_object.data.materials.append(mat_seat)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.025, location=(0, 0.55, 0.02), rotation=(math.radians(45), 0, 0))
    bpy.context.active_object.data.materials.append(mat_seat)

    # Exhaust pipes
    for ex in [-0.22, 0.22]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.45, location=(ex, 0.32, -0.85), rotation=(math.radians(90), 0, 0))
        bpy.context.active_object.data.materials.append(mat_metal)

    # Rear spoiler
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.72, -0.75), scale=(0.95, 0.05, 0.25))
    bpy.context.active_object.data.materials.append(mat_yellow)

    # Driver Conker
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.52, -0.15), scale=(0.35, 0.35, 0.3))
    bpy.context.active_object.data.materials.append(mat_hoodie)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(0, 0.85, -0.12))
    bpy.context.active_object.data.materials.append(mat_fur)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0.8, 0.08), scale=(0.9, 0.7, 1.2))
    bpy.context.active_object.data.materials.append(mat_fur)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.235, location=(0, 0.88, -0.14), scale=(1.02, 1.0, 0.95))
    bpy.context.active_object.data.materials.append(mat_leather)

    for gx in [-0.09, 0.09]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.04, location=(gx, 0.92, 0.04), rotation=(math.radians(75), 0, 0))
        bpy.context.active_object.data.materials.append(mat_glass)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0, 0.65, -0.55), scale=(0.7, 1.4, 0.9), rotation=(math.radians(35), 0, 0))
    bpy.context.active_object.data.materials.append(mat_fur)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "ConkerChassis"
    return base

# 2. Berri
def build_berri():
    clear_scene()
    mat_pink = create_mat("BerriPink", (0.95, 0.25, 0.6, 1.0), roughness=0.25)
    mat_white = create_mat("BerriWhite", (0.95, 0.95, 0.95, 1.0), roughness=0.3)
    mat_driver_pink = create_mat("BerriOutfit", (0.9, 0.15, 0.5, 1.0), roughness=0.4)
    mat_driver_fur = create_mat("BerriFur", (0.95, 0.9, 0.85, 1.0), roughness=0.8)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.15, 0), scale=(0.8, 0.12, 1.35))
    base = bpy.context.active_object
    base.data.materials.append(mat_pink)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.8, location=(0, 0.25, 0.6), rotation=(math.radians(90), 0, 0), scale=(0.9, 0.45, 1.0))
    bpy.context.active_object.data.materials.append(mat_white)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.68, -0.7), scale=(0.9, 0.04, 0.22))
    bpy.context.active_object.data.materials.append(mat_pink)

    # Driver: Berri
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(0, 0.82, -0.1))
    bpy.context.active_object.data.materials.append(mat_driver_fur)

    for ex in [-0.09, 0.09]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.4, location=(ex, 1.15, -0.1), scale=(0.6, 1.0, 1.0), rotation=(math.radians(-10), 0, 0))
        bpy.context.active_object.data.materials.append(mat_pink)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.5, -0.12), scale=(0.32, 0.32, 0.28))
    bpy.context.active_object.data.materials.append(mat_driver_pink)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "BerriChassis"
    return base

# 3. Panther King
def build_panther():
    clear_scene()
    mat_gold = create_mat("PantherGold", (0.85, 0.65, 0.15, 1.0), roughness=0.3, metallic=0.7)
    mat_armor = create_mat("PantherDarkArmor", (0.15, 0.15, 0.18, 1.0), roughness=0.6, metallic=0.5)
    mat_fur = create_mat("PantherFur", (0.1, 0.1, 0.12, 1.0), roughness=0.9)
    mat_cape = create_mat("PantherCape", (0.8, 0.05, 0.1, 1.0), roughness=0.6)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.2, 0), scale=(0.95, 0.22, 1.5))
    base = bpy.context.active_object
    base.data.materials.append(mat_armor)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.25, 0.75), scale=(1.05, 0.2, 0.25))
    bpy.context.active_object.data.materials.append(mat_gold)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0, 0.9, -0.15))
    bpy.context.active_object.data.materials.append(mat_fur)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.18, vertices=8, location=(0, 1.18, -0.15))
    bpy.context.active_object.data.materials.append(mat_gold)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.55, -0.45), scale=(0.6, 0.5, 0.08), rotation=(math.radians(20), 0, 0))
    bpy.context.active_object.data.materials.append(mat_cape)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "PantherChassis"
    return base

# 4. The Great Mighty Poo
def build_mighty_poo():
    clear_scene()
    mat_porcelain = create_mat("ToiletCeramic", (0.95, 0.95, 0.95, 1.0), roughness=0.1)
    mat_poo = create_mat("MightyPooBrown", (0.45, 0.25, 0.08, 1.0), roughness=0.8)
    mat_teeth = create_mat("PooTeeth", (0.95, 0.92, 0.75, 1.0), roughness=0.3)
    mat_mouth = create_mat("PooMouth", (0.2, 0.05, 0.05, 1.0), roughness=0.5)
    mat_tp = create_mat("ToiletPaper", (0.98, 0.98, 0.98, 1.0), roughness=0.9)
    mat_pipes = create_mat("PlumbingChrome", (0.75, 0.75, 0.8, 1.0), roughness=0.2, metallic=0.9)

    # Toilet Bowl Base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.35, vertices=24, location=(0, 0.25, 0))
    base = bpy.context.active_object
    base.data.materials.append(mat_porcelain)

    # Cistern Tank behind
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.65, -0.45), scale=(0.7, 0.6, 0.28))
    bpy.context.active_object.data.materials.append(mat_porcelain)

    # Toilet Paper Rolls on sides
    for tpx in [-0.48, 0.48]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.22, location=(tpx, 0.35, 0), rotation=(0, math.pi/2, 0))
        bpy.context.active_object.data.materials.append(mat_tp)

    # Sewer plumbing exhausts
    for px in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.4, location=(px, 0.3, -0.7), rotation=(math.radians(80), 0, 0))
        bpy.context.active_object.data.materials.append(mat_pipes)

    # DRIVER: The Great Mighty Poo
    # Tiered Poo Body (Bottom swirl, mid swirl, top swirl)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.38, location=(0, 0.55, 0.05), scale=(1.1, 0.8, 1.1))
    bpy.context.active_object.data.materials.append(mat_poo)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0.8, 0.02), scale=(1.0, 0.8, 1.0))
    bpy.context.active_object.data.materials.append(mat_poo)

    bpy.ops.mesh.primitive_cone_add(radius1=0.22, depth=0.35, location=(0, 1.05, 0))
    bpy.context.active_object.data.materials.append(mat_poo)

    # Big singing mouth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.75, 0.26), scale=(0.35, 0.2, 0.1))
    bpy.context.active_object.data.materials.append(mat_mouth)

    # Goofy teeth
    for tx in [-0.1, 0.1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, 0.82, 0.28), scale=(0.06, 0.06, 0.05))
        bpy.context.active_object.data.materials.append(mat_teeth)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "MightyPooChassis"
    return base

# 5. Professor Von Kriplespac
def build_von_kriplespac():
    clear_scene()
    mat_cyber = create_mat("CyberChrome", (0.7, 0.75, 0.8, 1.0), roughness=0.2, metallic=0.9)
    mat_neon = create_mat("PlasmaCyan", (0.1, 0.9, 0.95, 1.0), roughness=0.1)
    mat_coat = create_mat("LabCoat", (0.9, 0.9, 0.95, 1.0), roughness=0.6)
    mat_weasel = create_mat("WeaselFur", (0.55, 0.4, 0.25, 1.0), roughness=0.8)
    mat_hair = create_mat("WildWhiteHair", (0.95, 0.95, 0.95, 1.0), roughness=0.9)
    mat_target = create_mat("RedMonocle", (0.95, 0.05, 0.05, 1.0), roughness=0.1)

    # Futuristic streamlined saucer / pod base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.18, vertices=24, location=(0, 0.18, 0))
    base = bpy.context.active_object
    base.data.materials.append(mat_cyber)

    # Glowing plasma intake rings
    for rx in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.04, location=(rx, 0.22, 0.3), rotation=(math.radians(90), 0, 0))
        bpy.context.active_object.data.materials.append(mat_neon)

    # Robotic tentacles arching over back
    for tx, rotz in [(-0.3, -20), (0.3, 20)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.7, location=(tx, 0.6, -0.4), rotation=(math.radians(30), 0, math.radians(rotz)))
        bpy.context.active_object.data.materials.append(mat_cyber)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(tx*1.2, 0.9, -0.25))
        bpy.context.active_object.data.materials.append(mat_neon)

    # Driver: Von Kriplespac
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.48, -0.1), scale=(0.32, 0.35, 0.28))
    bpy.context.active_object.data.materials.append(mat_coat)

    # Weasel head & pointed snout
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(0, 0.78, -0.08))
    bpy.context.active_object.data.materials.append(mat_weasel)

    bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.25, location=(0, 0.75, 0.12), rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_weasel)

    # Wild scientist hair tufts
    for hx in [-0.18, 0.18]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(hx, 0.86, -0.08), scale=(1.2, 0.8, 1.0))
        bpy.context.active_object.data.materials.append(mat_hair)

    # Cyber monocle on left eye
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.05, location=(0.08, 0.82, 0.05), rotation=(math.radians(85), 0, 0))
    bpy.context.active_object.data.materials.append(mat_target)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "KriplespacChassis"
    return base

# 6. Gregg the Grim Reaper
def build_gregg():
    clear_scene()
    mat_wood = create_mat("CoffinWood", (0.25, 0.15, 0.1, 1.0), roughness=0.7)
    mat_bone = create_mat("SkeletonBone", (0.88, 0.85, 0.78, 1.0), roughness=0.5)
    mat_cloak = create_mat("ReaperCloak", (0.08, 0.08, 0.09, 1.0), roughness=0.9)
    mat_eyes = create_mat("CyanGlow", (0.1, 0.95, 0.95, 1.0), roughness=0.1)
    mat_scythe = create_mat("ScytheSteel", (0.75, 0.75, 0.8, 1.0), roughness=0.1, metallic=0.9)

    # Coffin-shaped kart chassis
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.2, 0), scale=(0.75, 0.2, 1.4))
    base = bpy.context.active_object
    base.data.materials.append(mat_wood)

    # Front skull bumper
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(0, 0.25, 0.72))
    bpy.context.active_object.data.materials.append(mat_bone)

    # Crossbones on side
    for bx in [-0.42, 0.42]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.6, location=(bx, 0.25, 0), rotation=(0, math.radians(45), 0))
        bpy.context.active_object.data.materials.append(mat_bone)

    # Driver: Gregg
    bpy.ops.mesh.primitive_cone_add(radius1=0.28, depth=0.55, location=(0, 0.55, -0.15))
    bpy.context.active_object.data.materials.append(mat_cloak)

    # Hood & Skull
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(0, 0.82, -0.12))
    bpy.context.active_object.data.materials.append(mat_cloak)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(0, 0.8, -0.02))
    bpy.context.active_object.data.materials.append(mat_bone)

    # Glowing eye pinpoints
    for ex in [-0.05, 0.05]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=(ex, 0.83, 0.1))
        bpy.context.active_object.data.materials.append(mat_eyes)

    # Scythe mounted behind
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.9, location=(0.28, 0.7, -0.4), rotation=(math.radians(25), 0, math.radians(-15)))
    bpy.context.active_object.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.025, location=(0.22, 1.1, -0.48), rotation=(0, math.pi/2, 0))
    bpy.context.active_object.data.materials.append(mat_scythe)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "GreggChassis"
    return base

# 7. Tediz Commander
def build_tediz():
    clear_scene()
    mat_green = create_mat("ArmyDrab", (0.28, 0.35, 0.22, 1.0), roughness=0.6)
    mat_metal = create_mat("DarkSteel", (0.2, 0.22, 0.22, 1.0), roughness=0.4, metallic=0.7)
    mat_bear = create_mat("StitchedPlush", (0.48, 0.32, 0.18, 1.0), roughness=0.9)
    mat_helmet = create_mat("Stahlhelm", (0.22, 0.28, 0.18, 1.0), roughness=0.5, metallic=0.4)
    mat_redeye = create_mat("CyborgRed", (0.95, 0.05, 0.05, 1.0), roughness=0.1)

    # Armored boxy military kart
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.22, 0), scale=(0.9, 0.24, 1.5))
    base = bpy.context.active_object
    base.data.materials.append(mat_green)

    # Armor plates / hood slant
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.32, 0.5), scale=(0.82, 0.15, 0.6), rotation=(math.radians(-10), 0, 0))
    bpy.context.active_object.data.materials.append(mat_green)

    # Twin Minigun rocket exhausts
    for mx in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.55, location=(mx, 0.45, -0.75), rotation=(math.radians(65), 0, 0))
        bpy.context.active_object.data.materials.append(mat_metal)

    # Driver: Tediz Commander
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.5, -0.1), scale=(0.38, 0.35, 0.32))
    bpy.context.active_object.data.materials.append(mat_green)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.24, location=(0, 0.85, -0.1))
    bpy.context.active_object.data.materials.append(mat_bear)

    # Round Teddy Bear Ears
    for rx in [-0.2, 0.2]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(rx, 1.05, -0.12))
        bpy.context.active_object.data.materials.append(mat_bear)

    # Military Steel Helmet
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.26, location=(0, 0.94, -0.1), scale=(1.05, 1.0, 0.8))
    bpy.context.active_object.data.materials.append(mat_helmet)

    # Glowing Red Eye
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.04, location=(0.09, 0.88, 0.1), rotation=(math.radians(85), 0, 0))
    bpy.context.active_object.data.materials.append(mat_redeye)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "TedizChassis"
    return base

# 8. Buga the Cavedude
def build_buga():
    clear_scene()
    mat_stone = create_mat("ChiseledRock", (0.5, 0.52, 0.55, 1.0), roughness=0.9)
    mat_tusk = create_mat("MammothTusk", (0.9, 0.88, 0.78, 1.0), roughness=0.4)
    mat_skin = create_mat("CavemanSkin", (0.85, 0.62, 0.45, 1.0), roughness=0.8)
    mat_leopard = create_mat("LeopardFur", (0.85, 0.65, 0.15, 1.0), roughness=0.7)
    mat_beard = create_mat("DarkBeard", (0.1, 0.1, 0.1, 1.0), roughness=0.9)

    # Heavy Stone Kart Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.22, 0), scale=(0.95, 0.24, 1.5))
    base = bpy.context.active_object
    base.data.materials.append(mat_stone)

    # Giant Mammoth Tusk Bumper Guards
    for tx, roty in [(-0.45, -25), (0.45, 25)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.6, location=(tx, 0.25, 0.8), rotation=(math.radians(20), math.radians(roty), 0))
        bpy.context.active_object.data.materials.append(mat_tusk)

    # Driver: Buga
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.52, -0.1), scale=(0.48, 0.42, 0.35))
    bpy.context.active_object.data.materials.append(mat_leopard)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.26, location=(0, 0.88, -0.1))
    bpy.context.active_object.data.materials.append(mat_skin)

    # Big Caveman Beard & Hair
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.24, location=(0, 0.76, 0.08), scale=(1.1, 0.9, 0.8))
    bpy.context.active_object.data.materials.append(mat_beard)

    # Bone in hair
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.45, location=(0, 1.15, -0.1), rotation=(0, math.pi/2, 0))
    bpy.context.active_object.data.materials.append(mat_tusk)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "BugaChassis"
    return base

# 9. Franky the Pitchfork
def build_franky():
    clear_scene()
    mat_tractor = create_mat("RustyTractor", (0.55, 0.2, 0.15, 1.0), roughness=0.7)
    mat_hay = create_mat("HayBale", (0.85, 0.75, 0.3, 1.0), roughness=0.9)
    mat_wood = create_mat("PitchforkHandle", (0.6, 0.45, 0.25, 1.0), roughness=0.6)
    mat_tines = create_mat("ForkSteel", (0.65, 0.65, 0.7, 1.0), roughness=0.3, metallic=0.8)
    mat_eyes = create_mat("CartoonEye", (0.95, 0.95, 0.95, 1.0), roughness=0.2)
    mat_pupil = create_mat("CartoonPupil", (0.05, 0.05, 0.05, 1.0), roughness=0.2)

    # Farm Tractor Hood
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.25, 0.4), scale=(0.65, 0.35, 0.8))
    base = bpy.context.active_object
    base.data.materials.append(mat_tractor)

    # Vertical Tractor Chimney Exhaust
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.5, location=(0.22, 0.6, 0.5))
    bpy.context.active_object.data.materials.append(mat_tractor)

    # Hay bale stack behind seat
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.35, -0.45), scale=(0.75, 0.4, 0.6))
    bpy.context.active_object.data.materials.append(mat_hay)

    # DRIVER: Franky (Sentient Pitchfork)
    # Pitchfork Wooden Shaft Body
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.75, location=(0, 0.6, -0.05))
    bpy.context.active_object.data.materials.append(mat_wood)

    # Expressive sad googly eyes on handle
    for ex in [-0.06, 0.06]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=(ex, 0.78, 0.03))
        bpy.context.active_object.data.materials.append(mat_eyes)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(ex, 0.78, 0.07))
        bpy.context.active_object.data.materials.append(mat_pupil)

    # Curved Metal Tines Head
    for tx in [-0.12, -0.04, 0.04, 0.12]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.35, location=(tx, 1.15, -0.05))
        bpy.context.active_object.data.materials.append(mat_tines)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "FrankyChassis"
    return base

# 10. King Bee
def build_king_bee():
    clear_scene()
    mat_honeycomb = create_mat("HoneycombGold", (0.95, 0.7, 0.1, 1.0), roughness=0.3)
    mat_honey_drip = create_mat("GoldenHoney", (0.9, 0.55, 0.05, 1.0), roughness=0.1)
    mat_bee_black = create_mat("BeeBlack", (0.1, 0.1, 0.12, 1.0), roughness=0.8)
    mat_bee_yellow = create_mat("BeeYellow", (0.98, 0.85, 0.05, 1.0), roughness=0.7)
    mat_crown = create_mat("RoyalCrownGold", (0.9, 0.75, 0.15, 1.0), roughness=0.2, metallic=0.85)
    mat_wings = create_mat("GossamerWings", (0.8, 0.9, 0.98, 1.0), roughness=0.1)

    # Hexagonal Honeycomb Speed Pod Base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.2, vertices=6, location=(0, 0.2, 0))
    base = bpy.context.active_object
    base.data.materials.append(mat_honeycomb)

    # Honey drips on sides
    for hx in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(hx, 0.15, 0), scale=(1.0, 1.5, 0.8))
        bpy.context.active_object.data.materials.append(mat_honey_drip)

    # Stinger jet thrusters at rear
    for sx in [-0.2, 0.2]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.08, depth=0.35, location=(sx, 0.2, -0.65), rotation=(math.radians(90), 0, 0))
        bpy.context.active_object.data.materials.append(mat_bee_black)

    # DRIVER: King Bee
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.32, location=(0, 0.58, -0.05), scale=(0.95, 1.1, 0.95))
    bpy.context.active_object.data.materials.append(mat_bee_yellow)

    # Black bee stripes
    bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=0.15, location=(0, 0.58, -0.05))
    bpy.context.active_object.data.materials.append(mat_bee_black)

    # Translucent buzzing wings
    for wx, roty in [(-0.25, -30), (0.25, 30)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, 0.85, -0.2), scale=(0.35, 0.02, 0.55), rotation=(math.radians(35), math.radians(roty), 0))
        bpy.context.active_object.data.materials.append(mat_wings)

    # Royal Crown
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.14, vertices=6, location=(0, 0.98, -0.05))
    bpy.context.active_object.data.materials.append(mat_crown)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "KingBeeChassis"
    return base

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Generating all 10 Conker characters in: {root_dir}")

    karts = [
        ("conker", build_conker, "conker_chassis.obj"),
        ("berri", build_berri, "berri_chassis.obj"),
        ("panther", build_panther, "panther_chassis.obj"),
        ("mighty_poo", build_mighty_poo, "mighty_poo_chassis.obj"),
        ("von_kriplespac", build_von_kriplespac, "kriplespac_chassis.obj"),
        ("gregg", build_gregg, "gregg_chassis.obj"),
        ("tediz", build_tediz, "tediz_chassis.obj"),
        ("buga", build_buga, "buga_chassis.obj"),
        ("franky", build_franky, "franky_chassis.obj"),
        ("king_bee", build_king_bee, "king_bee_chassis.obj")
    ]

    for kart_id, builder_fn, obj_name in karts:
        kart_dir = os.path.join(root_dir, "karts", kart_id)
        os.makedirs(kart_dir, exist_ok=True)
        # Build & Export wheel
        wheel = build_wheel()
        export_obj(wheel, os.path.join(kart_dir, "wheel.obj"))
        export_spm_mesh(wheel, os.path.join(kart_dir, "wheel.spm"))
        # Build & Export character chassis
        chassis = builder_fn()
        export_obj(chassis, os.path.join(kart_dir, obj_name))
        spm_name = obj_name.replace(".obj", ".spm")
        export_spm_mesh(chassis, os.path.join(kart_dir, spm_name))

    print("ALL 10 CHARACTERS GENERATED IN BLENDER SUCCESSFULLY!")

if __name__ == "__main__":
    main()
