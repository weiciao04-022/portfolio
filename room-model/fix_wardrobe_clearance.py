import bpy,os
from mathutils import Vector

OUT='/private/tmp/katy-room-v7';os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/weiciao/Desktop/work/Katy_Parisian_Room.blend')
scene=bpy.context.scene
# Shift the complete wardrobe, including door pivots, 0.50 m away from the window.
# Child door details inherit the hinge translation exactly once.
for ob in bpy.data.objects:
 if ob.name.startswith('Wardrobe') and ob.parent is None:ob.location.x+=.50
bpy.context.view_layer.update()

def bounds(ob,depsgraph):
 evaluated=ob.evaluated_get(depsgraph)
 if ob.type=='CURVE':
  geometry=evaluated.to_mesh()
  points=[evaluated.matrix_world@v.co for v in geometry.vertices]
  evaluated.to_mesh_clear()
  return points
 return [evaluated.matrix_world@Vector(c) for c in evaluated.bound_box]
curtains=[o for o in bpy.data.objects if o.name.startswith('Full-length gathered curtain')]
left_hinge=bpy.data.objects['WardrobeDoor_Left_Hinge']
right_hinge=bpy.data.objects['WardrobeDoor_Right_Hinge']
left_parts=[o for o in left_hinge.children if o.type in {'MESH','CURVE'}]
right_parts=[o for o in right_hinge.children if o.type in {'MESH','CURVE'}]
bed=bpy.data.objects['Fluffy silk duvet — refined fabric']
minimum_curtain_clearance=float('inf');minimum_bed_clearance=float('inf')
for frame in range(1,81):
 scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 curtain_max_x=max(v.x for o in curtains for v in bounds(o,deps))
 door_min_x=min(v.x for o in left_parts for v in bounds(o,deps))
 bed_min_x=min(v.x for v in bounds(bed,deps))
 right_max_x=max(v.x for o in right_parts for v in bounds(o,deps))
 clearance=door_min_x-curtain_max_x;bed_clearance=bed_min_x-right_max_x
 # Non-overlapping X bounds prove these meshes cannot intersect, at any sampled frame.
 assert clearance>.08,(frame,clearance)
 assert bed_clearance>.05,(frame,bed_clearance)
 minimum_curtain_clearance=min(minimum_curtain_clearance,clearance)
 minimum_bed_clearance=min(minimum_bed_clearance,bed_clearance)
print('VERIFIED_ALL_80_FRAMES', 'curtain clearance',round(minimum_curtain_clearance,3),'m','bed clearance',round(minimum_bed_clearance,3),'m')
scene['Wardrobe collision validation']='All 80 integer frames: left door and details clear of curtains; right door and details clear of duvet. Evaluated geometry bounding boxes tested.'
scene['Wardrobe minimum curtain clearance (m)']=minimum_curtain_clearance
scene['Wardrobe minimum bed clearance (m)']=minimum_bed_clearance
scene.frame_set(1);scene.camera=bpy.data.objects['Camera • Room overview']
scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Katy_Parisian_Room.blend')
scene.frame_set(40);scene.cycles.samples=48;scene.render.resolution_x=1200;scene.render.resolution_y=960
scene.render.filepath=OUT+'/Katy_Wardrobe_Open_Preview.png';bpy.ops.render.render(write_still=True)
scene.frame_set(1);scene.render.filepath=OUT+'/Katy_Parisian_Room_Preview.png';bpy.ops.render.render(write_still=True)
print('WARDROBE_CLEARANCE_FIXED')
