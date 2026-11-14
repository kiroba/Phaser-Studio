# Relay spire — procedural low-poly build (Blender primitives + bevels).
# A small Omniverse node tower / plaza landmark: stacked base, tapered
# shaft, lavender collar bands, an emissive violet orb in a cradle ring,
# and an antenna mast with a glowing tip.
#
#   blender --background --python build_relay_spire.py -- --pack <pack_dir>
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

def mat(name, color, rough=0.6, metal=0.0, emission=None, estr=0.0):
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

def box(name, loc, dims, material, bevel=0.02, flat=False):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, material, bevel, flat)

def cyl(name, loc, radius, depth, material, bevel=0.012, vertices=24, flat=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel, flat)

def cone(name, loc, r1, r2, depth, material, bevel=0.01, vertices=24, rot=(0, 0, 0), flat=False):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel, flat)

def sphere(name, loc, radius, material, scale=(1, 1, 1), seg=20, rings=14, flat=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=radius, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, material, 0.0, flat)

def torus(name, loc, major, minor, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=28, minor_segments=10, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, False)

# --- palette: graphite + lavender Omniverse metals, violet glow ---
stone = mat("stone", (0.23, 0.25, 0.30), rough=0.85, metal=0.0)
metal = mat("shaft_metal", (0.36, 0.39, 0.47), rough=0.35, metal=0.85)
band = mat("lavender_band", (0.52, 0.46, 0.78), rough=0.40, metal=0.60)
orb_mat = mat("orb", (0.25, 0.12, 0.45), rough=0.30, metal=0.0, emission=(0.62, 0.35, 1.0), estr=3.2)
tip_mat = mat("tip", (0.25, 0.12, 0.45), rough=0.30, metal=0.0, emission=(0.62, 0.35, 1.0), estr=2.2)

# --- stacked base ---
cyl("base_disc", (0, 0, 0.09), 0.88, 0.18, stone, bevel=0.02, vertices=28)
box("plinth", (0, 0, 0.30), (1.20, 1.20, 0.24), stone, bevel=0.03)
cyl("step", (0, 0, 0.50), 0.60, 0.16, stone, bevel=0.02, vertices=28)
# --- tapered shaft + collar bands ---
cone("shaft", (0, 0, 1.63), 0.47, 0.30, 2.10, metal, bevel=0.015, vertices=28)
cyl("band_low", (0, 0, 1.10), 0.45, 0.09, band, bevel=0.01, vertices=28)
cyl("band_high", (0, 0, 2.20), 0.365, 0.09, band, bevel=0.01, vertices=28)
# --- crown, cradle ring, orb, mast, tip ---
cyl("crown", (0, 0, 2.78), 0.40, 0.20, metal, bevel=0.015, vertices=28)
torus("cradle_ring", (0, 0, 3.30), 0.30, 0.035, band)
sphere("orb", (0, 0, 3.38), 0.27, orb_mat, seg=24, rings=16)
cyl("mast", (0, 0, 3.655), 0.028, 1.55, metal, bevel=0.0, vertices=12)
sphere("mast_tip", (0, 0, 4.47), 0.06, tip_mat, seg=14, rings=10)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PACK, "master.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(PACK, "master.glb"),
                          export_format='GLB', export_apply=True)
print("BUILD: master.glb", os.path.getsize(os.path.join(PACK, "master.glb")), "bytes")
print("BUILD: DONE relay-spire-01")
