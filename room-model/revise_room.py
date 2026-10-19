import bpy, math, random, ast, os
from math import sin,cos,pi,exp
from mathutils import Vector
from pathlib import Path

OUT='/private/tmp/katy-room-v2'
os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
tree=ast.parse(src)
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','cube','sphere','cyl','rod','curve','ring','mesh','light']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base=bpy.data.collections['00 • Architecture']
collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()}
current=base
def remove(o):bpy.data.objects.remove(o,do_unlink=True)
def named(prefix):return [o for o in bpy.data.objects if o.name.startswith(prefix)]
cream=bpy.data.materials['Warm ivory plaster'];trim=bpy.data.materials['Painted moulding · porcelain'];walnut=bpy.data.materials['Walnut furniture'];gold=bpy.data.materials['Aged brass'];dark=bpy.data.materials['Dark iron'];paper=bpy.data.materials['Book pages'];sage=bpy.data.materials['Sage upholstery'];rose=bpy.data.materials['Dusty rose velvet'];pink=bpy.data.materials['Blush cushion'];silver=bpy.data.materials['Laptop aluminium'];glass=bpy.data.materials['Clear window glass'];linen=bpy.data.materials['Washed ivory linen']

# Expand shell from 7 x 6 m to 8.3 x 7.4 m, preserving window and wall details.
o=bpy.data.objects['Floor foundation'];o.location.x=.65;o.location.y=-.70;o.dimensions=(8.45,7.55,.22)
o=bpy.data.objects['Back plaster wall'];o.location.x=.65;o.dimensions.x=8.45
for o in named('Window side wall'):
 if o.location.y<0:o.location.y=-2.975;o.dimensions.y=2.85
for o in named('Back skirting / cornice'):o.location.x=.65;o.dimensions.x=8.30
for o in named('Left skirting / cornice'):o.location.y=-.70;o.dimensions.y=7.40
for o in collections['01'].objects[:]:remove(o)
floor_code=src.split('# Individually editable, clipped herringbone oak blocks.')[1].split('# French window, sheer curtains')[0]
floor_code=floor_code.replace('range(-20,21)','range(-30,31)').replace('(0,3.48,True)','(0,4.78,True)').replace('(1,-2.98,False)','(1,-4.38,False)')
exec(floor_code)
group('00')
for delta in [0,.047]:
 curve('Expanded wall moulding',[(3.75-.65+delta,2.938,.62+delta),(3.75+.65-delta,2.938,.62+delta),(3.75+.65-delta,2.938,3.23-delta),(3.75-.65+delta,2.938,3.23-delta)],.016 if delta==0 else .007,trim,True)
for o in collections['05'].objects:o.location.x+=.55

# Remove all fireplace parts; preserve the wall-mounted arched mirror.
for o in collections['04'].objects[:]:
 if not any(s in o.name.lower() for s in ['mirror','gilded']):remove(o)
for o in named('Mantel roses'):remove(o)

# Silk materials: smooth anisotropic highlights, rather than coarse matte linen.
silk=mat('Champagne silk bedding',(.82,.76,.64),.26)
bs=silk.node_tree.nodes.get('Principled BSDF');bs.inputs['Anisotropic'].default_value=.48;bs.inputs['Sheen Weight'].default_value=.25;bs.inputs['Sheen Roughness'].default_value=.35
bs.inputs['Coat Weight'].default_value=.08
texture(silk,240,.055,.004)
rose_silk=mat('Dusty pink silk coverlet',(.52,.29,.27),.25)
bs=rose_silk.node_tree.nodes.get('Principled BSDF');bs.inputs['Anisotropic'].default_value=.50;bs.inputs['Sheen Weight'].default_value=.25
texture(rose_silk,230,.05,.004)
for prefix in ['Draped ivory duvet','Rose throw across bed foot','Throw fringe','Linen pillow','Blush accent pillow','Sage accent pillow']:
 for o in named(prefix):remove(o)
