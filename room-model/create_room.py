import bpy, math, random, os
from mathutils import Vector
from math import sin, cos, pi

random.seed(22)
OUT='/private/tmp/katy-room'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection': bpy.data.collections.remove(c)
base=bpy.data.collections.get('Collection');base.name='00 • Architecture'
collections={}
for name in ['01 • Oak parquet','02 • French window','03 • Bed & linen','04 • Fireplace & mirror','05 • Bookshelf — About','06 • Writing desk — Journalism','07 • Violin — Life','08 • Plants & flowers','09 • Lighting','10 • Cameras']:
    c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c);collections[name[:2]]=c
current=base
def group(key):
    global current
    current=base if key=='00' else collections[key]
def place(obj,name):
    obj.name=name
    for c in list(obj.users_collection):c.objects.unlink(obj)
    current.objects.link(obj)
    return obj
def mat(name,color,rough=.5,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m
def texture(m,scale=55,strength=.1,distance=.02):
    n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=2
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=distance;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
def cube(name,loc,dim,material,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=place(bpy.context.object,name);o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if material:o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new('Soft edge','BEVEL');mod.width=bevel;mod.segments=3
        mod=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def sphere(name,loc,scale,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc);o=place(bpy.context.object,name);o.scale=scale
    o.data.materials.append(material)
    for p in o.data.polygons:p.use_smooth=True
    return o
def cyl(name,loc,r,depth,material,verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=loc);o=place(bpy.context.object,name);o.data.materials.append(material)
    m=o.modifiers.new('Edge radius','BEVEL');m.width=min(.014,r*.15);m.segments=3
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def rod(name,a,b,r,material):
    a,b=Vector(a),Vector(b);o=cyl(name,(a+b)/2,r,(b-a).length,material,16);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def curve(name,points,r,material,closed=False):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=16;data.bevel_depth=r;data.bevel_resolution=3
    spl=data.splines.new('POLY');spl.points.add(len(points)-1)
    for p,co in zip(spl.points,points):p.co=(*co,1)
    spl.use_cyclic_u=closed;o=bpy.data.objects.new(name,data);current.objects.link(o);o.data.materials.append(material);return o
def ring(name,loc,r,material,axis='Z',tube=.014):
    points=[]
    for i in range(65):
        a=2*pi*i/64
        points.append((loc[0]+r*cos(a),loc[1]+r*sin(a),loc[2]) if axis=='Z' else (loc[0]+r*cos(a),loc[1],loc[2]+r*sin(a)))
    return curve(name,points,tube,material,True)
def mesh(name,verts,faces,material):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new(name,m);current.objects.link(o);o.data.materials.append(material);return o
cream=mat('Warm ivory plaster',(.79,.755,.68),.85);texture(cream,140,.12,.013)
trim=mat('Painted moulding · porcelain',(.92,.885,.80),.38)
gold=mat('Aged brass',(.52,.31,.105),.28,.78)
walnut=mat('Walnut furniture',(.16,.075,.039),.4);texture(walnut,12,.16,.045)
linen=mat('Washed ivory linen',(.90,.86,.75),.92);texture(linen,170,.2,.025)
rose=mat('Dusty rose velvet',(.47,.245,.24),.8);texture(rose,120,.13,.012)
pink=mat('Blush cushion',(.69,.45,.41),.87);texture(pink,140,.2,.02)
sage=mat('Sage upholstery',(.30,.38,.29),.88);texture(sage,140,.15,.02)
dark=mat('Dark iron',(.026,.032,.031),.4,.55)
marble=mat('Warm marble',(.79,.76,.68),.26)
n=marble.node_tree.nodes;l=marble.node_tree.links;p=n.get('Principled BSDF');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Roughness'].default_value=.8
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.45;ramp.color_ramp.elements[0].color=(.67,.64,.58,1);ramp.color_ramp.elements[1].position=.54;ramp.color_ramp.elements[1].color=(.86,.83,.76,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
leafmat=mat('Leaf · deep olive',(.095,.20,.072),.65)
potmat=mat('Terracotta ceramic',(.46,.22,.13),.6)
paper=mat('Book pages',(.83,.78,.64),.9)
bookmats=[mat('Book cloth '+str(i),c,.82) for i,c in enumerate([(.17,.25,.30),(.49,.22,.18),(.58,.45,.30),(.30,.39,.29),(.68,.60,.45),(.28,.20,.25),(.66,.48,.44)])]

# Open-front architectural shell, 7 m x 6 m. All dimensions are metres.
group('00')
cube('Floor foundation',(0,0,-.12),(7.15,6.15,.22),walnut,.035)
cube('Back plaster wall',(0,3.05,1.9),(7.15,.18,3.8),cream,.015)
# Left wall has an actual opening for a two-leaf French window.
for y,w in [(-2.275,1.45),(2.125,1.75)]:cube('Window side wall',(-3.55,y,1.9),(.18,w,3.8),cream,.01)
cube('Window lintel',(-3.55,-.15,3.49),(.18,2.95,.62),cream,.01)
cube('Window lower wall',(-3.55,-.15,.24),(.18,2.95,.48),cream,.01)
for z,height,depth in [(.12,.18,.10),(.29,.05,.07),(3.45,.10,.12),(3.56,.09,.18),(3.67,.12,.24)]:
    cube('Back skirting / cornice',(0,2.91,z),(7,height if False else depth,height),trim,.015)
    cube('Left skirting / cornice',(-3.41,0,z),(depth,6,height),trim,.015)
# Decorative panel mouldings on the back wall.
def panel_back(name,cx,z,w,h):
    for delta in [0,.047]:
        pts=[(cx-w/2+delta,2.938,z-h/2+delta),(cx+w/2-delta,2.938,z-h/2+delta),(cx+w/2-delta,2.938,z+h/2-delta),(cx-w/2+delta,2.938,z+h/2-delta)]
        curve(name,pts,.016 if delta==0 else .007,trim,True)
for x,w in [(-2.1,1.95),(.18,2.05),(2.35,1.72)]:panel_back('French wall panel',x,1.92,w,2.62)
for y in [-2.24,2.12]:
    pts=[(-3.43,y-.53,.68),(-3.43,y+.53,.68),(-3.43,y+.53,3.12),(-3.43,y-.53,3.12)]
    curve('Left wall panel',pts,.017,trim,True)

# Individually editable, clipped herringbone oak blocks.
group('01')
woods=[]
for i in range(10):
    v=random.uniform(.85,1.17);m=mat('Oak plank tone %02d'%i,(.31*v,.16*v,.066*v),.42)
    nodes=m.node_tree.nodes;links=m.node_tree.links;bs=nodes.get('Principled BSDF');tex=nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4;tex.inputs['Detail'].default_value=3
    tc=nodes.new('ShaderNodeTexCoord');mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1,32,7)
    links.new(tc.outputs['Generated'],mapping.inputs[0]);links.new(mapping.outputs[0],tex.inputs['Vector'])
    ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.12*v,.055*v,.020*v,1);ramp.color_ramp.elements[1].color=(.42*v,.235*v,.103*v,1)
    links.new(tex.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],bs.inputs['Base Color']);woods.append(m)
