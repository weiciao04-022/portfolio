import bpy
from mathutils import Vector
from pathlib import Path
P=Path('/private/tmp/katy-violin-move');P.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;s.frame_set(1)
for o in bpy.data.collections['07 • Violin — Life'].objects:
 print(o.name,'parent',o.parent.name if o.parent else None,'world',tuple(round(x,3) for x in o.matrix_world.translation))
bpy.context.view_layer.update()
root=bpy.data.objects['Motion_Violin_Bounce'];old=root.location.copy();new=Vector((3.35,1.65,old.z));delta=new-old
for layer in root.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if fc.data_path=='location':
     value=delta[fc.array_index]
     for k in fc.keyframe_points:
      k.co.y+=value;k.handle_left.y+=value;k.handle_right.y+=value
for o in bpy.data.collections['07 • Violin — Life'].objects:
 if o.parent is None:o.location+=delta
# Match the new violin position without changing HOME or other close-ups.
c=s.camera
for f in [925,948,949]:
 s.frame_set(f);loc=c.location.copy();c.location=loc+delta;c.keyframe_insert(data_path='location',frame=f)
for layer in c.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
for f in [1,877,1008,1140]:
 s.frame_set(f);assert (root.location-new).length<1e-5
s.frame_set(948);assert abs(root.location.z-new.z-.45)<1e-5
for f in [1,72,252,480,612,744,876,1008,1140]:
 s.frame_set(f);assert (c.location-Vector((3.6,-7.4,4.65))).length<1e-5
s.frame_set(1);bpy.context.view_layer.update();s['Violin position']='Between bed and bookshelf, x=3.35 y=1.65; matching floating close-up updated'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Katy_Parisian_Room.blend'))
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=1280;s.render.resolution_y=720;s.cycles.samples=32
s.render.filepath=str(P/'Katy_Parisian_Room_Preview.png');bpy.ops.render.render(write_still=True)
s.frame_set(948);s.render.resolution_x=800;s.render.resolution_y=450;s.cycles.samples=16;s.render.filepath=str(P/'Katy_Violin_Preview.png');bpy.ops.render.render(write_still=True)
print('VERIFIED: violin and stand moved together, floating action intact, close-up retargeted, HOME unchanged')
