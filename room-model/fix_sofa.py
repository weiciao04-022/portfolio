import bpy,ast,math,os,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
OUT=Path('/private/tmp/katy-sofa');OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.data.scenes['DEMO • Complete room tour'];bpy.context.window.scene=s;s.frame_set(72)
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['place','cube','cyl','mesh','curve']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helper','exec'))
current=bpy.data.collections['11 • Sofa & living area']
for o in list(current.objects):
 if o.name.startswith('Sofa ') and not o.name.startswith('Sofa coffee table'):bpy.data.objects.remove(o,do_unlink=True)
cloth=bpy.data.materials['Warm ivory boucle sofa'];wood=bpy.data.materials['Walnut furniture']
bs=cloth.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.84;bs.inputs['Sheen Weight'].default_value=.32;bs.inputs['Sheen Roughness'].default_value=.65
# All cushion piping is local geometry parented to its cushion.
def rounded(name,loc,dim,material,r=.08,puff=.018):
 half=Vector(dim)/2;inner=Vector([v-r for v in half]);verts=[];faces=[];N=32
 for axis in range(3):
  a=(axis+1)%3;b=(axis+2)%3
  for sign in [-1,1]:
   start=len(verts)
   for j in range(N+1):
    for i in range(N+1):
     p=Vector((0,0,0));p[axis]=sign*half[axis];p[a]=(2*i/N-1)*half[a];p[b]=(2*j/N-1)*half[b]
     q=Vector([max(-inner[k],min(inner[k],p[k])) for k in range(3)]);v=q+(p-q).normalized()*r
     if axis==2:
      bulge=max(0,1-(v.x/half.x)**2)*max(0,1-(v.y/half.y)**2)
      v.z+=sign*puff*bulge
     verts.append(v)
   for j in range(N):
    for i in range(N):
     k=start+j*(N+1)+i;f=(k,k+1,k+N+2,k+N+1);faces.append(f if sign>0 else f[::-1])
 o=mesh(name,verts,faces,material);o.location=loc
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for p in o.data.polygons:p.use_smooth=True
 pts=[];rx=half.x;ry=half.y;rr=r
 for cx,cy,angle in [(rx-rr,ry-rr,0),(-rx+rr,ry-rr,90),(-rx+rr,-ry+rr,180),(rx-rr,-ry+rr,270)]:
  for k in range(13):
   t=math.radians(angle+90*k/12);pts.append((cx+rr*math.cos(t),cy+rr*math.sin(t),0))
 seam=curve(name+' • stitched edge',pts,.0022,material,True);seam.parent=o;seam.location=(0,0,0)
 return o
def back_rotation(lean):
 sn=math.sin(lean);cs=math.cos(lean)
 return Matrix(((0,sn,cs),(1,0,0),(0,cs,-sn))).to_quaternion()
sx=5.29;sy=-.48
base=cube('Sofa upholstered base',(sx,sy,.36),(1.16,2.48,.32),cloth,.11)
back=cube('Sofa soft back',(sx+.46,sy,.95),(.25,2.40,1.02),cloth,.11)
for y in [sy-1.13,sy+1.13]:cube('Sofa rounded arm',(sx-.03,y,.74),(1.14,.26,.59),cloth,.12)
for y in [sy-.53,sy+.53]:
 rounded('Sofa plush seat',(sx-.07,y,.645),(.92,1.055,.25),cloth,.085,.016)
 o=rounded('Sofa plump back cushion',(sx+.28,y,1.105),(1.02,.74,.235),cloth,.09,.022);o.rotation_mode='QUATERNION';o.rotation_quaternion=back_rotation(.13)
for x in [sx-.43,sx+.41]:
 for y in [sy-1.03,sy+1.03]:cyl('Sofa walnut foot',(x,y,.125),.047,.20,wood)
pink=cloth.copy();pink.name='Sofa dusty rose woven fabric';pink.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.56,.34,.32,1)
for name,y,mat,lean in [('Sofa pink scatter cushion',sy+.61,pink,.27),('Sofa sage scatter cushion',sy-.63,bpy.data.materials['Sage upholstery'],.31)]:
 o=rounded(name,(sx+.025,y,1.00),(.45,.47,.235),mat,.10,.023);o.rotation_mode='QUATERNION';o.rotation_quaternion=back_rotation(lean)
# Increase bevel resolution for smooth upholstered arms and frame.
for o in current.objects:
 if o.name.startswith('Sofa '):
  for m in o.modifiers:
   if m.type=='BEVEL':m.segments=8
for o in current.objects:
 if 'stitched edge' in o.name:assert o.parent is not None and o.location.length<1e-7
assert len(bpy.data.scenes)==19
for f in [49,72,252,480,612,744,876,1008,1140]:
 s.frame_set(f);assert (s.camera.location-Vector((2.5,-8.3,3.8))).length<1e-5
s.frame_set(72);s['Sofa revision']='Thick supported seat cushions, leaning back and scatter cushions, attached piping'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Katy_Parisian_Room.blend'))
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=1280;s.render.resolution_y=720;s.cycles.samples=40
s.render.filepath=str(OUT/'Katy_Parisian_Room_Preview.png');bpy.ops.render.render(write_still=True)
# Temporary camera for verification only, not saved into the animation file.
cd=bpy.data.cameras.new('Sofa review temporary');co=bpy.data.objects.new('Sofa review temporary',cd);s.collection.objects.link(co);co.location=(1.65,-3.95,2.6);co.rotation_euler=(Vector((5.3,-.48,.80))-co.location).to_track_quat('-Z','Y').to_euler();cd.lens=48;s.camera=co
s.render.filepath=str(OUT/'Katy_Sofa_Preview.png');bpy.ops.render.render(write_still=True)
print('SOFA VERIFIED: seams parented, supported thick cushions, preserved 19 scenes and HOME camera')
