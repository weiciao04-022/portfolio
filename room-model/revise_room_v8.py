import bpy,ast,math,os
from mathutils import Vector
from pathlib import Path
OUT='/private/tmp/katy-room-v8';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','cube','sphere','cyl','rod','curve','ring','mesh']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base=bpy.data.collections['00 • Architecture'];collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};current=base
cream=bpy.data.materials['Wardrobe warm ivory paint'];trim=bpy.data.materials['Painted moulding · porcelain'];walnut=bpy.data.materials['Walnut furniture'];gold=bpy.data.materials['Aged brass'];paper=bpy.data.materials['Document paper']
scene=bpy.context.scene;scene.frame_set(1)
# Replace the high wardrobe and garment placeholders with a low certificate cabinet.
for ob in list(bpy.data.objects):
 if ob.name.startswith('Wardrobe'):bpy.data.objects.remove(ob,do_unlink=True)
collections['04'].name='04 • Certificate cabinet';group('04')
wx=-1.59;wy=2.54;width=2.03;top=1.10
for x in [wx-.977,wx+.977]:cube('Certificate cabinet side',(x,wy,.59),(.075,.66,.93),cream,.016)
cube('Certificate cabinet back',(wx,2.84,.59),(1.93,.055,.93),cream,.012)
cube('Certificate cabinet bottom',(wx,wy,.17),(1.93,.63,.065),cream,.010)
cube('Certificate cabinet plinth',(wx,wy,.105),(2.10,.71,.14),trim,.02)
cube('Certificate cabinet tabletop',(wx,wy,top-.038),(2.15,.76,.076),walnut,.026)
cube('Certificate cabinet top trim',(wx,wy,1.00),(2.10,.70,.062),trim,.015)
cube('Certificate cabinet internal shelf',(wx,wy,.54),(1.91,.56,.043),trim,.009)
# Neutral folders inside, with no invented certificate text.
folder=bpy.data.materials['Book cloth 0']
for side in [-1,1]:
 for k in range(3):cube('Cabinet document folder',(wx+side*.46,2.53,.22+k*.062),(.63,.36,.052),[folder,paper,cream][k],.006)
hinges={};door_parts={-1:[],1:[]}
for side,label in [(-1,'Left'),(1,'Right')]:
 x=wx+side*.499
 door_parts[side].append(cube('Cabinet door '+label,(x,2.183,.58),(.973,.049,.79),cream,.016))
 for offset,r in [(0,.012),(.026,.006)]:
  w=.77-offset*2;z0=.28+offset;z1=.88-offset
  door_parts[side].append(curve('Cabinet door panel '+label,[(x-w/2,2.146,z0),(x+w/2,2.146,z0),(x+w/2,2.146,z1),(x-w/2,2.146,z1)],r,trim,True))
 hx=wx+side*.073
 door_parts[side].append(rod('Cabinet brass handle '+label,(hx,2.112,.52),(hx,2.112,.68),.012,gold))
 for z in [.52,.68]:door_parts[side].append(rod('Cabinet handle mount '+label,(hx,2.17,z),(hx,2.112,z),.007,gold))
 hinge=bpy.data.objects.new('CabinetDoor_'+label+'_Hinge',None);current.objects.link(hinge);hinge.location=(wx+side*.986,2.183,.58);hinge.empty_display_type='PLAIN_AXES';hinge.empty_display_size=.10;hinges[side]=hinge
bpy.context.view_layer.update()
for side,hinge in hinges.items():
 for ob in door_parts[side]:
  world=ob.matrix_world.copy();ob.parent=hinge;ob.matrix_parent_inverse=hinge.matrix_world.inverted();ob.matrix_basis=world
 for frame,angle in [(1,0),(40,side*105),(80,0)]:
  hinge.rotation_euler.z=math.radians(angle);hinge.keyframe_insert(data_path='rotation_euler',index=2,frame=frame)
 hinge.animation_data.action.name='CertificateCabinet_'+('Left' if side<0 else 'Right')+'_OpenClose'

# Three removable frame objects: a graduation certificate and two internship placeholders.
# Visible sheets stay blank until actual images are supplied.
def certificate(name,x,y,w,h,material):
 parent=bpy.data.objects.new(name,None);current.objects.link(parent);parent.location=(x,y,top+h/2+.014);parent.rotation_euler.x=-.10
 def add(ob):ob.parent=parent;return ob
 add(cube(name+' frame back',(0,0,0),(w,.035,h),walnut,.006))
 for xx in [-w/2+.012,w/2-.012]:add(cube(name+' frame vertical',(xx,-.027,0),(.024,.029,h),material,.005))
 for zz in [-h/2+.012,h/2-.012]:add(cube(name+' frame horizontal',(0,-.027,zz),(w-.04,.029,.024),material,.005))
 add(cube(name+' blank mat',(0,-.021,0),(w-.05,.003,h-.05),trim,.003))
 add(cube(name+' certificate image placeholder',(0,-.025,0),(w-.10,.002,h-.10),paper,.001))
 parent['Content']='Blank placeholder. Replace with an authentic supplied certificate image.'
 parent['Interaction']='Select / lift certificate frame; content not yet added'
 rod(name+' rear stand',(x,y+.055,top+h*.52),(x,y+.23,top+.015),.008,walnut)
 return parent
certificate('Certificate_Graduation',wx-.61,2.40,.65,.45,gold)
certificate('Certificate_Internship_01',wx+.025,2.41,.44,.55,walnut)
certificate('Certificate_Internship_02',wx+.565,2.43,.43,.53,gold)

# Verify full door sweep against the curtains and duvet before saving.
def points(ob,deps):
 e=ob.evaluated_get(deps)
 if ob.type=='CURVE':
  m=e.to_mesh();p=[e.matrix_world@v.co for v in m.vertices];e.to_mesh_clear();return p
 return [e.matrix_world@Vector(c) for c in e.bound_box]
curtains=[o for o in bpy.data.objects if o.name.startswith('Full-length gathered curtain')];bed=bpy.data.objects['Fluffy silk duvet — refined fabric']
gap=float('inf')
for frame in range(1,81):
 scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 clearance=min(v.x for o in door_parts[-1] for v in points(o,deps))-max(v.x for o in curtains for v in points(o,deps))
 assert clearance>.08,(frame,clearance)
 assert min(v.x for v in points(bed,deps))-max(v.x for o in door_parts[1] for v in points(o,deps))>.05
 gap=min(gap,clearance)
print('VERIFIED_LOW_CABINET', 'height',top,'m','3 blank certificate frames','80 animation frames clear','curtain gap',round(gap,3),'m')
scene['Revision']='v8 — low paneled cabinet with blank graduation/internship certificate frames; opening animation retained'
scene['Certificate notes']='Three blank frames only; no claim of issued certificates or qualifications. Await actual images.'
scene['Animation instructions']='Frame 1 closed; frame 40 open; frame 80 closed. CabinetDoor_Left_Hinge and CabinetDoor_Right_Hinge.'
scene.frame_set(1);scene.camera=bpy.data.objects['Camera • Room overview'];scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
scene.render.resolution_x=1200;scene.render.resolution_y=960;scene.cycles.samples=48
bpy.ops.render.render(write_still=True)
scene.frame_set(40);scene.render.filepath=OUT+'/Katy_Cabinet_Open_Preview.png';bpy.ops.render.render(write_still=True)
print('V8_COMPLETE')
