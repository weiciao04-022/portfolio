import bpy,ast,math,os
from math import pi,sin,cos
from mathutils import Vector
from pathlib import Path
OUT='/private/tmp/katy-room-v5';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
src=Path('/Users/weiciao/Desktop/school/113-2/portfolio/room-model/create_room.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['group','place','mat','texture','cube','sphere','cyl','rod','curve','ring','mesh']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base=bpy.data.collections['00 • Architecture'];collections={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};current=base
trim=bpy.data.materials['Painted moulding · porcelain'];gold=bpy.data.materials['Aged brass'];walnut=bpy.data.materials['Walnut furniture'];cream=bpy.data.materials['Wardrobe warm ivory paint'];linen=bpy.data.materials['Washed ivory linen'];sage=bpy.data.materials['Sage upholstery'];rose=bpy.data.materials['Dusty pink silk coverlet']

# Clear, thin glazing. Transparency keeps the outside visible without milky roughness.
clear=bpy.data.materials.new('Transparent clear window glass');clear.use_nodes=True;clear.diffuse_color=(.95,.98,1,.09)
n=clear.node_tree.nodes;n.clear();links=clear.node_tree.links
output=n.new('ShaderNodeOutputMaterial');transparent=n.new('ShaderNodeBsdfTransparent');glass=n.new('ShaderNodeBsdfGlass');glass.inputs['Color'].default_value=(.99,.995,1,1);glass.inputs['Roughness'].default_value=.015;glass.inputs['IOR'].default_value=1.45
mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.10;links.new(transparent.outputs[0],mix.inputs[1]);links.new(glass.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
clear['Notes']='Thin clear glazing, transparent transmission with subtle glass reflection'
for ob in collections['02'].objects:
 if ob.name.startswith('Full-height glass panel'):ob.data.materials.clear();ob.data.materials.append(clear)
group('02')
ymin=-3.50;ymax=1.75;bottom=.065;top=3.35
# Six columns and five rows of large rectangular panes.
for k in [1,3,5]:
 y=ymin+(ymax-ymin)*k/6
 cube('Window grid vertical bar',(-3.435,y,(top+bottom)/2),(.055,.028,top-bottom),trim,.006)
for k in range(1,5):
 z=bottom+(top-bottom)*k/5
 cube('Window grid horizontal bar',(-3.435,(ymin+ymax)/2,z),(.055,ymax-ymin,.030),trim,.006)
# Exterior landing: a simple architectural surface visible through the glass.
# No scenery, plants, or personal content is invented.
cube('Exterior stone landing',(-4.22,(ymin+ymax)/2,-.015),(1.42,ymax-ymin+.20,.08),mat('Exterior pale stone',(.72,.73,.71),.7),.015)

# The wardrobe becomes a hollow cabinet, not a solid box hidden by doors.
group('04');wx=-2.09;wy=2.54;width=2.03
old=bpy.data.objects.get('Wardrobe cabinet body')
if old:bpy.data.objects.remove(old,do_unlink=True)
body=bpy.data.objects.new('Wardrobe_Carcass',None);current.objects.link(body)
for x in [wx-width/2+.04,wx+width/2-.04]:cube('Wardrobe shell side',(x,wy,1.46),(.08,.66,2.73),cream,.016)
cube('Wardrobe shell back',(wx,2.84,1.46),(width-.15,.055,2.73),cream,.012)
cube('Wardrobe shell top',(wx,wy,2.79),(width,.66,.075),cream,.012)
cube('Wardrobe shell bottom',(wx,wy,.27),(width-.13,.62,.06),cream,.009)
for z in [.59,.94]:cube('Wardrobe inner shelf',(wx,wy,z),(width-.16,.54,.045),trim,.008)
rod('Wardrobe hanging rail',(wx-.87,2.54,2.35),(wx+.87,2.54,2.35),.018,gold)
# Simple garment placeholders make the open state visually understandable.
for idx,x in enumerate([wx-.62,wx-.20,wx+.24,wx+.63]):
 curve('Wardrobe hanger',[(x-.17,2.48,2.20),(x,2.48,2.30),(x+.17,2.48,2.20),(x-.17,2.48,2.20)],.009,walnut)
 curve('Wardrobe hanger hook',[(x,2.48,2.30),(x,2.48,2.40),(x+.032,2.48,2.43),(x+.056,2.48,2.40)],.007,gold)
 material=[linen,sage,rose,linen][idx]
 verts=[(x-.11,2.46,2.23),(x-.20,2.46,2.14),(x-.23,2.46,1.98),(x-.13,2.46,1.95),(x-.14,2.46,1.22),(x+.14,2.46,1.22),(x+.13,2.46,1.95),(x+.23,2.46,1.98),(x+.20,2.46,2.14),(x+.11,2.46,2.23)]
 ob=mesh('Wardrobe hanging garment placeholder',verts,[tuple(range(len(verts)))],material)
 ob.modifiers.new('Garment thickness','SOLIDIFY').thickness=.038
 mod=ob.modifiers.new('Garment soft edge','BEVEL');mod.width=.024;mod.segments=3;ob.modifiers.new('Garment normals','WEIGHTED_NORMAL')
for side in [-1,1]:
 for k in range(3):cube('Wardrobe folded garment placeholder',(wx+side*.47,2.48,.65+k*.083),(.50,.34,.074),[linen,rose,sage][k],.027)

# Separate hinge pivots with reversible animation. Handles and mouldings follow doors.
hinges={}
for side,label in [(-1,'Left'),(1,'Right')]:
 ob=bpy.data.objects.new('WardrobeDoor_'+label+'_Hinge',None);current.objects.link(ob);ob.empty_display_type='PLAIN_AXES';ob.empty_display_size=.16;ob.location=(wx+side*.986,2.183,1.49);hinges[side]=ob
 ob['Interaction']='Wardrobe_Open / Wardrobe_Close';ob['Open degrees']=105*side
bpy.context.view_layer.update()
for ob in list(current.objects):
 if ob.name.startswith(('Wardrobe paneled door','Wardrobe raised door moulding','Wardrobe brass handle','Wardrobe handle mount')):
  xs=[(ob.matrix_world@Vector(c)).x for c in ob.bound_box];center=(max(xs)+min(xs))/2;side=-1 if center<wx else 1
  world=ob.matrix_world.copy();ob.parent=hinges[side];ob.matrix_parent_inverse=hinges[side].matrix_world.inverted();ob.matrix_basis=world
for side,hinge in hinges.items():
 for frame,angle in [(1,0),(40,side*105),(80,0)]:
  hinge.rotation_euler.z=math.radians(angle);hinge.keyframe_insert(data_path='rotation_euler',index=2,frame=frame)
 hinge.animation_data.action.name='Wardrobe_'+('Left' if side<0 else 'Right')+'_OpenClose'
scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=80;scene.render.fps=24
scene.timeline_markers.clear();scene.timeline_markers.new('CLOSED / 關閉',frame=1);scene.timeline_markers.new('OPEN / 打開',frame=40);scene.timeline_markers.new('CLOSED / 關閉',frame=80)
scene['Revision']='v5 — clear grid windows; hollow wardrobe with left/right hinge animation'
scene['Animation instructions']='Frame 1: closed; frame 40: open; frame 80: closed. Door hinge objects and handles are separate; clothing is decorative placeholder geometry.'
scene.frame_set(1);scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
bpy.ops.render.render(write_still=True)
scene.frame_set(40);scene.render.filepath=OUT+'/Katy_Wardrobe_Open_Preview.png';bpy.ops.render.render(write_still=True)
print('V5_ROOM_COMPLETE')