def clip(poly,axis,bound,less):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        ia=a[axis]<=bound if less else a[axis]>=bound;ib=b[axis]<=bound if less else b[axis]>=bound
        if ia:out.append(a)
        if ia!=ib:
            t=(bound-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[j]+t*(b[j]-a[j]) for j in range(2)))
    return out
L=.70;W=.14
for i in range(-20,21):
 for j in range(-20,21):
  ax=i*L-j*W;ay=i*L+j*W
  for ori in [0,1]:
   if ori==0:rect=[(ax+.003,ay+.003),(ax+L-.003,ay+.003),(ax+L-.003,ay+W-.003),(ax+.003,ay+W-.003)]
   else:rect=[(ax+L+.003,ay+.003),(ax+L+W-.003,ay+.003),(ax+L+W-.003,ay+L-.003),(ax+L+.003,ay+L-.003)]
   poly=[((x-y)*.7071,(x+y)*.7071) for x,y in rect]
   for axis,bound,less in [(0,3.48,True),(0,-3.48,False),(1,2.98,True),(1,-2.98,False)]:
       if poly:poly=clip(poly,axis,bound,less)
   if len(poly)<3:continue
   o=mesh('Oak herringbone block',[(x,y,.013) for x,y in poly],[tuple(range(len(poly)))],random.choice(woods))
   mod=o.modifiers.new('Plank thickness','SOLIDIFY');mod.thickness=.024
   mod=o.modifiers.new('Plank edges','BEVEL');mod.width=.003;mod.segments=1

