import bpy,ast,math,os,json
from mathutils import Vector
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
OUT='/private/tmp/katy-room-animation';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','cube','sphere','cyl','rod','curve','ring','mesh']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
scene=bpy.context.scene;scene.frame_set(1)
base=bpy.data.collections['00 • Architecture'];collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};current=base
gold=bpy.data.materials['Aged brass'];paper=bpy.data.materials['Document paper'];navy=bpy.data.materials['Book cloth 0'];dark=bpy.data.materials['Dark iron']
# Disable the old independent cabinet loop so it cannot play accidentally during intro.
for name in ['CabinetDoor_Left_Hinge','CabinetDoor_Right_Hinge']:
 ob=bpy.data.objects[name]
 if ob.animation_data and ob.animation_data.action:ob.animation_data.action.use_fake_user=True
 ob.animation_data_clear();ob.rotation_euler.z=0

# A separately addressable smartphone for the requested contact shot.
group('06');phone=bpy.data.objects.new('Interactive_Phone',None);current.objects.link(phone);phone.location=(-1.65,-.47,.896)
def attach(ob,parent):ob.parent=parent;return ob
attach(cube('Phone rounded body',(0,0,0),(.17,.31,.016),dark,.012),phone)
screen=bpy.data.materials.new('Phone dark blue glass');screen.use_nodes=True
bs=screen.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.025,.065,.095,1);bs.inputs['Roughness'].default_value=.24;bs.inputs['Coat Weight'].default_value=.18
attach(cube('Phone screen',(0,0,.009),(.149,.275,.002),screen,.010),phone)
attach(cube('Phone speaker',(0,.12,.011),(.035,.003,.001),dark,.001),phone)
attach(sphere('Phone front camera',(.030,.120,.011),(.003,.003,.001),gold),phone)
phone['Content']='Contact — actual supplied email and phone can be added in website'

# Keep the notebook distinct from the newspaper for its own requested close-up.
bpy.context.view_layer.update()
notebook=bpy.data.objects['Reporting_Notebook']
notebook_delta=Vector((-1.68,-2.62,.91))-notebook.matrix_world.translation
for ob in bpy.data.objects:
 if ob.name.startswith(('Reporting_Notebook','Notebook ruled line','Brass pen')) and ob.parent is None:ob.location+=notebook_delta
bpy.context.view_layer.update()
# Replace one shelf book with a hinged, addressable replica; pull out and open it.
group('05');selected=bpy.data.objects['About_Book_01'];bpy.context.view_layer.update()
centre=selected.matrix_world.translation.copy();dims=selected.dimensions.copy()
for ob in list(current.objects):
 if ob.name==selected.name or (ob.name.startswith(('Book page block','Book spine gold band')) and abs(ob.location.x-centre.x)<.025 and abs(ob.location.y-centre.y)<.16 and abs(ob.location.z-centre.z)<dims.z*.6):
  ob.hide_render=True;ob.hide_set(True)
book=bpy.data.objects.new('Interactive_Book_Root',None);current.objects.link(book)
start=Vector((centre.x,2.48,centre.z));start_rot=(math.pi/2,0,math.pi/2)
book.location=start;book.rotation_euler=start_rot
w=.24;h=.32
attach(cube('Book back cover',(.12,0,-.033),(w,.34,.014),navy,.005),book)
attach(cube('Book right page block',(.12,0,-.012),(w-.01,h,.025),paper,.003),book)
cover_hinge=bpy.data.objects.new('Interactive_Book_Cover_Hinge',None);current.objects.link(cover_hinge);cover_hinge.parent=book;cover_hinge.location=(0,0,.021)
attach(cube('Book opening front cover',(.12,0,.009),(w,.34,.014),navy,.005),cover_hinge)
page_hinge=bpy.data.objects.new('Interactive_Book_Page_Hinge',None);current.objects.link(page_hinge);page_hinge.parent=book;page_hinge.location=(0,0,.021)
attach(cube('Book left page block',(.12,0,-.010),(w-.01,h,.014),paper,.003),page_hinge)
attach(cube('Book spine',(0,0,0),(.018,.34,.075),navy,.005),book)
book['Content']='Selected feature reporting; blank page blocks await owner content'
book['Interaction']='Pull from shelf / open hinged cover and pages / close / return'

