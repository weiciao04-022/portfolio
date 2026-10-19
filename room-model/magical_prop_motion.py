import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path('/private/tmp/katy-magic');OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;s.frame_set(1)
def smooth(o):
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
# Replace the brief bounce with lift, suspended movement, and controlled landing.
base={};targets=[]
def float_object(name,start,end,return_end,height,tilt=.045,delay=0):
 o=bpy.data.objects[name];loc=o.location.copy();rot=o.rotation_euler.copy();base[name]=(loc.copy(),rot.copy());o.animation_data_clear()
 for frame,z,angle in [(1,0,0),(start+delay,0,0),(start+20,height*.65,tilt*.45),(start+42,height+.045,tilt),(start+48,height,tilt*.7),(end-12,height+.028,tilt*.9),(end,height,tilt*.7),(end+1,height,tilt*.7),(return_end-24,height*.22,tilt*.2),(return_end-12,0,0),(return_end,0,0),(1140,0,0)]:
  o.location=loc+Vector((0,0,z));o.rotation_euler=rot.copy();o.rotation_euler.y+=angle
  for prop in ['location','rotation_euler']:o.keyframe_insert(data_path=prop,frame=frame)
 o.animation_data.action.name=name+'_MagicFloat';o['Motion']='Levitate visibly; hover while viewed; land on zoom-out';smooth(o);targets.append(o)
for i,name in enumerate(['Certificate_Graduation','Certificate_Internship_01','Certificate_Internship_02']):float_object(name,121,192,252,.28,.045,i*3)
for args in [('Motion_Newspaper_Bounce',481,552,612,.40,.075),('Motion_Laptop_Bounce',613,684,744,.36,.04),('Motion_Notebook_Bounce',745,816,876,.42,.065),('Motion_Violin_Bounce',877,948,1008,.45,.055),('Interactive_Phone',1009,1080,1140,.38,.085)]:float_object(*args)
# Lift only after the existing extraction animation has cleared the shelf.
o=bpy.data.objects['Motion_Book_Bounce'];base[o.name]=(o.location.copy(),o.rotation_euler.copy());o.animation_data_clear();targets.append(o)
for f,z in [(1,0),(253,0),(301,0),(333,0),(337,.04),(361,.18),(384,.205),(396,.18),(397,.18),(421,.18),(441,0),(480,0),(1140,0)]:
 o.location=base[o.name][0]+Vector((0,0,z));o.keyframe_insert(data_path='location',frame=f)
smooth(o)
# Retarget close-up positions upward to keep the flying objects inside the frame.
c=s.camera
for frames,height in [([169,192,193],.28),([337],.04),([396,397,421],.18),([529,552,553],.40),([661,684,685],.36),([793,816,817],.42),([925,948,949],.45),([1057,1080,1081],.38)]:
 for f in frames:
  s.frame_set(f);loc=c.location.copy();loc.z+=height;c.location=loc;c.keyframe_insert(data_path='location',frame=f)
smooth(c)
# Independent clip scenes and all common room endpoints remain intact.
returns=[72,120,252,480,612,744,876,1008,1140]
for f in returns:
 s.frame_set(f);assert (c.location-Vector((2.5,-8.3,3.8))).length<1e-5
 for o in targets:assert (o.location-base[o.name][0]).length<1e-5
 assert abs(bpy.data.objects['Interactive_Laptop_Lid_Hinge'].rotation_euler.x-math.pi/2)<1e-5
for name,f,h in [('Motion_Newspaper_Bounce',552,.4),('Motion_Laptop_Bounce',684,.36),('Motion_Notebook_Bounce',816,.42),('Motion_Violin_Bounce',948,.45),('Interactive_Phone',1080,.38)]:
 s.frame_set(f);assert abs(bpy.data.objects[name].location.z-base[name][0].z-h)<1e-5
assert len(bpy.data.scenes)==19
for sc in bpy.data.scenes:
 assert (sc.render.resolution_x,sc.render.resolution_y)==(1920,1080)
 if sc!=s:sc.frame_set(sc.frame_start)
s.frame_set(72);s['Prop motion']='Magic levitation: 28–45 cm sustained hover; return and land. Book flies out and opens; laptop rises and opens.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Katy_Parisian_Room.blend'))
manifest=json.loads(Path('/Users/weiciao/Desktop/work/Katy_Animation_Clips.json').read_text())
manifest['motion']='Visible magic levitation with sustained hovering; landing on return'
for clip in manifest['clips']:
 if clip['id'].endswith('_in') or clip['id']=='book_open':clip['prop_motion']='Lift visibly and hover; book/laptop also opens'
 elif clip['id'].endswith('_out'):clip['prop_motion']='Float down and return to original resting position'
(OUT/'Katy_Animation_Clips.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('VERIFIED_MAGIC_FLOAT: 19 scenes, all room endpoints restored, visible lift 28–45cm')
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=640;s.render.resolution_y=360;s.cycles.samples=8
for label,start,end in [('Newspaper',481,612),('Laptop',613,744)]:
 for f in range(start,end+1,6):
  s.frame_set(f);s.render.filepath=str(OUT/('%s_%04d.png'%(label,f)));bpy.ops.render.render(write_still=True)
print('MAGIC_PREVIEWS_COMPLETE')
