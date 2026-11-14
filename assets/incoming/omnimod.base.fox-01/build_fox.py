# Fox — procedural low-poly build (Blender primitives, flat-shaded).
# Body from a bevelled box, sphere head, cone ears, cream muzzle, and a
# big two-tone tail. Built facing -Y. Charming at 128px beats realistic.
#
#   blender --background --python build_fox.py -- --pack <pack_dir>
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

def mat(name, color, rough=0.8, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
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

def box(name, loc, dims, material, bevel=0.02, flat=True):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, material, bevel, flat)

def cyl(name, loc, radius, depth, material, vertices=10, flat=True):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, flat)

def cone(name, loc, r1, r2, depth, material, vertices=12, rot=(0, 0, 0), flat=True):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, flat)

def sphere(name, loc, radius, material, scale=(1, 1, 1), seg=14, rings=10, flat=True):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=radius, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, material, 0.0, flat)

# --- palette ---
orange = mat("fox_orange", (0.85, 0.42, 0.15), rough=0.85)
orange_dark = mat("fox_orange_dark", (0.72, 0.33, 0.11), rough=0.85)
cream = mat("fox_cream", (0.96, 0.90, 0.78), rough=0.85)
dark = mat("fox_dark", (0.16, 0.10, 0.08), rough=0.50)
eye_mat = mat("fox_eye", (0.05, 0.04, 0.04), rough=0.25)

# --- legs + paws ---
for sx in (-1, 1):
    for sy in (-1, 1):
        cyl(f"leg_{sx}_{sy}", (0.15 * sx, 0.24 * sy, 0.18), 0.05, 0.36, orange_dark)
        box(f"paw_{sx}_{sy}", (0.15 * sx, 0.25 * sy, 0.04), (0.12, 0.17, 0.08), dark, bevel=0.02)
# --- body ---
box("body", (0, 0.02, 0.55), (0.44, 0.80, 0.42), orange, bevel=0.12)
# --- head: sphere + cream muzzle + nose + eyes + cone ears ---
sphere("head", (0, -0.55, 0.74), 0.215, orange, scale=(1.0, 0.92, 0.88))
box("muzzle", (0, -0.705, 0.655), (0.22, 0.20, 0.15), cream, bevel=0.06)
sphere("nose", (0, -0.80, 0.685), 0.048, dark, scale=(1.15, 0.7, 0.7), seg=10, rings=8)
sphere("eye_l", (-0.095, -0.705, 0.815), 0.030, eye_mat, seg=10, rings=8)
sphere("eye_r", (0.095, -0.705, 0.815), 0.030, eye_mat, seg=10, rings=8)
cone("ear_l", (-0.115, -0.50, 0.96), 0.095, 0.012, 0.24, orange, rot=(0.08, -0.20, 0))
cone("ear_r", (0.115, -0.50, 0.96), 0.095, 0.012, 0.24, orange, rot=(0.08, 0.20, 0))
# --- big tail: orange base cone swept up-back + cream tip ---
cone("tail_base", (0, 0.47, 0.60), 0.145, 0.06, 0.52, orange, rot=(-0.85, 0, 0))
cone("tail_tip", (0, 0.740, 0.838), 0.078, 0.014, 0.30, cream, rot=(-0.85, 0, 0))

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PACK, "master.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(PACK, "master.glb"),
                          export_format='GLB', export_apply=True)
print("BUILD: master.glb", os.path.getsize(os.path.join(PACK, "master.glb")), "bytes")
print("BUILD: DONE fox-01")
