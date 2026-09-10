#!/usr/bin/env python3
"""
Procedural 3D Model Generator for Conker-Kart using Blender (bpy).
Generates chassis, wheels, and drivers for:
1. Conker Nitro Rod (karts/conker/)
2. Berri Pink Fury (karts/berri/)
3. Panther Heavy King (karts/panther/)
"""

import sys
import os
import math

try:
    import bpy
    import bmesh
except ImportError:
    print("Error: This script must be run inside Blender: blender --background --python generate_models.py")
    sys.exit(1)

def clear_scene():
    """Wipes all existing objects, meshes, materials from the scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, diffuse_color, roughness=0.4, metallic=0.0):
    """Creates a simple principled BSDF material with specified color."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = diffuse_color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
    return mat

def build_wheel():
    """Builds a high-detail kart wheel centered at origin."""
    clear_scene()
    
    mat_tire = create_material("WheelTire", (0.1, 0.1, 0.12, 1.0), roughness=0.8)
    mat_rim = create_material("WheelRim", (0.9, 0.75, 0.1, 1.0), roughness=0.3, metallic=0.8)
    mat_hub = create_material("WheelHub", (0.8, 0.1, 0.1, 1.0), roughness=0.4)
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.28, depth=0.22, vertices=24, location=(0, 0, 0), rotation=(0, math.pi/2, 0)
    )
    tire = bpy.context.active_object
    tire.name = "Tire"
    tire.data.materials.append(mat_tire)
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.18, depth=0.23, vertices=24, location=(0, 0, 0), rotation=(0, math.pi/2, 0)
    )
    rim = bpy.context.active_object
    rim.name = "Rim"
    rim.data.materials.append(mat_rim)
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.07, depth=0.25, vertices=16, location=(0, 0, 0), rotation=(0, math.pi/2, 0)
    )
    hub = bpy.context.active_object
    hub.name = "Hub"
    hub.data.materials.append(mat_hub)
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = tire
    bpy.ops.object.join()
    tire.name = "KartWheel"
    return tire

def build_conker_kart():
    """Builds Conker's Nitro Rod kart chassis and driver."""
    clear_scene()
    
    mat_body_red = create_material("ConkerRed", (0.85, 0.1, 0.05, 1.0), roughness=0.3)
    mat_body_yellow = create_material("ConkerYellow", (1.0, 0.8, 0.05, 1.0), roughness=0.3)
    mat_metal = create_material("ChromeExhaust", (0.8, 0.8, 0.85, 1.0), roughness=0.15, metallic=0.9)
    mat_seat = create_material("SeatBlack", (0.15, 0.15, 0.18, 1.0), roughness=0.7)
    mat_fur_orange = create_material("SquirrelFur", (0.92, 0.42, 0.08, 1.0), roughness=0.9)
    mat_hoodie_blue = create_material("ConkerHoodie", (0.08, 0.35, 0.85, 1.0), roughness=0.6)
    mat_helmet_leather = create_material("AviatorLeather", (0.35, 0.2, 0.1, 1.0), roughness=0.5)
    mat_goggles_glass = create_material("GogglesLens", (0.2, 0.8, 0.95, 1.0), roughness=0.1, metallic=0.5)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.15, 0), scale=(0.85, 0.12, 1.4))
    base = bpy.context.active_object
    base.data.materials.append(mat_seat)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.28, 0.65), scale=(0.7, 0.18, 0.7))
    nose = bpy.context.active_object
    nose.data.materials.append(mat_body_red)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.38, 0.65), scale=(0.2, 0.02, 0.72))
    stripe = bpy.context.active_object
    stripe.data.materials.append(mat_body_yellow)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.42, 0.22, 0), scale=(0.25, 0.15, 0.8))
    pod_r = bpy.context.active_object
    pod_r.data.materials.append(mat_body_red)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.42, 0.22, 0), scale=(0.25, 0.15, 0.8))
    pod_l = bpy.context.active_object
    pod_l.data.materials.append(mat_body_red)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.45, -0.3), scale=(0.45, 0.5, 0.12), rotation=(math.radians(-15), 0, 0))
    seat_back = bpy.context.active_object
    seat_back.data.materials.append(mat_seat)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.4, location=(0, 0.42, 0.15), rotation=(math.radians(45), 0, 0))
    col = bpy.context.active_object
    col.data.materials.append(mat_metal)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.025, location=(0, 0.55, 0.02), rotation=(math.radians(45), 0, 0))
    wheel = bpy.context.active_object
    wheel.data.materials.append(mat_seat)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.35, -0.65), scale=(0.45, 0.3, 0.3))
    engine = bpy.context.active_object
    engine.data.materials.append(mat_metal)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.45, location=(-0.22, 0.32, -0.85), rotation=(math.radians(90), 0, 0))
    ex_l = bpy.context.active_object
    ex_l.data.materials.append(mat_metal)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.45, location=(0.22, 0.32, -0.85), rotation=(math.radians(90), 0, 0))
    ex_r = bpy.context.active_object
    ex_r.data.materials.append(mat_metal)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.72, -0.75), scale=(0.95, 0.05, 0.25))
    wing = bpy.context.active_object
    wing.data.materials.append(mat_body_yellow)

    for sx in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.35, location=(sx, 0.55, -0.72))
        strut = bpy.context.active_object
        strut.data.materials.append(mat_metal)

    # Driver: Conker
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.52, -0.15), scale=(0.35, 0.35, 0.3))
    torso = bpy.context.active_object
    torso.data.materials.append(mat_hoodie_blue)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(0, 0.85, -0.12))
    head = bpy.context.active_object
    head.data.materials.append(mat_fur_orange)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0.8, 0.08), scale=(0.9, 0.7, 1.2))
    snout = bpy.context.active_object
    snout.data.materials.append(mat_fur_orange)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.235, location=(0, 0.88, -0.14), scale=(1.02, 1.0, 0.95))
    helmet = bpy.context.active_object
    helmet.data.materials.append(mat_helmet_leather)

    for gx in [-0.09, 0.09]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.04, location=(gx, 0.92, 0.04), rotation=(math.radians(75), 0, 0))
        gog = bpy.context.active_object
        gog.data.materials.append(mat_goggles_glass)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0, 0.65, -0.55), scale=(0.7, 1.4, 0.9), rotation=(math.radians(35), 0, 0))
    tail = bpy.context.active_object
    tail.data.materials.append(mat_fur_orange)

    for ax, rot in [(-0.16, -20), (0.16, 20)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.35, location=(ax, 0.52, -0.02), rotation=(math.radians(50), 0, math.radians(rot)))
        arm = bpy.context.active_object
        arm.data.materials.append(mat_hoodie_blue)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "ConkerChassis"
    return base