o=bpy.data.objects['Mattress'];o.location.z=.60;o.dimensions.z=.39
def smoothstep(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def duvet_height(x,y):
 edge=smoothstep((abs(x-.45)-.86)/.37)
 foot=smoothstep((-.24-y)/.58)
 mound=.20*exp(-((x-.45)/.96)**4-((y-.63)/1.28)**4)
 z=.91+mound-.69*edge-.72*foot
 # Broad irregular folds, fine folds only along draped edges.
 z+=.028*sin(y*7.1+x*2.3)+.014*sin(x*9-y*4)
 z+=.045*exp(-((y-.88)/.21)**2)*sin(x*3.3+.8)
 z+=.019*sin(y*23+x*3)*edge+.026*sin(x*19-y*5)*foot
 return max(.15,z)
group('03')
verts=[];faces=[];nx=96;ny=112
for j in range(ny+1):
 y=-.83+2.80*j/ny
 for i in range(nx+1):
  x=.45+(i/nx-.5)*2.45;verts.append((x,y,duvet_height(x,y)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
o=mesh('Fluffy silk duvet',verts,faces,silk)
for p in o.data.polygons:p.use_smooth=True
o.modifiers.new('Smooth soft folds','SUBSURF').levels=1
mod=o.modifiers.new('Duvet padded hem','SOLIDIFY');mod.thickness=.045;mod.offset=-1
# Hem follows the same surface, with an intentionally subtle welt seam.
for x in [-.765,1.665]:curve('Silk duvet side hem',[(x,-.83+2.80*k/112,duvet_height(x,-.83+2.80*k/112)+.004) for k in range(113)],.006,silk)
def pillow(name,loc,w,d,puff,material,tilt=0,turn=0):
 verts=[];faces=[];n=32
 for side in [1,-1]:
  for j in range(n+1):
   v=j/n
   for i in range(n+1):
    u=i/n;x=(u-.5)*w*(1-.10*(2*v-1)**6);y=(v-.5)*d*(1-.10*(2*u-1)**6)
    bulge=(max(0,sin(pi*u)*sin(pi*v)))**.50
    z=side*(.012+puff*bulge)
    z+=.007*sin(u*47+v*19)*(1-bulge)*bulge
    verts.append((x,y,z))
 N=(n+1)**2
 for side in [0,1]:
  for j in range(n):
   for i in range(n):
    a=side*N+j*(n+1)+i;f=(a,a+1,a+n+2,a+n+1);faces.append(f if side==0 else f[::-1])
 perimeter=list(range(n+1))+[j*(n+1)+n for j in range(1,n+1)]+[n*(n+1)+i for i in range(n-1,-1,-1)]+[j*(n+1) for j in range(n-1,0,-1)]
 for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):faces.append((a,b,b+N,a+N))
 o=mesh(name,verts,faces,material);o.location=loc;o.rotation_euler=(tilt,0,turn)
 for p in o.data.polygons:p.use_smooth=True
 o.modifiers.new('Pillow softening','SUBSURF').levels=1
 seam=curve(name+' piped seam',[(verts[i][0],verts[i][1],0) for i in perimeter],.004,material,True);seam.location=loc;seam.rotation_euler=o.rotation_euler
 return o
pillow('Plump silk pillow left',(-.03,1.93,1.11),.87,.66,.16,silk,.20,-.055)
pillow('Plump silk pillow right',(.91,1.90,1.13),.87,.67,.18,silk,.16,.075)
pillow('Rose soft accent pillow',(.03,1.59,1.25),.61,.55,.16,rose_silk,1.12,-.13)
pillow('Sage soft accent pillow',(.89,1.65,1.26),.57,.53,.15,sage,1.09,.06)
# Draped silk coverlet lays on the padded duvet without intersecting it.
verts=[];faces=[];nx=96;ny=40
for j in range(ny+1):
 y=-.62+.86*j/ny
 for i in range(nx+1):
  x=.45+(i/nx-.5)*2.46
  verts.append((x,y,duvet_height(x,y)+.062+.009*sin(x*10+y*4)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
o=mesh('Silk rose coverlet',verts,faces,rose_silk)
for p in o.data.polygons:p.use_smooth=True
o.modifiers.new('Silk smooth folds','SUBSURF').levels=1
o.modifiers.new('Silk hem thickness','SOLIDIFY').thickness=.009

# Move existing desk props to a new larger organic writing table.
group('06')
for o in collections['06'].objects:
 o.location.x+=.80;o.location.y-=1.55
for o in collections['06'].objects[:]:
 if any(t in o.name for t in ['Journalism_Desk','Desk tapered leg','Desk drawer','Drawer brass handle']):remove(o)
dx=-1.55;dy=-2.67
pts=[]
for i in range(128):
 a=2*pi*i/128
 r=1+.065*sin(3*a+.7)+.043*cos(5*a-.4)
 x=dx+1.45*cos(a)*r;y=dy+.66*sin(a)*r
 # shallow curved indentation at the seated side
 y+=.13*exp(-((a-1.5*pi)/.38)**2)
 pts.append((x,y,.87))
o=mesh('Journalism_Desk',pts,[tuple(range(128))],walnut)
mod=o.modifiers.new('Solid organic tabletop','SOLIDIFY');mod.thickness=.09;mod.offset=-1
mod=o.modifiers.new('Soft rounded table edge','BEVEL');mod.width=.028;mod.segments=4
o.modifiers.new('Table weighted normals','WEIGHTED_NORMAL')
for x,y in [(dx-1.03,dy-.34),(dx+1.03,dy-.34),(dx-1.00,dy+.34),(dx+1.00,dy+.34)]:
 rod('Organic desk oak leg',(x,y,.055),(x,y,.78),.053,walnut)
# Chair is kept inside the larger room, with space behind the desktop.
for o in named('Chair '):o.location.y-=.10
# Printed documents and open newspaper sheets with column layouts.
ink=mat('Newspaper ink',(.12,.135,.14),.9)
news_paper=mat('Warm newsprint',(.78,.75,.65),.92)
white_paper=mat('Document paper',(.87,.85,.78),.92)
def printed_page(name,x,y,z,w,h,material,angle=0,news=False):
 parent=bpy.data.objects.new(name,None);current.objects.link(parent);parent.location=(x,y,z);parent.rotation_euler.z=angle
 def part(obj):obj.parent=parent;return obj
 part(cube(name+' sheet',(0,0,0),(w,h,.0017),material,.004))
 # typographic blocks intentionally contain no invented personal information.
 part(cube(name+' headline',(0,h*.35,.002),(w*.82,.018,.001),ink))
 part(cube(name+' divider',(0,h*.29,.002),(w*.87,.0016,.001),ink))
 columns=3 if news else 1
 for col in range(columns):
  xx=-w*.42+(col+.5)*w*.84/columns
  for line in range(18):
   yy=h*.22-line*h*.028
   length=w*.84/columns*random.uniform(.63,.91)
   part(cube(name+' text column',(xx,yy,.002),(length,.0013,.001),ink))
 if news:
  part(cube(name+' photo block',(-w*.27,-h*.31,.002),(w*.22,h*.19,.001),sage))
 return parent
for k in range(5):printed_page('Research document %02d'%k,dx+.74,dy+.23,.890+k*.0025,.34,.47,white_paper,.06+k*.013)
printed_page('Newspaper left page',dx-.60,dy-.09,.897,.38,.51,news_paper,-.16,True)
printed_page('Newspaper right page',dx-.23,dy-.15,.899,.38,.51,news_paper,-.16,True)
# A loose marked-up sheet near the laptop.
printed_page('Interview notes sheet',dx+.28,dy-.31,.899,.26,.34,white_paper,.17)
# Fine brass eyeglasses laid on the documents.
gx=dx+.78;gy=dy+.09;gz=.921
for side in [-1,1]:
 points=[(gx+side*.064+.050*cos(2*pi*i/64),gy+.039*sin(2*pi*i/64),gz) for i in range(65)]
 curve('Eyeglasses round brass rim',points,.0026,gold,True)
 ob=mesh('Eyeglasses clear lens',[(gx+side*.064+.047*cos(2*pi*i/64),gy+.036*sin(2*pi*i/64),gz) for i in range(64)],[tuple(range(64))],glass)
curve('Eyeglasses bridge',[(gx-.015,gy,gz),(gx,gy+.012,gz+.006),(gx+.015,gy,gz)],.0026,gold)
for side in [-1,1]:curve('Eyeglasses temple',[(gx+side*.115,gy,gz),(gx+side*.12,gy+.12,gz+.005),(gx+side*.10,gy+.145,gz+.003)],.0026,gold)

# Sofa zone on the expanded right side. Sculpted cushions use the pillow mesh.
c=bpy.data.collections.new('11 • Sofa & living area');bpy.context.scene.collection.children.link(c);current=c
sofa_cloth=mat('Warm ivory boucle sofa',(.70,.66,.56),.92);texture(sofa_cloth,170,.16,.018)
sx=3.69;sy=-.48
cube('Sofa upholstered base',(sx,sy,.37),(1.16,2.48,.34),sofa_cloth,.15)
cube('Sofa soft back',(sx+.46,sy,.82),(.27,2.41,.86),sofa_cloth,.125)
for y in [sy-1.15,sy+1.15]:cube('Sofa rounded arm',(sx-.04,y,.64),(1.17,.27,.49),sofa_cloth,.12)
for y in [sy-.55,sy+.55]:
 pillow('Sofa plush seat',(sx-.05,y,.64),.91,1.04,.12,sofa_cloth)
 ob=pillow('Sofa plump back cushion',(sx+.29,y,.91),1.02,.66,.15,sofa_cloth,1.13)
 ob.rotation_euler=(1.18,0,pi/2)
for x in [sx-.43,sx+.41]:
 for y in [sy-1.03,sy+1.03]:cyl('Sofa walnut foot',(x,y,.13),.04,.20,walnut)
ob=pillow('Sofa pink scatter cushion',(sx-.13,sy+.65,.89),.47,.47,.14,rose_silk,1.1,-.3);ob.rotation_euler=(1.12,0,pi/2+.15)
ob=pillow('Sofa sage scatter cushion',(sx-.14,sy-.57,.89),.43,.46,.13,sage,1.0,.2);ob.rotation_euler=(1.10,0,pi/2-.15)
# Small rounded coffee table in front of sofa, preserving a walkable gap.
o=cyl('Sofa coffee table top',(2.46,sy-.15,.48),.43,.055,walnut,64);o.scale.y=1.26
for a in [0,2*pi/3,4*pi/3]:rod('Coffee table leg',(2.46+.29*cos(a),sy-.15+.32*sin(a),.06),(2.46+.29*cos(a),sy-.15+.32*sin(a),.45),.024,walnut)
cube('Coffee table book',(2.43,sy-.13,.53),(.25,.33,.035),bpy.data.materials['Book cloth 1'],.006)
# Reposition violin clear of bed/sofa paths.
for o in collections['07'].objects:o.location.y-=.43

# Cameras frame the expanded room; retain detail and interior views.
scene=bpy.context.scene
cam=bpy.data.objects['Camera • Room overview'];cam.location=(12,-16,11.5);target=Vector((.55,-.40,1.15));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=13.5
scene.camera=cam
cam=bpy.data.objects['Camera • Immersive interior'];cam.location=(4.1,-6.8,2.55);cam.rotation_euler=(Vector((-.1,1,1.35))-cam.location).to_track_quat('-Z','Y').to_euler()
group('10')
data=bpy.data.cameras.new('Camera • Silk bed detail');cam=bpy.data.objects.new('Camera • Silk bed detail',data);current.objects.link(cam);cam.location=(3.4,-3.6,3.4);cam.rotation_euler=(Vector((.45,.8,.9))-cam.location).to_track_quat('-Z','Y').to_euler();data.lens=50
scene.render.resolution_x=1600;scene.render.resolution_y=1280;scene.cycles.samples=48
scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
scene['Revision']='v2 — fluffy silk bedding, no fireplace, larger organic desk with documents/newspapers/eyeglasses, expanded room and sofa'
scene['Room dimensions']='8.3 m x 7.4 m; open-front cutaway'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
bpy.ops.render.render(write_still=True)
print('REVISED_ROOM_COMPLETE',len(bpy.data.objects))