# One master orthographic camera. Every HOME keyframe is copied from the same pose.
group('10');data=bpy.data.cameras.new('Camera • Portfolio animation 1920x1080');cam=bpy.data.objects.new('Camera • Portfolio animation 1920x1080',data);current.objects.link(cam)
data.type='ORTHO';data.lens=50;cam.rotation_mode='QUATERNION';scene.camera=cam
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100;scene.render.fps=24
home_target=Vector((1.30,-.40,1.15));home_position=Vector((13.5,-16.5,12.0));home_rotation=(home_target-home_position).to_track_quat('-Z','Y')
cam.location=home_position;cam.rotation_quaternion=home_rotation;data.ortho_scale=15.1
# Frame actual camera-visible geometry, not imaginary ceiling corners in the cutaway.
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();shell=[]
for ob in bpy.data.objects:
 if ob.type not in {'MESH','CURVE'} or ob.hide_render or not ob.visible_camera or ob.name.startswith(('Studio ground','Exterior stone landing')):continue
 e=ob.evaluated_get(deps)
 if ob.type=='CURVE':
  m=e.to_mesh();shell.extend(e.matrix_world@v.co for v in m.vertices);e.to_mesh_clear()
 else:shell.extend(e.matrix_world@Vector(c) for c in e.bound_box)
for i in range(3):
 bpy.context.view_layer.update();uv=[world_to_camera_view(scene,cam,p) for p in shell]
 minx=min(p.x for p in uv);maxx=max(p.x for p in uv);miny=min(p.y for p in uv);maxy=max(p.y for p in uv)
 shift=home_rotation@Vector((((minx+maxx)/2-.5)*data.ortho_scale,((miny+maxy)/2-.5)*data.ortho_scale*1080/1920,0))
 home_position+=shift;home_target+=shift;cam.location=home_position
 required=max((maxx-minx)/.91,(maxy-miny)/.91)
 data.ortho_scale*=required
home_scale=data.ortho_scale
HOME=(home_position.copy(),home_rotation.copy(),home_scale)
def pose(target,offset,scale):
 target=Vector(target);position=target+Vector(offset);return (position,(target-position).to_track_quat('-Z','Y'),scale)
def key(frame,p):
 cam.location=p[0];cam.rotation_quaternion=p[1];data.ortho_scale=p[2]
 cam.keyframe_insert(data_path='location',frame=frame);cam.keyframe_insert(data_path='rotation_quaternion',frame=frame);data.keyframe_insert(data_path='ortho_scale',frame=frame)
def centre_of(name):
 ob=bpy.data.objects[name];bpy.context.view_layer.update();return sum((ob.matrix_world@Vector(c) for c in ob.bound_box),Vector())/8
focus={
 'cabinet':pose((-1.59,2.43,.99),(2.4,-4.6,2.65),3.40),
 'bookshelf':pose((4.82,2.55,1.40),(2.2,-4.5,1.7),4.95),
 'open_book':pose((4.66,1.58,1.66),(1.1,-3.5,1.55),1.70),
 'newspaper':pose((-1.55,-2.01,.90),(1.4,-1.4,3.0),1.65),
 'laptop':pose(centre_of('Digital_Laptop_base')+Vector((0,0,.08)),(2.5,-.8,1.8),1.60),
 'notebook':pose(centre_of('Reporting_Notebook'),(1.2,-1.6,2.7),1.25),
 'violin':pose((2.40,-2.08,.75),(1.8,-3.0,1.0),2.60),
 'phone':pose(phone.location,(1.0,-1.2,2.6),.90)
}
scene.timeline_markers.clear();stages=[];returns=[]
def stage(number,label,start,end,preview):
 scene.timeline_markers.new('%02d | %s'%(number,label),frame=start)
 stages.append({'step':number,'label':label,'start':start,'end':end,'preview':preview,'start_seconds':round((start-1)/24,2),'end_seconds':round(end/24,2)})