def build_berri_kart():
    """Builds Berri's Pink Fury kart chassis and driver."""
    clear_scene()
    
    mat_pink = create_material("BerriPink", (0.95, 0.25, 0.6, 1.0), roughness=0.25)
    mat_white = create_material("BerriWhite", (0.95, 0.95, 0.95, 1.0), roughness=0.3)
    mat_chrome = create_material("BerriChrome", (0.85, 0.85, 0.9, 1.0), roughness=0.1, metallic=0.95)
    mat_driver_pink = create_material("BerriOutfit", (0.9, 0.15, 0.5, 1.0), roughness=0.4)
    mat_driver_fur = create_material("BerriFur", (0.95, 0.9, 0.85, 1.0), roughness=0.8)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.15, 0), scale=(0.8, 0.12, 1.35))
    base = bpy.context.active_object
    base.data.materials.append(mat_pink)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.8, location=(0, 0.25, 0.6), rotation=(math.radians(90), 0, 0), scale=(0.9, 0.45, 1.0))
    nose = bpy.context.active_object
    nose.data.materials.append(mat_white)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.68, -0.7), scale=(0.9, 0.04, 0.22))
    spoiler = bpy.context.active_object
    spoiler.data.materials.append(mat_pink)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(0, 0.82, -0.1))
    head = bpy.context.active_object
    head.data.materials.append(mat_driver_fur)

    for ex in [-0.09, 0.09]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.4, location=(ex, 1.15, -0.1), scale=(0.6, 1.0, 1.0), rotation=(math.radians(-10), 0, 0))
        ear = bpy.context.active_object
        ear.data.materials.append(mat_pink)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.5, -0.12), scale=(0.32, 0.32, 0.28))
    torso = bpy.context.active_object
    torso.data.materials.append(mat_driver_pink)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "BerriChassis"
    return base

def build_panther_kart():
    """Builds Panther King's Heavy Tank kart chassis and driver."""
    clear_scene()
    
    mat_gold = create_material("PantherGold", (0.85, 0.65, 0.15, 1.0), roughness=0.3, metallic=0.7)
    mat_armor_dark = create_material("PantherDarkArmor", (0.15, 0.15, 0.18, 1.0), roughness=0.6, metallic=0.5)
    mat_panther_fur = create_material("PantherFur", (0.1, 0.1, 0.12, 1.0), roughness=0.9)
    mat_cape_red = create_material("PantherCape", (0.8, 0.05, 0.1, 1.0), roughness=0.6)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.2, 0), scale=(0.95, 0.22, 1.5))
    base = bpy.context.active_object
    base.data.materials.append(mat_armor_dark)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.25, 0.75), scale=(1.05, 0.2, 0.25))
    ram = bpy.context.active_object
    ram.data.materials.append(mat_gold)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0, 0.9, -0.15))
    head = bpy.context.active_object
    head.data.materials.append(mat_panther_fur)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.18, vertices=8, location=(0, 1.18, -0.15))
    crown = bpy.context.active_object
    crown.data.materials.append(mat_gold)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.55, -0.45), scale=(0.6, 0.5, 0.08), rotation=(math.radians(20), 0, 0))
    cape = bpy.context.active_object
    cape.data.materials.append(mat_cape_red)

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    base.name = "PantherChassis"
    return base

def export_obj(obj, filepath):
    """Exports active object to OBJ."""
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

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Generating kart 3D assets in: {root_dir}")

    # 1. Generate Shared Wheel
    wheel = build_wheel()
    for kart_name in ["conker", "berri", "panther"]:
        kart_dir = os.path.join(root_dir, "karts", kart_name)
        export_obj(wheel, os.path.join(kart_dir, "wheel.obj"))

    # 2. Conker Kart
    conker = build_conker_kart()
    export_obj(conker, os.path.join(root_dir, "karts", "conker", "conker_chassis.obj"))

    # 3. Berri Kart
    berri = build_berri_kart()
    export_obj(berri, os.path.join(root_dir, "karts", "berri", "berri_chassis.obj"))

    # 4. Panther Kart
    panther = build_panther_kart()
    export_obj(panther, os.path.join(root_dir, "karts", "panther", "panther_chassis.obj"))

    print("SUCCESS: All 3D assets generated successfully!")

if __name__ == "__main__":
    main()
