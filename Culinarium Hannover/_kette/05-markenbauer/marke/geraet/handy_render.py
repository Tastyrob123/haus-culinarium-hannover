# Culinarium Hannover, Markenbuch Station 05 (26.10.2026), übernommen vom Markenbuch Monte-Moro: Gehäuse dunkel wie das Schiefer-Violett, Kantenlicht Kerze und Orange. Ursprung Monte-Moro (17.10.2026), übernommen aus der Potentialanalyse (Robert 17.10.2026, Master 1b Nr. 16): Aufnahme als Bildschirm-Textur auf dem iPhone-Modell, leicht gedreht,
# Kantenlicht in Lärche und Logo-Blau, freigestellt. Gerade von vorn (Robert 17.10.2026), der Schatten entsteht danach leise in geraet.py. Vorlage: Carlton _gast/handy/render.py.
# Zweiter Durchgang (wenige Samples) mit einer Marken-Textur: grünes Feld an der Stelle → Lage der Stelle im fertigen Bild für die Linie zur Lupe.
import bpy, math, sys, json, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
jobs = json.loads(open(argv[0]).read())
HDR = '/Applications/Blender.app/Contents/Resources/5.1/datafiles/studiolights/world/studio.exr'
GLB = '/Users/robertreff/Desktop/Website-Projekte/Tasty Webdesign Showcase/assets/3d/iphone.glb'

def setup(res):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type = 'METAL'; prefs.get_devices()
        for d in prefs.devices: d.use = True
        sc.cycles.device = 'GPU'
    except Exception as e: print('gpu', e)
    sc.render.film_transparent = True; sc.render.resolution_x, sc.render.resolution_y = res
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(HDR)
    bg = nt.nodes['Background']; bg.inputs['Strength'].default_value = 0.34; nt.links.new(env.outputs['Color'], bg.inputs['Color'])
    return sc

def phone(rot):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=GLB)
    o = [x for x in bpy.data.objects if x not in before and x.type == 'MESH'][0]
    schirm = []
    for i, m in enumerate(o.data.materials):
        if m.name.startswith('17ProMax_Screen') or any(n.type == 'TEX_IMAGE' and n.image and n.image.name.startswith('imagepaste') for n in (m.node_tree.nodes if m.node_tree else [])):
            nm = m.copy(); o.data.materials[i] = nm; schirm.append(nm)
            b = nm.node_tree.nodes['Principled BSDF']
            b.inputs['Emission Strength'].default_value = 1.1
            for l in list(b.inputs['Base Color'].links): nm.node_tree.links.remove(l)
            b.inputs['Base Color'].default_value = (0, 0, 0, 1); b.inputs['Roughness'].default_value = 0.25
            if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.0
        elif m.name.startswith('17ProMax_glass'):
            b = m.node_tree.nodes.get('Principled BSDF')
            if b:
                for k, v in (('Specular IOR Level', 0.03), ('Roughness', 0.05), ('Coat Weight', 0.0)):
                    if k in b.inputs: b.inputs[k].default_value = v
        elif m.name.startswith(('17ProMax_color', '17ProMax_Black', '17ProMax_black', '17ProMax_Logo')):
            b = m.node_tree.nodes.get('Principled BSDF')
            if b:
                b.inputs['Base Color'].default_value = (0.10, 0.095, 0.12, 1)   # Gehäuse dunkel, Schiefer
                b.inputs['Metallic'].default_value = 0.9; b.inputs['Roughness'].default_value = 0.3
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    o.rotation_mode = 'XYZ'; o.location = (0, 0, 0); o.rotation_euler = [math.radians(a) for a in rot]; o.select_set(False)
    return schirm

def bild(schirm, pfad):
    img = bpy.data.images.load(pfad)
    for nm in schirm:
        for n in nm.node_tree.nodes:
            if n.type == 'TEX_IMAGE': n.image = img

def light(name, loc, color, energy, size, target=(0, 0, 0)):
    L = bpy.data.lights.new(name, 'AREA'); L.energy = energy; L.color = color; L.size = size
    ob = bpy.data.objects.new(name, L); bpy.context.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(loc)).to_track_quat('-Z', 'Y').to_euler()

def camera(loc, lens):
    c = bpy.data.cameras.new('cam'); c.lens = lens
    ob = bpy.data.objects.new('cam', c); bpy.context.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (mathutils.Vector((0, 0, 0)) - mathutils.Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = ob

for J in jobs:
    sc = setup(tuple(J.get('res', (800, 1400))))
    schirm = phone(tuple(J.get('rot', (0, 0, 0))))   # Robert 17.10.2026: «die Telefone bitte gerade»
    # kein Schattenfänger mehr (Robert 17.10.2026: der Schatten «funktioniert so nicht»): der leise Schatten direkt hinter dem Gerät kommt in geraet.py dazu
    light('key', (-0.22, 0.42, 0.34), (1, 0.98, 0.95), J.get('key', 9), 0.35)
    light('fill', (0.3, 0.6, -0.1), (1, 1, 1), 2.5, 1.0)
    light('rimL', (-0.3, -0.25, 0.12), (1.0, 0.72, 0.36), 30, 0.3)
    light('rimR', (0.32, -0.25, 0.1), (0.94, 0.46, 0.29), 26, 0.3)
    camera((0.0, 0.42, 0.0), J.get('lens', 88))
    bild(schirm, J['screen']); sc.cycles.samples = J.get('samples', 56); sc.cycles.use_denoising = True
    sc.render.filepath = J['out']; bpy.ops.render.render(write_still=True)
    print('DONE', J['out'])