key(1,(HOME[0],HOME[1],home_scale*1.40));key(49,HOME);key(72,HOME)
stage(1,'Zoom in 房間 → HOME',1,72,72)
key(73,HOME);key(120,HOME);stage(2,'可點物件提示 — 網頁效果預留',73,120,120)
cursor=121
items=[('cabinet','學經歷矮櫃'),('bookshelf','書架／抽書／打開書本'),('newspaper','桌上報紙'),('laptop','筆電'),('notebook','採訪筆記本'),('violin','小提琴'),('phone','電話')]
book_open_start=0
for index,(which,label) in enumerate(items):
 num=3+index*2;start=cursor;key(start,HOME);key(start+48,focus[which])
 if which=='bookshelf':
  # Keep camera on bookshelf, then approach the extracted opening book.
  book_open_start=start+48
  for f,loc,rot,scale in [(1,Vector((centre.x,2.48,centre.z)),start_rot,1),(book_open_start,Vector((centre.x,2.48,centre.z)),start_rot,1),(book_open_start+32,Vector((4.66,1.58,1.66)),(1.03,0,0),1.5)]:
   book.location=loc;book.rotation_euler=rot;book.scale=(scale,scale,scale)
   book.keyframe_insert(data_path='location',frame=f);book.keyframe_insert(data_path='rotation_euler',frame=f);book.keyframe_insert(data_path='scale',frame=f)
  key(book_open_start+36,focus['open_book'])
  for ob in [cover_hinge,page_hinge]:
   for f,angle in [(1,0),(book_open_start+25,0),(book_open_start+60,-math.radians(172))]:
    ob.rotation_euler.y=angle;ob.keyframe_insert(data_path='rotation_euler',index=1,frame=f)
  end=start+143;key(end,focus['open_book']);stage(num,label,start,end,end)
  back_start=end+1;close_end=back_start+24
  for ob in [cover_hinge,page_hinge]:
   ob.keyframe_insert(data_path='rotation_euler',index=1,frame=back_start)
   ob.rotation_euler.y=0;ob.keyframe_insert(data_path='rotation_euler',index=1,frame=close_end)
  book.keyframe_insert(data_path='location',frame=back_start);book.keyframe_insert(data_path='rotation_euler',frame=back_start);book.keyframe_insert(data_path='scale',frame=back_start)
  book.location=(centre.x,2.48,centre.z);book.rotation_euler=start_rot;book.scale=(1,1,1)
  for prop in ['location','rotation_euler','scale']:book.keyframe_insert(data_path=prop,frame=close_end+20)
  key(back_start,focus['open_book']);key(close_end,focus['open_book']);key(close_end+48,HOME);back_end=close_end+59;key(back_end,HOME)
 else:
  end=start+71;key(end,focus[which]);stage(num,label,start,end,end)
  back_start=end+1;back_end=back_start+59;key(back_start,focus[which]);key(back_start+48,HOME);key(back_end,HOME)
 stage(num+1,'Zoom out → HOME（相同構圖）',back_start,back_end,back_end);returns.append(back_end);cursor=back_end+1

# Auto-clamped easing avoids overshoot during zooms and moving book parts.
def smooth_action(action):
 if not action:return
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
for ob in [cam,book,cover_hinge,page_hinge]:
 if ob.animation_data:smooth_action(ob.animation_data.action)
if data.animation_data:smooth_action(data.animation_data.action)
scene.frame_start=1;scene.frame_end=cursor-1
# Verify all returns have precisely the same pose and framing as the intro endpoint.
for frame in [49,72,120]+returns:
 scene.frame_set(frame);bpy.context.view_layer.update()
 assert (cam.location-HOME[0]).length<1e-5
 assert abs(cam.rotation_quaternion.dot(HOME[1]))>0.999999
 assert abs(data.ortho_scale-home_scale)<1e-5
 assert data.lens==50
scene.frame_set(stages[4]['preview']);bpy.context.view_layer.update()
assert abs(cover_hinge.rotation_euler.y)>2.9
scene.frame_set(1)
scene['Animation sequence']='16 requested stages; all room returns identical to INTRO endpoint'
scene['HOME frames']=json.dumps([49,72,120]+returns)
scene['HOME orthographic scale']=home_scale
scene['Sparkle']='Website only: slowly pulsing object outlines; stronger glow on hover. No glow baked into Blender.'
scene['Clickable objects']='Certificate_Graduation; Certificate_Internship_01; Certificate_Internship_02; Interactive_Book_Root; Newspaper left page; Digital_Laptop_base; Reporting_Notebook; Life_Violin_body; Interactive_Phone'
scene.render.image_settings.file_format='PNG';scene.render.filepath='//Katy_Animation_Frames/Room_';scene.cycles.samples=64
for screen_ui in bpy.data.screens:
 for area in screen_ui.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
manifest={'resolution':[1920,1080],'fps':24,'frames':scene.frame_end,'duration_seconds':round(scene.frame_end/24,2),'home_scale':home_scale,'home_location':list(HOME[0]),'home_rotation_quaternion':list(HOME[1]),'stages':stages,'return_frames':returns}
Path(OUT+'/animation_plan.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('VERIFIED_ANIMATION',scene.frame_end,'frames',len(stages),'stages','1920x1080','identical HOME framing')
# Small rendered storyboard: all return shots reuse one verified HOME render.
scene.render.resolution_x=640;scene.render.resolution_y=360;scene.cycles.samples=8
for step in [1,3,5,7,9,11,13,15]:
 entry=next(x for x in stages if x['step']==step);scene.frame_set(entry['preview']);scene.render.filepath=OUT+'/shot_%02d.png'%step;bpy.ops.render.render(write_still=True)
print('STORYBOARD_COMPLETE')
