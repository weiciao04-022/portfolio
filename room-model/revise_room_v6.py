import bpy,ast,math,os,random
from math import sin,cos,pi,exp,sqrt
from mathutils import Vector
from pathlib import Path
OUT='/private/tmp/katy-room-v6';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/private/tmp/katy-room-v5/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','cube','sphere','cyl','rod','curve','ring','mesh']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base=bpy.data.collections['00 • Architecture'];collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};current=base

def satin(name,color):
 m=mat(name,color,.40);nodes=m.node_tree.nodes;links=m.node_tree.links;bs=nodes.get('Principled BSDF')
 bs.inputs['Specular IOR Level'].default_value=.32;bs.inputs['Coat Weight'].default_value=0
 bs.inputs['Anisotropic'].default_value=.32;bs.inputs['Sheen Weight'].default_value=.22;bs.inputs['Sheen Roughness'].default_value=.50
 tex=nodes.new('ShaderNodeTexCoord')
 noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=130;noise.inputs['Detail'].default_value=2
 links.new(tex.outputs['Object'],noise.inputs['Vector'])
 rough=nodes.new('ShaderNodeMapRange');rough.inputs['From Min'].default_value=0;rough.inputs['From Max'].default_value=1;rough.inputs['To Min'].default_value=.34;rough.inputs['To Max'].default_value=.46
 links.new(noise.outputs['Fac'],rough.inputs['Value']);links.new(rough.outputs['Result'],bs.inputs['Roughness'])
 wave_x=nodes.new('ShaderNodeTexWave');wave_x.bands_direction='X';wave_x.inputs['Scale'].default_value=240;wave_x.inputs['Distortion'].default_value=.15
 wave_y=nodes.new('ShaderNodeTexWave');wave_y.bands_direction='Y';wave_y.inputs['Scale'].default_value=240;wave_y.inputs['Distortion'].default_value=.15
 links.new(tex.outputs['Object'],wave_x.inputs['Vector']);links.new(tex.outputs['Object'],wave_y.inputs['Vector'])
 weave=nodes.new('ShaderNodeMath');weave.operation='MULTIPLY';links.new(wave_x.outputs['Color'],weave.inputs[0]);links.new(wave_y.outputs['Color'],weave.inputs[1])
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.11;bump.inputs['Distance'].default_value=.0011
 links.new(weave.outputs[0],bump.inputs['Height']);links.new(bump.outputs[0],bs.inputs['Normal'])
 m['Fabric']='Soft satin / fine crossed fibre normal, varied roughness, no plastic clearcoat'
 return m
ivory=satin('Ivory silk with fine woven fibres',(.84,.80,.72));blush=satin('Blush silk with fine woven fibres',(.55,.34,.31));sage=satin('Sage soft pillow fabric',(.38,.44,.34))
group('03')
for ob in list(current.objects):
 if ob.name.startswith(('Fluffy silk duvet','Silk duvet side hem','Silk rose coverlet','Plump silk pillow','Rose soft accent pillow','Sage soft accent pillow')):bpy.data.objects.remove(ob,do_unlink=True)

cx=1.20
def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
folds=[(.37,-.08,.7,.035,.035),(-.44,.42,-.4,.055,.047),(.12,.81,.3,.060,.055),(.54,1.17,-.8,.045,.040),(-.28,1.40,.5,.052,.053)]
def height(x,y):
 xx=x-cx
 side=smooth((abs(xx)-.87)/.40);foot=smooth((-.26-y)/.60)
 loft=.24*exp(-(xx/.97)**4-((y-.61)/1.27)**4)
 z=.91+loft-.72*side-.75*foot
 z+=.024*sin(y*5.5+xx*2)+.018*cos(xx*6.1-y*2.8)
 # Irregular narrow folds across the duvet, strongest near the head and hem.
 for a,b,angle,width,amplitude in folds:
  distance=(xx-a)*cos(angle)+(y-b)*sin(angle)
  along=-(xx-a)*sin(angle)+(y-b)*cos(angle)
  z+=amplitude*exp(-(distance/width)**2-(along/.65)**2)
 z+=.10*exp(-((y-1.48)/.15)**2)*(1-.30*cos(xx*6))
 z+=.015*sin(xx*26+y*12)*exp(-((y-1.52)/.34)**2)
 z+=.042*sin(y*19+xx*4)*side+.037*sin(xx*22-y*3)*foot
 # Small non-uniform edge puckering, avoiding the previous smooth clay-like silhouette.
 z+=.012*sin(xx*35-y*8)*max(side,foot)
 return max(.12,z)

