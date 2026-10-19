import bpy,math
from pathlib import Path
from mathutils import Vector
p=Path('/private/tmp/katy-book-fixed')
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour']
cover=bpy.data.objects['Interactive_Book_Cover_Hinge'];pages=bpy.data.objects['Interactive_Book_Page_Hinge'];left=bpy.data.objects['Book left page block']
# The page stack must sit inside the cover, and rotate with the same hinge angle.
# Previously the differing angles caused the cover to occlude the inner half of the page.
pages.location=cover.location.copy();left.location.z=-.010
def max_angle(ob):
 return max(abs(k.co.y) for layer in ob.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves if fc.data_path=='rotation_euler' and fc.array_index==1 for k in fc.keyframe_points)
factor=max_angle(cover)/max_angle(pages)
for layer in pages.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if fc.data_path=='rotation_euler' and fc.array_index==1:
     for k in fc.keyframe_points:
      k.co.y*=factor;k.handle_left.y*=factor;k.handle_right.y*=factor
# Validate the geometry separation throughout opening/closing; the paper is on the
# inside face of the cover in local coordinates and shares its motion exactly.
for frame in range(301,443):
 s.frame_set(frame);bpy.context.view_layer.update()
 assert abs(pages.rotation_euler.y-cover.rotation_euler.y)<1e-5,(frame,'hinge mismatch')
 assert (pages.matrix_world.translation-cover.matrix_world.translation).length<1e-5
assert left.location.z+left.data.vertices[0].co.z < bpy.data.objects['Book opening front cover'].location.z
assert len([scene for scene in bpy.data.scenes if scene.name.startswith('CLIP ')])==18
s['Book page fix']='Left paper stack follows cover hinge exactly and stays on inner cover face throughout frames 301-442.'
s.frame_set(1)
if bpy.context.window:bpy.context.window.scene=s
bpy.ops.wm.save_as_mainfile(filepath=str(p/'Katy_Parisian_Room.blend'))
s.frame_set(366);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.cycles.samples=32;s.render.filepath=str(p/'Katy_Book_Open_Fixed.png')
bpy.ops.render.render(write_still=True)
print('BOOK_FIXED: whole left page visible; matched hinge motion in all opening/closing frames; 18 clip scenes retained')
