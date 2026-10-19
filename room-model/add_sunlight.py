import bpy,os
from mathutils import Vector
OUT='/private/tmp/katy-room-v9';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
s=bpy.context.scene;s.frame_set(1)
sun=bpy.data.objects['Afternoon sunlight'];sun.data.energy=3.0;sun.data.color=(1.0,.83,.62);sun.data.angle=.022
# Low side light enters through the window instead of falling through the cutaway roof.
direction=Vector((1,.22,-.42));sun.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
bpy.data.objects['Window daylight'].data.energy=160
bpy.data.objects['Soft front fill'].data.energy=145
bpy.data.objects['Ceiling soft bounce'].data.energy=85
s.world.node_tree.nodes['Background'].inputs[1].default_value=.14

# Camera-invisible architectural blockers ensure direct sunlight really passes through
# the glass opening and casts the actual grid bars onto the floor and bedding.
col=bpy.data.collections.new('12 • Sunlight blockers — render only');s.collection.children.link(col)
material=bpy.data.materials['Warm ivory plaster']
def blocker(name,loc,dim):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.data.materials.append(material)
 o.visible_camera=False;o.visible_diffuse=False;o.visible_glossy=False;o.visible_transmission=False;o.visible_shadow=True
 o.display_type='WIRE';o.hide_set(True);o['Purpose']='Render-only sunlight blocker; exclude from interactive room exports'
 return o
blocker('Sun blocker • ceiling',(1.45,-.70,3.84),(10.05,7.55,.06))
blocker('Sun blocker • front opening',(1.45,-4.45,1.90),(10.05,.06,3.80))
blocker('Sun blocker • right opening',(6.45,-.70,1.90),(.06,7.55,3.80))
s['Lighting']='Warm low afternoon sunlight through actual transparent grid windows; camera-invisible roof/front/right blockers prevent cutaway light leaks'
s.camera=bpy.data.objects['Camera • Room overview'];s.render.resolution_x=1440;s.render.resolution_y=1152;s.cycles.samples=64;s.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
bpy.ops.render.render(write_still=True)
print('SUNLIGHT_COMPLETE')
