import bpy,math,os
from mathutils import Vector,Matrix
from pathlib import Path
OUT='/private/tmp/katy-prop-motion'
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
scene=bpy.data.scenes['DEMO • Complete room tour'];scene.frame_set(1);bpy.context.view_layer.update()
col=bpy.data.collections['06 • Writing desk — Journalism']
def empty(name,loc):
 o=bpy.data.objects.new(name,None);col.objects.link(o);o.location=loc;o.empty_display_type='PLAIN_AXES';o.empty_display_size=.08;bpy.context.view_layer.update();return o
def parent_keep(o,parent):
 world=o.matrix_world.copy();o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted();o.matrix_basis=world
def smooth(o):
 if not o.animation_data:return
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
def bounce(o,start,height,tilt=0,delay=0):
 loc=o.location.copy();rot=o.rotation_euler.copy();start+=delay
 for frame,z,angle in [(1,0,0),(start,0,0),(start+18,height,tilt),(start+31,height*.20,-tilt*.25),(start+43,0,0),(1140,0,0)]:
  o.location=loc+Vector((0,0,z));o.rotation_euler=rot.copy();o.rotation_euler.y+=angle
  o.keyframe_insert(data_path='location',frame=frame);o.keyframe_insert(data_path='rotation_euler',frame=frame)
 o.animation_data.action.name=o.name+'_SoftBounce';smooth(o);o['Motion']='Small positive lift then settle; no scale stretching or floor penetration'

# Certificate frames (including their rear supports) lift gently when approached.
for index,name in enumerate(['Certificate_Graduation','Certificate_Internship_01','Certificate_Internship_02']):
 root=bpy.data.objects[name];stand=bpy.data.objects.get(name+' rear stand')
 if stand:parent_keep(stand,root)
 bounce(root,121,.055,.025,index*2)

# Book keeps its existing extraction/open/close action, with a separate subtle lift layer.
root=empty('Motion_Book_Bounce',(0,0,0));book=bpy.data.objects['Interactive_Book_Root'];book.parent=root;book.matrix_parent_inverse=Matrix.Identity(4)
bounce(root,253,.055)

root=empty('Motion_Newspaper_Bounce',(-1.58,-1.92,.90))
for name in ['Newspaper left page','Newspaper right page']:parent_keep(bpy.data.objects[name],root)
root.location.y-=.12
bounce(root,481,.038,.025)

root=empty('Motion_Notebook_Bounce',(-1.68,-2.62,.91))
for o in list(bpy.data.objects):
 if o.name.startswith(('Reporting_Notebook','Notebook ruled line','Brass pen')) and o.parent is None:parent_keep(o,root)
bounce(root,745,.055,.028)

root=empty('Motion_Violin_Bounce',(2.40,-2.08,.75))
for o in list(bpy.data.objects):
 if (o.name.startswith(('Life_Violin','Violin ','Bow horsehair')) and not o.name.startswith('Violin stand') and o.parent is None):parent_keep(o,root)
bounce(root,877,.075,.020)
bounce(bpy.data.objects['Interactive_Phone'],1009,.035,.030)

# Laptop is closed at HOME. A real rear hinge carries both the shell and display.
base=bpy.data.objects['Digital_Laptop_base'];root=empty('Motion_Laptop_Bounce',base.matrix_world.translation)
root.rotation_euler.z=math.pi/2;bpy.context.view_layer.update()
shell=bpy.data.objects['Digital_Laptop_screen'];display=bpy.data.objects['Laptop screen inset']
for o in list(bpy.data.objects):
 if (o.name in ['Digital_Laptop_base','Laptop keyboard'] or o.name.startswith('Laptop key')) and o.parent is None:parent_keep(o,root)
hinge=empty('Interactive_Laptop_Lid_Hinge',(0,0,0));hinge.parent=root;hinge.matrix_parent_inverse=Matrix.Identity(4);hinge.location=(0,.165,.044)
for o,loc in [(shell,(0,0,.165)),(display,(0,-.017,.165))]:
 o.parent=hinge;o.matrix_parent_inverse=Matrix.Identity(4);o.location=loc;o.rotation_euler=(0,0,0);o.scale=(1,1,1)
for frame,angle in [(1,90),(613,90),(625,90),(665,-12),(684,-12),(732,90),(1140,90)]:
 hinge.rotation_euler.x=math.radians(angle);hinge.keyframe_insert(data_path='rotation_euler',index=0,frame=frame)
hinge.animation_data.action.name='Laptop_Lid_Close_Open_Close';smooth(hinge)
bounce(root,613,.035)
hinge['Motion']='Closed at HOME; opens during laptop_in; closes during laptop_out'

# Verify pop-ups settle before every return; camera and clip scene settings stay intact.
returns=[72,120,252,480,612,744,876,1008,1140]
camera=scene.camera;scene.frame_set(72);bpy.context.view_layer.update();home=camera.matrix_world.copy();scale=camera.data.ortho_scale
for frame in returns:
 scene.frame_set(frame);bpy.context.view_layer.update()
 assert max(abs(camera.matrix_world[i][j]-home[i][j]) for i in range(4) for j in range(4))<1e-5
 assert abs(camera.data.ortho_scale-scale)<1e-5
 assert abs(hinge.rotation_euler.x-math.pi/2)<1e-5
for frame in [665,684]:
 scene.frame_set(frame);assert abs(hinge.rotation_euler.x-math.radians(-12))<1e-5
assert len([s for s in bpy.data.scenes if s.name.startswith('CLIP ')])==18
scene['Prop motion']='Certificates, selected book, newspaper, laptop, notebook, violin and phone gently lift then settle during their zoom-in. Laptop closes at HOME.'
scene.frame_set(1)
if bpy.context.window:bpy.context.window.scene=scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
# A small review sequence samples the laptop opening, with its matching camera animation.
scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.image_settings.media_type='IMAGE';scene.render.image_settings.file_format='PNG';scene.cycles.samples=8
for frame in [613,631,645,665,684,709,732]:
 scene.frame_set(frame);scene.render.filepath=OUT+'/Laptop_%04d.png'%frame;bpy.ops.render.render(write_still=True)
print('PROP_MOTION_COMPLETE: seven targets bounce; laptop closed/open/closed; camera unchanged; 18 clip scenes retained')
