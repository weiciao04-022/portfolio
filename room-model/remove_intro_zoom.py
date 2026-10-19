import bpy,json
from pathlib import Path
from mathutils import Vector
P=Path('/private/tmp/katy-start-camera')
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;c=s.camera
old=Vector((2.5,-8.3,3.8));pos=Vector((2.5,-7.6,3.6));target=Vector((1.35,.3,1.35));rot=(target-pos).to_track_quat('-Z','Y')
# Change HOME anchors only; floating close-ups and object actions are retained.
frames=json.loads(s['HOME frames'])
for f in sorted(set([1]+frames)):
 c.location=pos;c.rotation_quaternion=rot;c.keyframe_insert(data_path='location',frame=f);c.keyframe_insert(data_path='rotation_quaternion',frame=f)
for layer in c.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
for f in list(range(1,121))+frames:
 s.frame_set(f);assert (c.location-pos).length<1e-5 and abs(c.rotation_quaternion.dot(rot))>.999999
for sc in bpy.data.scenes:
 assert sc.render.resolution_x==1920 and sc.render.resolution_y==1080
 sc['HOME position']=list(pos);sc['HOME target']=list(target);sc['Opening']='Fixed room view from frame 1, no intro zoom'
 for m in sc.timeline_markers:
  if m.frame==1 and 'Zoom in' in m.name:m.name='01 | 房間初始畫面（固定鏡頭）'
 if sc!=s:sc.frame_set(sc.frame_start)
s['HOME frames']=json.dumps(sorted(set([1]+frames)));s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Katy_Parisian_Room.blend'))
for name in ['animation_plan.json','Katy_Animation_Clips.json']:
 data=json.loads(Path('/Users/weiciao/Desktop/work',name).read_text());data.update(home_location=list(pos),home_target=list(target),home_rotation_quaternion=list(rot),opening='Fixed close room view; no opening zoom')
 if 'stages' in data:data['stages'][0]['label']='房間初始畫面（固定鏡頭）'
 if 'clips' in data:
  for cl in data['clips']:
   if cl['id']=='room_enter':cl.update(label='房間初始畫面（固定鏡頭）',**{'from':'room','to':'room','camera_motion':'none'})
 (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('VERIFIED_FIXED_OPENING: every frame 1–120 identical; all HOME returns identical; 1920x1080 preserved')
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=1280;s.render.resolution_y=720;s.cycles.samples=40;s.render.filepath=str(P/'Katy_Parisian_Room_Preview.png');bpy.ops.render.render(write_still=True)