# French window, sheer curtains and small outside balcony.
group('02')
for y in [-1.55,1.25]:cube('Window outer casing',(-3.40,y,1.8),(.13,.105,2.82),trim,.018)
for z in [.46,3.15]:cube('Window outer casing',(-3.40,-.15,z),(.13,2.90,.12),trim,.015)
cube('Deep window sill',(-3.32,-.15,.50),(.46,2.95,.075),marble,.018)
for y in [-1.47,-.15,1.17]:cube('French window vertical frame',(-3.5,y,1.81),(.11,.065,2.58),trim,.01)
for z in [.56,1.45,2.32,3.07]:cube('French window horizontal frame',(-3.5,-.15,z),(.11,2.7,.055),trim,.009)
glass=mat('Clear window glass',(.78,.87,.91),.07)
glass.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.96
glass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.45
cube('Window glazing',(-3.555,-.15,1.81),(.012,2.65,2.49),glass)
for y in [-.22,-.08]:rod('Brass window handle',(-3.39,y,1.60),(-3.39,y,1.77),.016,gold)
cube('Balcony paving',(-4.00,-.15,.34),(.9,2.95,.15),cream,.02)
rod('Balcony rail top',(-4.38,-1.56,1.39),(-4.38,1.25,1.39),.028,dark)
for y in [-1.5+k*.21 for k in range(14)]:
 rod('Balcony baluster',(-4.38,y,.45),(-4.38,y,1.38),.012,dark)
 curve('Balcony curl',[(-4.38,y+.06*cos(t),.96+.14*sin(t)) for t in [k*2*pi/32 for k in range(33)]],.01,dark)
sheer=mat('Sheer warm-white curtain',(.9,.87,.80),1)
sheer.node_tree.nodes.get('Principled BSDF').inputs['Subsurface Weight'].default_value=.12
texture(sheer,150,.18,.014)
rod('Curtain pole',(-3.16,-1.85,3.28),(-3.16,1.57,3.28),.027,gold)
for side,cy in enumerate([-1.32,1.03]):
 verts=[];faces=[];nx=32;nz=35
 for iz in range(nz+1):
  z=.53+2.69*iz/nz
  for ix in range(nx+1):
   t=ix/nx;y=cy+(t-.5)*.82
   x=-3.08+.07*sin(t*pi*14)+.04*sin(iz/nz*pi)
   verts.append((x,y,z+.012*sin(t*pi*14)))
 for iz in range(nz):
  for ix in range(nx):
   a=iz*(nx+1)+ix;faces.append((a,a+1,a+nx+2,a+nx+1))
 o=mesh('Pleated linen curtain '+str(side),verts,faces,sheer)
 for p in o.data.polygons:p.use_smooth=True
 mod=o.modifiers.new('Fine cloth thickness','SOLIDIFY');mod.thickness=.003
 for y in [cy-.38+k*.09 for k in range(9)]:ring('Curtain brass ring',(-3.16,y,3.28),.041,gold,'Y',.006)

# Dusty rose upholstered bed, cloth surfaces and cushions.
group('03')
cube('Bed oak base',(.45,.98,.29),(1.9,2.66,.32),walnut,.055)
for x in [-.34,1.24]:
 for y in [-.12,2.05]:cyl('Bed turned foot',(x,y,.15),.06,.30,walnut)
cube('Mattress',(.45,.98,.53),(1.85,2.57,.26),linen,.105)
head=cube('Rose upholstered headboard',(.45,2.43,1.06),(1.99,.20,1.68),rose,.19)
for x in [-.36,.04,.45,.86,1.26]:
 for z in [.57,.91,1.25,1.59]:sphere('Headboard tuft button',(x,2.313,z),(.025,.012,.025),rose)
def cushion(name,loc,dim,material,angle=0):
 o=cube(name,loc,dim,material,min(dim)*.44);o.rotation_euler[2]=angle
 sub=o.modifiers.new('Pillow smoothing','SUBSURF');sub.levels=2
 for p in o.data.polygons:p.use_smooth=True
 return o
