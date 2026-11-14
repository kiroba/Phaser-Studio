# Crown — procedural low-poly build (Blender primitives + bevels).
# The reference head-socket cosmetic: a gold band with eight points
# (alternating tall/short), orb tips on the tall points, and band gems
# — violet at the front (the first Halo's colour), teal and rose at the
# sides. Radially symmetric except for the gems; front is -Y.
#
#   blender --background --python build_crown.py -- --pack <pack_dir>
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

def cyl(name, loc, radius, depth, material, bevel=0.006, vertices=24, flat=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel, flat)

def cone(name, loc, r1, r2, depth, material, bevel=0.004, vertices=4, flat=True, rot_z=0.0):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth,
                                    location=loc, rotation=(0, 0, rot_z))
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel, flat)

def sphere(name, loc, radius, material, seg=12, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=radius, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, False)

def gem(name, loc, radius, material):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, True)

def torus(name, loc, major, minor, material):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=28, minor_segments=10, location=loc)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, 0.0, False)

# --- palette: two golds + three gem colours ---
gold = mat("gold", (0.83, 0.62, 0.18), rough=0.32, metal=1.0)
gold_dark = mat("gold_dark", (0.60, 0.43, 0.12), rough=0.42, metal=1.0)
gem_violet = mat("gem_violet", (0.30, 0.20, 0.65), rough=0.15, metal=0.1,
                 emission=(0.42, 0.30, 0.96), estr=0.7)
gem_teal = mat("gem_teal", (0.05, 0.45, 0.40), rough=0.15, metal=0.1,
               emission=(0.10, 0.75, 0.65), estr=0.5)
gem_rose = mat("gem_rose", (0.60, 0.12, 0.25), rough=0.15, metal=0.1,
               emission=(0.95, 0.25, 0.45), estr=0.5)

BAND_R = 0.30
BAND_H = 0.14
BAND_Z = BAND_H / 2  # band spans z 0 .. 0.14

# --- band + rims ---
cyl("band", (0, 0, BAND_Z), BAND_R, BAND_H, gold, vertices=28)
cyl("band_inner_shade", (0, 0, BAND_Z), BAND_R - 0.018, BAND_H - 0.02, gold_dark, bevel=0.0, vertices=28)
torus("rim_top", (0, 0, BAND_H - 0.01), BAND_R, 0.016, gold)
torus("rim_bottom", (0, 0, 0.01), BAND_R, 0.016, gold)

# --- eight points, alternating tall / short, orbs on the tall ones ---
for i in range(8):
    ang = math.radians(i * 45.0)
    x, y = BAND_R * 0.94 * math.sin(ang), -BAND_R * 0.94 * math.cos(ang)
    tall = (i % 2 == 0)
    h = 0.27 if tall else 0.15
    cone(f"point_{i}", (x, y, BAND_H - 0.02 + h / 2), 0.070, 0.004, h,
         gold if tall else gold_dark, rot_z=ang + math.pi / 4)
    if tall:
        sphere(f"orb_{i}", (x, y, BAND_H - 0.02 + h + 0.018), 0.030, gold)

# --- band gems: violet front-centre (-Y), teal / rose alternating around ---
gem_specs = [
    (0.0, 0.055, gem_violet, "gem_front"),
    (-42.0, 0.040, gem_teal, "gem_l_teal"),
    (42.0, 0.040, gem_teal, "gem_r_teal"),
    (-84.0, 0.040, gem_rose, "gem_l_rose"),
    (84.0, 0.040, gem_rose, "gem_r_rose"),
    (180.0, 0.040, gem_violet, "gem_back"),
]
for deg, r, material, name in gem_specs:
    ang = math.radians(deg)
    # Set INTO the band: centre sits inside the band wall so roughly
    # the outer third of the stone shows.
    rr = BAND_R - r * 0.45
    x, y = rr * math.sin(ang), -rr * math.cos(ang)
    gem(name, (x, y, BAND_Z), r, material)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PACK, "master.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(PACK, "master.glb"),
                          export_format='GLB', export_apply=True)
print("BUILD: master.glb", os.path.getsize(os.path.join(PACK, "master.glb")), "bytes")
print("BUILD: DONE crown-01")
