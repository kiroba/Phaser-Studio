# Plaza lantern — procedural low-poly build (Blender primitives + bevels).
# Iron post on a stepped base, a framed lamp head with a warm emissive
# core, a cone cap, finial ball and hanging ring.
#
#   blender --background --python build_lantern.py -- --pack <pack_dir>
#
# Saves master.blend + exports master.glb into the pack dir.
# Original procedural geometry, no third-party assets — CC0 by construction.
import bpy, math, os, sys

argv = sys.argv[sys.argv.index("--") + 1:]
def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default
PACK = os.path.abspath(arg("--pack"))
os.makedirs(os.path.join(PACK, "sprites"), exist_ok=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def mat(name, color, rough=0.5, metal=0.7, emission=None, estr=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emission is not None:
        b.inputs["Emission Color"].default_value = (*emission, 1.0)
        b.inputs["Emission Strength"].default_value = estr
    return m

def _finish(o, material, bevel, flat):
    if material is not None:
        o.data.materials.append(material)
    if flat:
        for p in o.data.polygons: p.use_smooth = False
    if bevel > 0:
        mod = o.modifiers.new("bev", 'BEVEL'); mod.width = bevel; mod.segments = 2
        bpy.context.view_layer.objects.active = o
        try: bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception as e: print("BEVEL apply failed:", o.name, e)
    return o

def box(name, loc, dims, material, bevel=0.01, flat=False):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, material, bevel, flat)

def cyl(name, loc, radius, depth, material, bevel=0.008, vertices=18, flat=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel, flat)

def cone(name, loc, r1, r2, depth, material, bevel=0.008, vertices=20, flat=False):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel, flat)

def sphere(name, loc, radius, material, seg=14, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=radius, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, False)

def torus(name, loc, major, minor, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=24, minor_segments=10, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, False)

# --- palette: dark iron, lighter cap, warm amber glow ---
iron = mat("iron", (0.13, 0.13, 0.15), rough=0.50, metal=0.70)
iron_light = mat("iron_light", (0.22, 0.23, 0.27), rough=0.45, metal=0.70)
glow = mat("lamp_core", (0.45, 0.25, 0.08), rough=0.40, metal=0.0, emission=(1.0, 0.60, 0.22), estr=3.0)

# --- stepped base + post + collar ---
cyl("base", (0, 0, 0.045), 0.17, 0.09, iron, vertices=20)
cyl("base_step", (0, 0, 0.14), 0.11, 0.10, iron, vertices=20)
cyl("post", (0, 0, 0.90), 0.045, 1.42, iron, bevel=0.0, vertices=14)
torus("collar", (0, 0, 1.52), 0.065, 0.018, iron_light)
# --- lamp head: plates, emissive core, four frame posts ---
box("lamp_bottom", (0, 0, 1.635), (0.36, 0.36, 0.05), iron, bevel=0.01)
cyl("core", (0, 0, 1.85), 0.105, 0.34, glow, bevel=0.0, vertices=18)
for sx in (-1, 1):
    for sy in (-1, 1):
        box(f"frame_{sx}_{sy}", (0.15 * sx, 0.15 * sy, 1.86), (0.04, 0.04, 0.44), iron, bevel=0.008)
box("lamp_top", (0, 0, 2.105), (0.38, 0.38, 0.05), iron, bevel=0.01)
# --- cap, finial, hanging ring ---
cone("cap", (0, 0, 2.24), 0.30, 0.03, 0.22, iron_light, vertices=20)
sphere("finial", (0, 0, 2.385), 0.035, iron_light)
torus("ring", (0, 0, 2.47), 0.07, 0.016, iron, rot=(math.pi / 2, 0, 0))

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PACK, "master.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(PACK, "master.glb"),
                          export_format='GLB', export_apply=True)
print("BUILD: master.glb", os.path.getsize(os.path.join(PACK, "master.glb")), "bytes")
print("BUILD: DONE lantern-01")
