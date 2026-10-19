import bpy,json
from pathlib import Path
from mathutils import Vector
OUT=Path('/private/tmp/katy-immersive')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'staged.blend'))
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;s.frame_set(72)
c=s.camera;c.animation_data_clear();c.data.animation_data_clear();c.data.type='PERSP';c.data.lens=32;c.data.sensor_fit='HORIZONTAL';c.data.clip_start=.02;c.data.clip_end=300
home_pos=Vector((2.5,-8.3,3.8));home_target=Vector((1.35,.3,1.35));home_rot=(home_target-home_pos).to_track_quat('-Z','Y');HOME=(home_pos,home_rot)
def pose(target,offset,width):
 target=Vector(target);offset=Vector(offset).normalized()*(width*c.data.lens/c.data.sensor_width)
 return target+offset,(-offset).to_track_quat('-Z','Y')
focus={
 'cabinet':pose((-1.59,2.43,1.0),(2.4,-4.6,2.65),3.4),
 'bookshelf':pose((4.82,2.55,1.4),(2.2,-4.5,1.7),4.95),
 'open_book':pose((4.66,1.58,1.66),(1.1,-3.5,1.55),1.7),
 'newspaper':pose((-1.55,-2.13,.90),(1.4,-1.4,3),1.65),
 'laptop':pose((-1.68,-1.35,1.01),(2.5,-.8,1.8),1.6),
 'notebook':pose((-1.68,-2.62,.91),(1.2,-1.6,2.7),1.25),
 'violin':pose((2.4,-2.08,.87),(1.8,-3,1),2.9),
 'phone':pose((-1.65,-.47,.896),(1,-1.2,2.6),.9)}
def key(f,p):
 c.location=p[0];c.rotation_quaternion=p[1]
 c.keyframe_insert(data_path='location',frame=f);c.keyframe_insert(data_path='rotation_quaternion',frame=f)
key(1,(home_pos+(home_pos-home_target).normalized()*3.5,home_rot))
for f in [49,72,73,120]:key(f,HOME)
returns=[]
for kind,start,end,back_end in [('cabinet',121,192,252),('bookshelf',253,396,480),('newspaper',481,552,612),('laptop',613,684,744),('notebook',745,816,876),('violin',877,948,1008),('phone',1009,1080,1140)]:
 key(start,HOME);key(start+48,focus[kind])
 if kind=='bookshelf':
  key(337,focus['open_book']);key(end,focus['open_book']);key(397,focus['open_book']);key(421,focus['open_book']);key(469,HOME)
 else:
  key(end,focus[kind]);key(end+1,focus[kind]);key(end+49,HOME)
 key(back_end,HOME);returns.append(back_end)
for layer in c.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
checks=[49,72,73,120,121,241,252,253,469,480,481,601,612,613,733,744,745,865,876,877,997,1008,1009,1129,1140]
for f in checks:
 s.frame_set(f);bpy.context.view_layer.update()
 assert (c.location-home_pos).length<1e-5
 assert abs(c.rotation_quaternion.dot(home_rot))>.999999
 assert abs(bpy.data.objects['Interactive_Laptop_Lid_Hinge'].rotation_euler.x-1.57079632679)<1e-4
assert len(bpy.data.scenes)==19
for sc in bpy.data.scenes:
 sc.camera=c;sc.render.resolution_x=1920;sc.render.resolution_y=1080;sc.render.resolution_percentage=100;sc.render.fps=24
 sc['HOME camera type']='PERSP';sc['HOME lens mm']=32;sc['Room ceiling height metres']=4.5
 if 'HOME orthographic scale' in sc:del sc['HOME orthographic scale']
 if sc!=s:sc.frame_set(sc.frame_start)
s['HOME frames']=json.dumps(checks);s['HOME position']=list(home_pos);s['HOME target']=list(home_target)
s.frame_set(72);bpy.context.view_layer.update();s.render.filepath='//Katy_Animation_Frames/Room_';s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.cycles.samples=64
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Katy_Parisian_Room.blend'))
for filename in ['animation_plan.json','Katy_Animation_Clips.json']:
 data=json.loads(Path('/Users/weiciao/Desktop/work',filename).read_text())
 for field in ['home_scale','home_ortho_scale','home_orthographic_scale']:data.pop(field,None)
 data.update(camera_type='PERSP',lens_mm=32,home_location=list(home_pos),home_rotation_quaternion=list(home_rot),home_target=list(home_target),room_height_metres=4.5)
 (OUT/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('VERIFIED: 19 scenes, 25 identical HOME anchors, 1920x1080, 32mm perspective, ceiling 4.5m')
s.render.resolution_x=640;s.render.resolution_y=360;s.cycles.samples=16
for name,f in [('cabinet',192),('book',396),('newspaper',552),('laptop',684),('notebook',816),('violin',948),('phone',1080)]:
 s.frame_set(f);s.render.filepath=str(OUT/('focus_'+name+'.png'));bpy.ops.render.render(write_still=True)
s.frame_set(72);s.render.resolution_x=1280;s.render.resolution_y=720;s.cycles.samples=40;s.render.filepath=str(OUT/'Katy_Parisian_Room_Preview.png');bpy.ops.render.render(write_still=True)