cushion('Linen pillow left',(-.03,1.92,.82),(.86,.57,.21),linen,-.04)
cushion('Linen pillow right',(.89,1.90,.84),(.86,.57,.23),linen,.055)
cushion('Blush accent pillow',(.04,1.74,1.02),(.62,.29,.45),pink,-.12)
cushion('Sage accent pillow',(.91,1.76,.98),(.55,.27,.37),sage,.08)
# Duvet continues over the foot and both sides; editable subdivided mesh.
verts=[];faces=[];nx=64;ny=84
for j in range(ny+1):
 t=j/ny;y=-.62+2.38*t
 for i in range(nx+1):
  u=i/nx;x=.45+(u-.5)*2.28
  edge=max(0,abs(x-.45)-.82)
  foot=max(0,-.29-y)
  z=.75-edge*1.4-foot*1.55
  z+=.025*sin(x*18+y*6)+.014*sin(y*25+x*7)+.018*sin(x*35-y*9)
  z+=.028*cos((x-.45)*4)*sin(t*pi)
  verts.append((x,y,max(.10,z)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
o=mesh('Draped ivory duvet',verts,faces,linen)
for p in o.data.polygons:p.use_smooth=True
mod=o.modifiers.new('Soft cloth','SUBSURF');mod.levels=1
mod=o.modifiers.new('Fabric thickness','SOLIDIFY');mod.thickness=.007
throw=mat('Rose cotton throw',(.44,.24,.21),.95);texture(throw,170,.25,.02)
verts=[];faces=[]
for j in range(25):
 for i in range(49):
  x=.45+(i/48-.5)*2.3;y=-.35+j/24*.72;edge=max(0,abs(x-.45)-.82)
  t=(y+.62)/2.38
  z=.75-edge*1.4-max(0,-.29-y)*1.55+.025*sin(x*18+y*6)+.014*sin(y*25+x*7)+.018*sin(x*35-y*9)+.028*cos((x-.45)*4)*sin(t*pi)+.035
  verts.append((x,y,z))
for j in range(24):
 for i in range(48):
  a=j*49+i;faces.append((a,a+1,a+50,a+49))
o=mesh('Rose throw across bed foot',verts,faces,throw)
for p in o.data.polygons:p.use_smooth=True
o.modifiers.new('Throw thickness','SOLIDIFY').thickness=.006
for x in [-.88+k*.05 for k in range(47)]:
 y=-.35;t=(y+.62)/2.38
 z=.75-max(0,abs(x-.45)-.82)*1.4-max(0,-.29-y)*1.55+.025*sin(x*18+y*6)+.014*sin(y*25+x*7)+.018*sin(x*35-y*9)+.028*cos((x-.45)*4)*sin(t*pi)+.035
 curve('Throw fringe',[(x,-.35,z),(x+.013,-.42,z-.025),(x,-.45,z-.05)],.003,throw)
# Rug: woven neutral body and decorative restrained border.
rugmat=mat('Woven vintage rug',(.50,.43,.33),1);texture(rugmat,180,.35,.025)
cube('Vintage wool rug',(.25,-.25,.047),(3.3,3.68,.038),rugmat,.015)
for w,h in [(3.14,3.51),(2.95,3.32),(2.87,3.24)]:curve('Rug border',[(-w/2+.25,-h/2-.25,.07),(w/2+.25,-h/2-.25,.07),(w/2+.25,h/2-.25,.07),(-w/2+.25,h/2-.25,.07)],.012,rose,True)
for x in [-1.03+k*.32 for k in range(9)]:
 for y in [-1.70+k*.34 for k in range(10)]:curve('Rug woven motif',[(x,y+.07,.072),(x+.06,y,.072),(x,y-.07,.072),(x-.06,y,.072)],.004,linen,True)
# Small bench at the bed foot.
cube('Foot bench frame',(.40,-1.34,.37),(1.48,.47,.10),walnut,.03)
cushion('Foot bench sage cushion',(.40,-1.34,.47),(1.52,.50,.15),sage)
for x in [-.23,1.03]:
 for y in [-1.50,-1.18]:rod('Bench leg',(x,y,.08),(x,y,.36),.035,walnut)

# Marble fireplace and arched antique brass mirror.
group('04')
fx=-2.08
cube('Fireplace black recess',(fx,2.90,.70),(1.14,.075,1.16),dark,.012)
for x in [fx-.63,fx+.63]:
 cube('Marble fireplace pilaster',(x,2.66,.66),(.25,.36,1.15),marble,.026)
 cube('Pilaster base',(x,2.66,.15),(.30,.40,.14),marble,.015)
 cube('Pilaster capital',(x,2.65,1.16),(.30,.41,.11),marble,.015)
cube('Mantel lintel',(fx,2.63,1.27),(1.61,.43,.20),marble,.025)
cube('Mantel shelf',(fx,2.60,1.40),(1.77,.52,.11),marble,.02)
cube('Marble hearth',(fx,2.59,.09),(1.67,.72,.10),marble,.02)
for x in [fx-.28,fx+.20]:
 o=cyl('Decorative firewood',(x,2.72,.29),.08,.52,walnut);o.rotation_euler[1]=pi/2;o.rotation_euler[2]=.18
for x in [fx-.42+k*.12 for k in range(8)]:rod('Fireplace grate',(x,2.40,.15),(x,2.40,.51),.012,dark)
def archpoints(cx,y,z,w,h,n=40):
 pts=[(cx-w/2,y,z),(cx+w/2,y,z),(cx+w/2,y,z+h-w/2)]
 for i in range(n+1):
  a=pi*i/n;pts.append((cx+w/2*cos(a),y,z+h-w/2+w/2*sin(a)))
 return pts
mirror=mat('Silver mirror',(.88,.88,.84),.065,1)
points=archpoints(fx,2.82,1.49,1.21,1.70)
mesh('Arched mirror glass',points,[tuple(range(len(points)))],mirror)
for offset,r in [(0,.036),(.07,.014),(-.06,.010)]:curve('Gilded arched mirror frame',archpoints(fx,2.78,1.49-offset,1.21+offset*2,1.70+offset*2),r,gold,True)
for j in range(7):
 a=j*pi/6
 sphere('Mirror crown ornament',(fx+.11*cos(a),2.76,3.25+.09*sin(a)),(.032,.019,.04),gold)
curve('Mirror crown flourish',[(fx-.19,2.76,3.20),(fx-.10,2.75,3.34),(fx,2.74,3.38),(fx+.10,2.75,3.34),(fx+.19,2.76,3.20)],.017,gold)

# Bookshelf with individually named books, future introduction interaction zone.
group('05')
bx=2.67;by=2.62
for x in [bx-.62,bx+.62]:cube('Bookcase side',(x,by,1.36),(.085,.42,2.60),trim,.016)
cube('Bookcase back',(bx,2.84,1.36),(1.32,.05,2.59),cream,.005)
for z in [.08,.53,1.02,1.51,2.00,2.52,2.69]:cube('Bookcase shelf',(bx,by,z),(1.34,.49,.075),trim,.012)
cube('Bookcase cornice',(bx,by,2.74),(1.46,.54,.10),trim,.018)
book_index=0
for shelf,z in enumerate([.56,1.05,1.54,2.03]):
 x=bx-.51
 for k in range(random.randint(7,11)):
  width=random.uniform(.055,.095);height=random.uniform(.23,.39);depth=.24
  if x+width>bx+.54:break
  cover=random.choice(bookmats);book_index+=1
  cube('About_Book_%02d'%book_index,(x+width/2,2.61,z+height/2),(width,depth,height),cover,.005)
  cube('Book page block',(x+width/2,2.60,z+height/2),(width*.70,depth*.93,height*.91),paper,.003)
  for zz in [z+.045,z+height-.048]:cube('Book spine gold band',(x+width/2,2.482,zz),(width*.76,.003,.008),gold)
  x+=width+.012
 # horizontal book stack at the free end
 if shelf in [0,2]:
  for k in range(3):cube('Book horizontal stack',(bx+.30,2.60,z+.028+k*.052),(.34,.26,.045),bookmats[(shelf+k)%7],.006)
# Framed blank cards: surfaces for user's own introduction content.
cube('Shelf personal frame',(bx+.30,2.59,1.26),(.32,.045,.37),gold,.012)
cube('Shelf personal frame paper',(bx+.30,2.56,1.26),(.27,.008,.32),paper,.003)

# Writing desk, laptop, notebook, camera, and chair.
group('06')
dx=-2.35;dy=-1.12
cube('Journalism_Desk',(dx,dy,.83),(1.40,.70,.09),walnut,.035)
for x in [dx-.59,dx+.59]:
 for y in [dy-.25,dy+.25]:rod('Desk tapered leg',(x,y,.06),(x,y,.80),.034,walnut)
cube('Desk drawer',(dx,dy-.02,.71),(1.17,.58,.15),walnut,.018)
rod('Drawer brass handle',(dx-.09,dy-.325,.71),(dx+.09,dy-.325,.71),.012,gold)
silver=mat('Laptop aluminium',(.37,.39,.38),.3,.65)
screen=mat('Laptop dark screen',(.045,.069,.075),.25)
o=cube('Digital_Laptop_base',(dx+.15,dy,.91),(.51,.35,.025),silver,.012)
o=cube('Digital_Laptop_screen',(dx+.15,dy+.15,1.085),(.51,.025,.33),silver,.013);o.rotation_euler[0]=math.radians(-12)
o=cube('Laptop screen inset',(dx+.15,dy+.133,1.085),(.47,.007,.28),screen,.006);o.rotation_euler[0]=math.radians(-12)
cube('Laptop keyboard',(dx+.15,dy+.025,.927),(.43,.20,.003),dark,.004)
for yy in [dy-.05+k*.033 for k in range(5)]:
 for xx in [dx-.04+k*.043 for k in range(9)]:cube('Laptop key',(xx,yy,.930),(.028,.018,.0015),silver,.002)
cube('Reporting_Notebook',(dx-.44,dy-.045,.902),(.28,.34,.029),bookmats[4],.009)
for xx in [dx-.51,dx-.40]:
 for yy in [dy-.13+k*.035 for k in range(6)]:cube('Notebook ruled line',(xx,yy,.919),(.085,.0015,.0007),sage)
rod('Brass pen',(dx-.40,dy-.21,.923),(dx-.27,dy+.01,.923),.006,gold)
cyl('Coffee saucer',(dx+.53,dy-.12,.893),.085,.012,trim)
cyl('Coffee cup',(dx+.53,dy-.12,.939),.055,.08,trim)
coffee=mat('Coffee',(.065,.028,.010),.18);cyl('Coffee surface',(dx+.53,dy-.12,.978),.047,.003,coffee)
curve('Cup handle',[(dx+.585+.03*sin(t),dy-.12,.94+.03*cos(t)) for t in [k*pi/24 for k in range(25)]],.007,trim)
cube('Photography_Camera',(dx-.33,dy+.21,.97),(.20,.105,.135),dark,.014)
o=cyl('Camera lens',(dx-.33,dy+.135,.97),.045,.08,dark);o.rotation_euler[0]=pi/2
# chair faces the desk, toward back/left
cx=-2.24;cy=-2.03
cushion('Chair sage seat',(cx,cy,.51),(.52,.51,.11),sage)
for x in [cx-.21,cx+.21]:
 for y in [cy-.21,cy+.21]:rod('Chair walnut leg',(x,y,.04),(x,y,.48),.025,walnut)
cushion('Chair sage back',(cx,cy-.23,.89),(.53,.09,.55),sage)
for x in [cx-.22,cx+.22]:rod('Chair back upright',(x,cy-.23,.49),(x,cy-.23,1.15),.022,walnut)

# Violin: a personal-interest prop with separate body, neck, strings and bow.
group('07')
vx=1.65;vy=-1.65
violin=mat('Violin varnished maple',(.34,.105,.032),.24);texture(violin,18,.10,.016)
# A shaped body outline in the XZ plane with waist cut-outs.
outline=[(-.00,-.32),(-.16,-.31),(-.22,-.22),(-.21,-.10),(-.115,-.01),(-.10,.06),(-.16,.12),(-.17,.20),(-.12,.29),(0,.32),(.12,.29),(.17,.20),(.16,.12),(.10,.06),(.115,-.01),(.21,-.10),(.22,-.22),(.16,-.31)]
verts=[(vx+x,vy+y,vz+.70) for y in [-.035,.035] for x,vz in outline];N=len(outline)
faces=[tuple(range(N-1,-1,-1)),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
o=mesh('Life_Violin_body',verts,faces,violin);mod=o.modifiers.new('Violin soft carved edge','BEVEL');mod.width=.024;mod.segments=3;o.modifiers.new('Violin normals','WEIGHTED_NORMAL')
curve('Violin purfling',[(vx+x*.94,vy-.038,.70+z*.95) for x,z in outline],.003,dark,True)
cube('Violin neck',(vx,vy,1.16),(.048,.047,.40),violin,.012)
cube('Violin fingerboard',(vx,vy-.035,1.105),(.047,.018,.43),dark,.008)
sphere('Violin scroll',(vx,vy,1.38),(.046,.033,.055),violin)
for z in [1.30,1.35]:rod('Violin tuning peg',(vx-.055,vy,z),(vx+.055,vy,z),.009,dark)
cube('Violin bridge',(vx,vy-.069,.68),(.087,.024,.047),paper,.005)
cube('Violin tailpiece',(vx,vy-.043,.48),(.065,.018,.14),dark,.012)
for x in [-.014,-.004,.004,.014]:rod('Violin string',(vx+x,vy-.058,.53),(vx+x,vy-.058,1.28),.0012,silver)
for side in [-1,1]:curve('Violin f hole',[(vx+side*.08,vy-.043,.61),(vx+side*.10,vy-.043,.66),(vx+side*.07,vy-.043,.75),(vx+side*.09,vy-.043,.80)],.006,dark)
rod('Violin bow',(vx+.29,vy,.43),(vx+.25,vy,1.40),.006,walnut)
rod('Bow horsehair',(vx+.28,vy-.025,.44),(vx+.24,vy-.025,1.38),.002,linen)
rod('Violin stand',(vx,vy+.07,.04),(vx,vy+.07,.68),.012,dark)
for x,y in [(vx-.2,vy-.10),(vx+.2,vy-.10),(vx,vy+.28)]:rod('Violin stand foot',(vx,vy+.07,.15),(x,y,.03),.012,dark)

# Plants and restrained flower arrangements.
group('08')
def plant(name,x,y,z,size=1):
 bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.16*size,radius2=.21*size,depth=.32*size,location=(x,y,z+.16*size));o=place(bpy.context.object,name+' ceramic pot');o.data.materials.append(potmat)
 cyl(name+' soil',(x,y,z+.315*size),.19*size,.01,dark)
 for k in range(9):
  a=2*pi*k/9+random.uniform(-.15,.15);height=random.uniform(.48,.93)*size
  tip=(x+.28*size*cos(a),y+.28*size*sin(a),z+.30*size+height)
  curve(name+' stem',[(x,y,z+.27*size),(x+.08*size*cos(a),y+.08*size*sin(a),z+.40*size),tip],.008*size,leafmat)
  for t in [.45,.70,1]:
   loc=(x+.28*size*cos(a)*t,y+.28*size*sin(a)*t,z+.30*size+height*t)
   o=sphere(name+' leaf',loc,(.075*size,.20*size,.015*size),leafmat);o.rotation_euler=(random.uniform(-.6,.6),.3,a)
plant('Window plant',-2.90,.83,.06,1.12)
plant('Bookcase plant',3.03,1.70,.05,.86)
plant('Shelf trailing plant',2.78,2.60,2.80,.30)
petal=mat('Rose petal',(.72,.46,.43),.7)
vase=mat('Ivory glazed vase',(.76,.72,.61),.22)
def flowers(name,x,y,z,scale=1):
 sphere(name+' vase',(x,y,z+.16*scale),(.12*scale,.12*scale,.18*scale),vase)
 cyl(name+' vase neck',(x,y,z+.31*scale),.066*scale,.13*scale,vase)
 for k in range(7):
  a=2*pi*k/7;xx=x+.15*scale*cos(a);yy=y+.15*scale*sin(a);zz=z+(.60+.07*sin(k*3))*scale
  rod(name+' stem',(x,y,z+.26*scale),(xx,yy,zz),.004*scale,leafmat)
  for j in range(6):
   aa=2*pi*j/6;sphere(name+' petal',(xx+.04*scale*cos(aa),yy+.04*scale*sin(aa),zz),(.05*scale,.035*scale,.038*scale),petal)
  sphere(name+' rose center',(xx,yy,zz+.022*scale),(.035*scale,.035*scale,.037*scale),pink)
flowers('Mantel roses',-2.64,2.52,1.46,.66)

# Side table with warm pleated lamp.
group('03')
cube('Bedside oak table',(1.70,1.92,.51),(.57,.55,.12),walnut,.024)
for x in [1.48,1.92]:
 for y in [1.70,2.14]:rod('Bedside leg',(x,y,.07),(x,y,.47),.027,walnut)
cube('Bedside lower shelf',(1.70,1.92,.22),(.50,.48,.05),walnut,.013)
for k in range(2):cube('Bedside reading book',(1.70,1.90,.28+k*.06),(.30,.23,.05),bookmats[k],.006)
group('09')
glow=mat('Warm luminous glass',(.98,.70,.34),.35)
bs=glow.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(1,.60,.24,1);bs.inputs['Emission Strength'].default_value=.6
cyl('Table lamp base',(1.70,1.92,.61),.12,.055,gold)
rod('Table lamp stem',(1.70,1.92,.63),(1.70,1.92,1.06),.020,gold)
verts=[];faces=[]
for z,r in [(.93,.23),(1.22,.13)]:
 for i in range(96):
  a=2*pi*i/96;rr=r+(.009 if i%2 else -.009);verts.append((1.70+rr*cos(a),1.92+rr*sin(a),z))
for i in range(96):faces.append((i,(i+1)%96,(i+1)%96+96,i+96))
o=mesh('Pleated table lamp shade',verts,faces,linen);o.modifiers.new('Shade cloth','SOLIDIFY').thickness=.004
sphere('Table lamp bulb',(1.70,1.92,1.02),(.043,.043,.065),glow)
def light(name,typ,loc,energy,color,size=1,target=None):
 data=bpy.data.lights.new(name,typ);data.energy=energy;data.color=color
 if typ=='AREA':data.shape='DISK';data.size=size
 if typ=='POINT':data.shadow_soft_size=size
 o=bpy.data.objects.new(name,data);current.objects.link(o);o.location=loc
 if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 return o
light('Bedside warm glow','POINT',(1.70,1.92,1.01),16,(1,.64,.36),.16)
# Parisian chandelier suspended in the open cutaway room.
chx=.18;chy=.20
cyl('Ceiling rose',(chx,chy,3.62),.29,.055,trim)
for r in [.12,.20,.27]:ring('Ceiling rose detail',(chx,chy,3.58),r,trim,tube=.013)
rod('Chandelier suspension',(chx,chy,3.58),(chx,chy,2.95),.015,gold)
sphere('Chandelier center',(chx,chy,2.96),(.095,.095,.12),gold)
for k in range(6):
 a=k*2*pi/6;xx=chx+.43*cos(a);yy=chy+.43*sin(a)
 points=[(chx,chy,2.96),(chx+.13*cos(a),chy+.13*sin(a),2.78),(chx+.33*cos(a),chy+.33*sin(a),2.77),(xx,yy,2.89)]
 curve('Chandelier curved arm',points,.016,gold)
 cyl('Candle brass cup',(xx,yy,2.90),.068,.033,gold)
 cyl('Chandelier candle',(xx,yy,2.98),.025,.14,linen)
 sphere('Chandelier flame',(xx,yy,3.074),(.023,.023,.045),glow)
 for z in [2.73,2.65]:sphere('Crystal drop',(xx,yy,z),(.022,.022,.05),glass)
 light('Chandelier candle light','POINT',(xx,yy,3.07),4,(1,.68,.40),.09)
ring('Chandelier lower ring',(chx,chy,2.83),.17,gold,tube=.01)

# Gallery frame above the bed: original abstract colour composition, no biography text.
group('00')
cube('Art gold frame',(.43,2.85,2.69),(.80,.055,.89),gold,.012)
cube('Art paper',(.43,2.816,2.69),(.72,.010,.81),paper,.003)
cube('Abstract art rose form',(.53,2.803,2.75),(.26,.010,.47),rose,.12)
cube('Abstract art sage form',(.29,2.799,2.59),(.22,.010,.25),sage,.09)
curve('Abstract art line',[(.14,2.787,2.42),(.38,2.787,2.50),(.41,2.787,2.78),(.61,2.787,2.91)],.008,gold)

# Studio background, daylight and editable camera rig.
group('09')
background=mat('Studio warm background',(.68,.69,.67),.9)
cube('Studio ground',(0,0,-.30),(200,200,.10),background)
light('Window daylight','AREA',(-5.5,-.50,3.8),650,(1,.89,.73),4.0,(0,.5,1.0))
light('Soft front fill','AREA',(1,-5,6.0),480,(.84,.90,1),5.0,(0,.8,1.0))
light('Ceiling soft bounce','AREA',(0,.8,5.4),250,(1,.90,.76),3.0,(0,.8,0))
sun=light('Afternoon sunlight','SUN',(-6,-3,7),1.5,(1,.86,.68),target=(0,1,0));sun.data.angle=.14
world=bpy.data.worlds.new('Soft daylight world');bpy.context.scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.68,.75,.86,1);world.node_tree.nodes['Background'].inputs[1].default_value=.25
group('10')
def camera(name,loc,target,lens=48,ortho=None):
 data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);current.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.lens=lens
 if ortho:data.type='ORTHO';data.ortho_scale=ortho
 return o
