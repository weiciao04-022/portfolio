import bpy,ast,math,os
from math import pi,sin,cos
from mathutils import Vector,Matrix
from pathlib import Path

OUT='/private/tmp/katy-room-v3';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','cube','sphere','cyl','rod','curve','ring','mesh']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base=bpy.data.collections['00 • Architecture'];collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};current=base
cream=bpy.data.materials['Warm ivory plaster'];trim=bpy.data.materials['Painted moulding · porcelain'];gold=bpy.data.materials['Aged brass'];walnut=bpy.data.materials['Walnut furniture'];glass=bpy.data.materials['Clear window glass'];linen=bpy.data.materials['Washed ivory linen'];sheer=bpy.data.materials['Sheer warm-white curtain']
def remove(o):bpy.data.objects.remove(o,do_unlink=True)

# Replace the old window and wall below it with a true 5.3 m-wide floor-to-ceiling opening.
for o in collections['02'].objects[:]:remove(o)
for o in base.objects[:]:
 if o.name.startswith(('Window side wall','Window lintel','Window lower wall','Left wall panel','Left skirting / cornice')):remove(o)
group('00')
cube('Left front wall pier',(-3.55,-3.965,1.9),(.18,.87,3.8),cream,.01)
cube('Left rear wall pier',(-3.55,2.41,1.9),(.18,1.27,3.8),cream,.01)
cube('Floor window lintel',(-3.55,-.88,3.60),(.18,5.30,.40),cream,.01)
# Continuous crown at the top, short skirting only outside the glazing.
for z,h,d in [(3.45,.10,.12),(3.56,.09,.18),(3.67,.12,.24)]:cube('Left crown moulding',(-3.41,-.70,z),(d,7.40,h),trim,.015)
for y,length in [(-3.965,.87),(2.41,1.27)]:
 for z,h,d in [(.12,.18,.10),(.29,.05,.07)]:cube('Window pier skirting',(-3.41,y,z),(d,length,h),trim,.012)
group('02')
ymin=-3.50;ymax=1.75;bottom=.065;top=3.35
for y in [ymin,ymax]:cube('Floor window outer jamb',(-3.40,y,(bottom+top)/2),(.13,.10,top-bottom+.10),trim,.014)
for z in [bottom,top]:cube('Floor window top bottom frame',(-3.40,(ymin+ymax)/2,z),(.13,ymax-ymin+.12,.09),trim,.012)
for y in [ymin+(ymax-ymin)*k/3 for k in range(1,3)]:cube('Slim floor window mullion',(-3.47,y,(bottom+top)/2),(.10,.043,top-bottom),trim,.007)
for k in range(3):
 ya=ymin+(ymax-ymin)*k/3;yb=ymin+(ymax-ymin)*(k+1)/3
 cube('Full-height glass panel %d'%(k+1),(-3.53,(ya+yb)/2,(bottom+top)/2),(.014,yb-ya-.065,top-bottom-.09),glass)
cube('Flush floor window threshold',(-3.43,(ymin+ymax)/2,.048),(.29,ymax-ymin,.045),trim,.012)
for y in [ymin+(ymax-ymin)/3-.065,ymin+(ymax-ymin)/3+.065]:rod('Window brass handle',(-3.37,y,1.01),(-3.37,y,1.18),.013,gold)
rod('Full-width curtain rail',(-3.13,ymin-.18,3.46),(-3.13,ymax+.18,3.46),.021,gold)
# Drawn-back curtains keep the large glass expanse unobstructed.
for idx,cy in enumerate([ymin+.20,ymax-.20]):
 verts=[];faces=[];nx=36;nz=50
 for j in range(nz+1):
  z=.045+3.35*j/nz
  for i in range(nx+1):
   t=i/nx;y=cy+(t-.5)*.61
   x=-3.08+.048*sin(t*pi*18)+.025*sin(j/nz*pi)
   verts.append((x,y,z+.007*sin(t*pi*18)))
 for j in range(nz):
  for i in range(nx):
   a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
 ob=mesh('Full-length gathered curtain %d'%idx,verts,faces,sheer)
 for p in ob.data.polygons:p.use_smooth=True
 ob.modifiers.new('Sheer fabric thickness','SOLIDIFY').thickness=.003
 for k in range(8):ring('Curtain ring',(-3.13,cy-.28+k*.08,3.46),.038,gold,'Y',.005)

# Rotate the entire work zone: seated gaze points outward through the left window.
# Transform only root objects; printed pages and their children inherit the same rotation.
old=Vector((-1.55,-2.67,0));new=Vector((-2.48,-1.50,0))
transform=Matrix.Translation(new) @ Matrix.Rotation(pi/2,4,'Z') @ Matrix.Translation(-old)
for ob in collections['06'].objects:
 if ob.parent is None:ob.matrix_world=transform @ ob.matrix_world
bpy.data.objects['Journalism_Desk']['Facing']='Seated direction: -X, toward floor-to-ceiling window'

# Remove mirror completely, replacing it with a freestanding paneled wardrobe.
for ob in collections['04'].objects[:]:remove(ob)
collections['04'].name='04 • Wardrobe'
group('04')
wx=-2.09;wy=2.54;width=2.03;height=2.76
cabinet=mat('Wardrobe warm ivory paint',(.77,.74,.66),.39)
cube('Wardrobe cabinet body',(wx,wy,height/2+.10),(width,.66,height),cabinet,.035)
cube('Wardrobe bottom plinth',(wx,wy,.14),(width+.08,.72,.20),trim,.021)
cube('Wardrobe crown lower',(wx,wy,2.88),(width+.12,.73,.085),trim,.018)
cube('Wardrobe crown upper',(wx,wy,2.96),(width+.19,.78,.085),trim,.02)
for side in [-1,1]:
 x=wx+side*.499
 cube('Wardrobe paneled door',(x,2.183,1.49),(.973,.049,2.48),cabinet,.016)
 for offset,r in [(0,.015),(.035,.007)]:
  w=.77-offset*2;z0=.47+offset;z1=2.57-offset
  curve('Wardrobe raised door moulding',[(x-w/2,2.146,z0),(x+w/2,2.146,z0),(x+w/2,2.146,z1),(x-w/2,2.146,z1)],r,trim,True)
 hx=wx+side*.073
 rod('Wardrobe brass handle',(hx,2.113,1.34),(hx,2.113,1.57),.013,gold)
 for z in [1.34,1.57]:rod('Wardrobe handle mount',(hx,2.17,z),(hx,2.113,z),.008,gold)
cube('Wardrobe door center gap',(wx,2.146,1.49),(.012,.006,2.47),walnut,.002)

# Shift plant away from the new outward-facing workstation and clear wardrobe doors.
for ob in collections['08'].objects:
 if ob.name.startswith('Window plant'):ob.location.y+=.69
scene=bpy.context.scene
scene['Revision']='v3 — wide floor-to-ceiling window; desk and chair facing outdoors; mirror replaced by paneled wardrobe'
scene['Window dimensions']='5.25 m wide x 3.285 m high'
scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
scene.cycles.samples=48
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
bpy.ops.render.render(write_still=True)
print('V3_ROOM_COMPLETE')