nx=240;ny=280;verts=[];faces=[]
for j in range(ny+1):
 y=-.88+2.65*j/ny
 for i in range(nx+1):
  x=cx+(i/nx-.5)*2.53;verts.append((x,y,height(x,y)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
duvet=mesh('Fluffy silk duvet — refined fabric',verts,faces,ivory)
for p in duvet.data.polygons:p.use_smooth=True
mod=duvet.modifiers.new('High resolution smooth folds','SUBSURF');mod.levels=1;mod.render_levels=1
mod=duvet.modifiers.new('Soft filled duvet edge','SOLIDIFY');mod.thickness=.035;mod.offset=-1
duvet['Base quads']=len(faces);duvet['Notes']='Higher-resolution, irregular fold mesh; silk surface separate from filled duvet volume'
for x in [cx-1.265,cx+1.265]:curve('Fine duvet stitched hem',[(x,-.88+2.65*k/280,height(x,-.88+2.65*k/280)+.003) for k in range(281)],.0025,ivory)

# Soft rounded pillow volume with pinched seam and fine fabric gathering at the edges.
def pillow(name,loc,w,d,puff,material,tilt=0,turn=0,seed=1):
 random.seed(seed);phase=random.uniform(0,pi);n=96;verts=[];faces=[]
 for side in [1,-1]:
  for j in range(n+1):
   v=j/n
   for i in range(n+1):
    u=i/n
    x=(u-.5)*w*(1-.08*(2*v-1)**8);y=(v-.5)*d*(1-.08*(2*u-1)**8)
    fill=max(0,sin(pi*u)*sin(pi*v))**.38
    z=side*(.008+puff*fill)
    gather=(exp(-u/.07)+exp(-(1-u)/.07))*sin(v*53+phase)
    gather+=(exp(-v/.07)+exp(-(1-v)/.07))*sin(u*49+phase*.7)
    z+=.018*gather*sqrt(max(0,fill))
    # A slight off-centre compression keeps the pillows from looking inflated rubber.
    z-=side*.018*exp(-((u-.36)/.20)**2-((v-.59)/.18)**2)
    verts.append((x,y,z))
 N=(n+1)**2
 for side in [0,1]:
  for j in range(n):
   for i in range(n):
    a=side*N+j*(n+1)+i;f=(a,a+1,a+n+2,a+n+1);faces.append(f if side==0 else f[::-1])
 edge=list(range(n+1))+[j*(n+1)+n for j in range(1,n+1)]+[n*(n+1)+i for i in range(n-1,-1,-1)]+[j*(n+1) for j in range(n-1,0,-1)]
 for a,b in zip(edge,edge[1:]+edge[:1]):faces.append((a,b,b+N,a+N))
 ob=mesh(name,verts,faces,material);ob.location=loc;ob.rotation_euler=(tilt,0,turn)
 for p in ob.data.polygons:p.use_smooth=True
 mod=ob.modifiers.new('Fine soft pillow surface','SUBSURF');mod.levels=1;mod.render_levels=1
 seam=curve(name+' stitched edge',[(verts[i][0],verts[i][1],0) for i in edge],.0025,material,True);seam.location=loc;seam.rotation_euler=ob.rotation_euler
 ob['Base quads']=len(faces)
 return ob
pillow('Plump silk pillow left — refined',(.72,1.94,1.18),.91,.69,.21,ivory,.22,-.075,3)
pillow('Plump silk pillow right — refined',(1.66,1.91,1.19),.90,.70,.225,ivory,.17,.06,8)
pillow('Rose soft accent pillow — refined',(.78,1.57,1.39),.63,.55,.18,blush,1.09,-.14,2)
pillow('Sage soft accent pillow — refined',(1.68,1.59,1.40),.58,.53,.18,sage,1.05,.08,5)

# A thinner silk coverlet follows the duvet with its own loose wrinkles, instead of a thick flat slab.
nx=240;ny=100;verts=[];faces=[]
for j in range(ny+1):
 y=-.65+.92*j/ny
 for i in range(nx+1):
  x=cx+(i/nx-.5)*2.54
  z=height(x,y)+.055+.012*sin((x-cx)*15+y*10)+.009*sin((x-cx)*27-y*7)
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
ob=mesh('Silk rose coverlet — refined folds',verts,faces,blush)
for p in ob.data.polygons:p.use_smooth=True
mod=ob.modifiers.new('Fine silk surface','SUBSURF');mod.levels=1;mod.render_levels=1
mod=ob.modifiers.new('Thin satin hem','SOLIDIFY');mod.thickness=.005
ob['Base quads']=len(faces)

scene=bpy.context.scene;scene.frame_set(1)
scene['Revision']='v6 — high-resolution padded bedding, irregular draped folds, gathered pillow seams and woven silk shaders; clear grid windows and animated wardrobe retained'
scene.cycles.samples=64
scene.camera=bpy.data.objects['Camera • Room overview'];scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
bpy.ops.render.render(write_still=True)
cam=bpy.data.objects['Camera • Silk bed detail'];cam.location=(4.10,-3.40,3.30);cam.rotation_euler=(Vector((1.20,.65,1.0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=56
scene.camera=cam;scene.render.resolution_x=1400;scene.render.resolution_y=1150;scene.render.filepath=OUT+'/Katy_Bedding_Detail.png'
bpy.ops.render.render(write_still=True)
print('V6_COMPLETE')