cam=camera('Camera • Room overview',(10,-13,10.0),(-.15,.25,1.25),ortho=11.7)
camera('Camera • Immersive interior',(3.0,-5.9,2.3),(-.65,1.7,1.55),lens=30)
camera('Camera • Bookshelf detail',(4.8,-.5,2.7),(2.55,2.5,1.5),lens=52)
scene=bpy.context.scene;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True
scene.render.resolution_x=1440;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=os.path.join(OUT,'Katy_Parisian_Room_Preview.png')
scene.view_settings.view_transform='AgX'
scene.render.film_transparent=False
scene.unit_settings.system='METRIC'
scene['Project']='Katy • Parisian eclectic room / introduction environment'
scene['Reference']='User supplied Pinterest screenshot, 2026-10-13. Original model; no external assets.'
scene['Interaction zones']='About_Book_* ; Journalism_Desk ; Digital_Laptop_* ; Photography_Camera ; Life_Violin_body'
scene['Notes']='First editable room model. No invented biographical copy. Open-front cutaway; no ceiling intentionally for web exploration. Interior and detail cameras provided.'
# Save a camera-framed material view for first opening in Blender.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active=None
os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Katy_Parisian_Room.blend'))
bpy.ops.render.render(write_still=True)
print('ROOM_COMPLETE',len(bpy.data.objects),'objects')
