import bpy,ast,random,os
from math import sin,cos,pi
from mathutils import Vector
from pathlib import Path

OUT='/private/tmp/katy-room-v4';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','mesh']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base=bpy.data.collections['00 • Architecture'];collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};current=base

# Widen the room by 1.6 m. Existing furniture retains its proportions.
o=bpy.data.objects['Floor foundation'];o.location.x=1.45;o.dimensions.x=10.05
o=bpy.data.objects['Back plaster wall'];o.location.x=1.45;o.dimensions.x=10.05
for o in bpy.data.objects:
 if o.name.startswith('Back skirting / cornice'):o.location.x=1.45;o.dimensions.x=9.90
for o in collections['01'].objects[:]:bpy.data.objects.remove(o,do_unlink=True)
floor_code=src.split('# Individually editable, clipped herringbone oak blocks.')[1].split('# French window, sheer curtains')[0]
floor_code=floor_code.replace('range(-20,21)','range(-40,41)').replace('(0,3.48,True)','(0,6.38,True)').replace('(1,-2.98,False)','(1,-4.38,False)')
random.seed(22);exec(floor_code)

# Remove every potted plant, including the small bookcase plant.
for o in collections['08'].objects[:]:bpy.data.objects.remove(o,do_unlink=True)

# Move desk and chair together 0.8 m inward, keeping the outward-facing direction.
for o in collections['06'].objects:
 if o.parent is None:o.location.x+=.80
# Shift the sleep and lounge zones to make space for the inward desk position.
for o in collections['03'].objects:
 if o.parent is None:o.location.x+=.75
for o in collections['05'].objects:
 if o.parent is None:o.location.x+=1.60
for o in collections['11'].objects:
 if o.parent is None:o.location.x+=1.60
for o in collections['07'].objects:
 if o.parent is None:o.location.x+=.75
# Lamps remain aligned with the moved bedside table; chandelier follows the room centre.
for o in collections['09'].objects:
 if o.name.startswith(('Table lamp','Pleated table lamp','Bedside warm glow')):o.location.x+=.75
 if o.name.startswith(('Chandelier','Candle brass','Crystal drop','Ceiling rose')):o.location.x+=.70
for o in base.objects:
 if o.name.startswith(('Art gold','Art paper','Abstract art')):o.location.x+=.75
 if o.name.startswith('Expanded wall moulding'):o.location.x+=1.60
 if o.name.startswith('French wall panel'):
  coords=[p.co.x for spl in o.data.splines for p in spl.points]
  if coords:
   centre=(min(coords)+max(coords))/2
   if -.5<centre<1:o.location.x+=.75
   elif centre>1:o.location.x+=1.60

scene=bpy.context.scene
cam=bpy.data.objects['Camera • Room overview'];cam.location=(13.5,-16.5,12);target=Vector((1.30,-.40,1.15));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=15.1;scene.camera=cam
cam=bpy.data.objects['Camera • Silk bed detail'];cam.location.x+=.75
cam=bpy.data.objects['Camera • Bookshelf detail'];cam.location.x+=1.6
scene['Revision']='v4 — room widened to 9.9 m, desk/seat moved 0.8 m inward, all potted plants removed'
scene['Room dimensions']='9.9 m x 7.4 m; open-front cutaway'
scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
bpy.ops.render.render(write_still=True)
print('V4_ROOM_COMPLETE')
