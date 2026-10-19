import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path('/private/tmp/katy-cert-stagger');OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;s.frame_set(1)
names=['Certificate_Graduation','Certificate_Internship_01','Certificate_Internship_02']
assert [bpy.data.objects[n].location.x for n in names]==sorted(bpy.data.objects[n].location.x for n in names)
base={}
for index,name in enumerate(names):
 o=bpy.data.objects[name];loc=o.location.copy();rot=o.rotation_euler.copy();base[name]=loc.copy();o.animation_data_clear()
 start=125+index*14;land=200+index*10
 for f,z,tilt in [(1,0,0),(start,0,0),(start+10,.19,.025),(start+20,.315,.045),(start+25,.28,.032),(192,.28,.032),(land,.28,.032),(land+14,0,0),(252,0,0),(1140,0,0)]:
  o.location=loc+Vector((0,0,z));o.rotation_euler=rot.copy();o.rotation_euler.y+=tilt
  o.keyframe_insert(data_path='location',frame=f);o.keyframe_insert(data_path='rotation_euler',frame=f)
 o.animation_data.action.name=name+'_MagicFloat_LeftToRight';o['Motion']='Left-to-right stagger: 14-frame lift delay, 10-frame landing delay'
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
# Verify the earlier frame is visibly airborne while the next has not started.
for f,airborne,waiting in [(137,names[0],names[1]),(151,names[1],names[2])]:
 s.frame_set(f)
 assert bpy.data.objects[airborne].location.z-base[airborne].z>.15
 assert (bpy.data.objects[waiting].location-base[waiting]).length<1e-6
for f in [192,252]:
 s.frame_set(f)
 for n in names:assert abs(bpy.data.objects[n].location.z-base[n].z-(.28 if f==192 else 0))<1e-5
for f in [72,252,480,612,744,876,1008,1140]:
 s.frame_set(f);assert (s.camera.location-Vector((2.5,-8.3,3.8))).length<1e-5
assert len(bpy.data.scenes)==19
s['Certificate motion']='Left to right: lift begins frames 125 / 139 / 153; landing begins 200 / 210 / 220'
s.frame_set(121);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Katy_Parisian_Room.blend'))
print('VERIFIED_LEFT_TO_RIGHT: visible individual starts 125/139/153, all hover 192, all home 252')
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=640;s.render.resolution_y=360;s.cycles.samples=8
for f in range(121,253,6):
 s.frame_set(f);s.render.filepath=str(OUT/('Certificate_%04d.png'%f));bpy.ops.render.render(write_still=True)
