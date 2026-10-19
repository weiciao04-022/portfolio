import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
OUT='/private/tmp/katy-immersive';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;s.frame_set(72)
dz=.7
for o in bpy.data.objects:
 n=o.name
 if n in ['Back plaster wall','Left front wall pier','Left rear wall pier','Sun blocker • front opening','Sun blocker • right opening']:
  o.dimensions.z+=dz;o.location.z+=dz/2
 elif n=='Floor window lintel' or n.startswith('Left crown moulding') or (n.startswith('Back skirting / cornice') and o.location.z>3) or n.startswith('Ceiling rose') or n=='Sun blocker • ceiling' or n=='Full-width curtain rail' or n.startswith('Curtain ring'):
  o.location.z+=dz
 elif n.startswith(('Floor window outer jamb','Slim floor window mullion','Window grid vertical bar','Full-height glass panel')):
  o.dimensions.z+=dz;o.location.z+=dz/2
 elif n.startswith('Floor window top bottom frame') and o.location.z>3:o.location.z+=dz
 elif n.startswith('Window grid horizontal bar'):o.location.z=.065+(o.location.z-.065)*(3.985/3.285)
 elif n.startswith('Full-length gathered curtain'):
  for v in o.data.vertices:v.co.z=.045+(v.co.z-.045)*(4.05/3.35)
 elif n.startswith(('French wall panel','Expanded wall moulding')):
  for spline in o.data.splines:
   for p in spline.points:p.co.z=.48+(p.co.z-.48)*((3.10+dz-.48)/(3.10-.48))
 elif n=='Chandelier suspension':o.dimensions.z+=dz;o.location.z+=dz/2
 elif n=='Ceiling soft bounce':o.location.z+=dz
# Keep chandelier at its comfortable hanging height and lengthen suspension.
cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear();cam.data.type='PERSP';cam.data.lens=32;cam.data.sensor_fit='HORIZONTAL';cam.rotation_mode='QUATERNION'
s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.cycles.samples=12
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
for label,pos,target in [('candidate_A',(3.2,-7.2,3.3),(1.3,.7,1.7)),('candidate_B',(2.6,-6.7,3.0),(1.3,.8,1.6))]:
 cam.location=pos;cam.rotation_quaternion=(Vector(target)-cam.location).to_track_quat('-Z','Y');s.render.filepath=OUT+'/'+label+'.png';bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/staged.blend')
