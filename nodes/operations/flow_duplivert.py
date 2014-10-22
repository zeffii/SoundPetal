# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from random import random
import numpy as np

import bpy
from bpy.props import StringProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FLowDupliOperator(bpy.types.Operator):
    bl_idname = 'node.flow_fdp_center_child'
    bl_label = "Center Child"

    name_child = StringProperty()

    def execute(self, context):
        ref = bpy.data.objects.get(self.name_child)
        if ref:
            ref.location = 0, 0, 0
            return {'FINISHED'}
        return {'CANCELLED'}


class FlowDuplivertOne(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowDuplivertOne , with extras i hope'''
    bl_idname = 'FlowDuplivertOne'
    bl_label = 'Duplivert Ugen'
    bl_icon = 'OUTLINER_OB_EMPTY'

    name_parent = StringProperty(
        description="obj's verts are used to duplicate child",
        update=updateSD)
    name_child = StringProperty(
        description="name of object to duplicate",
        update=updateSD)

    def init(self, context):
        self.inputs.new("FlowArraySocket", "Rotations")

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop_search(self, 'name_parent', bpy.data, 'objects', text='parent')

        if self.name_child and self.name_parent:
            ob = bpy.data.objects[self.name_parent]

            layout.prop(ob, "dupli_type", expand=True)

            if ob.dupli_type == 'FRAMES':
                split = layout.split()

                col = split.column(align=True)
                col.prop(ob, "dupli_frames_start", text="Start")
                col.prop(ob, "dupli_frames_end", text="End")

                col = split.column(align=True)
                col.prop(ob, "dupli_frames_on", text="On")
                col.prop(ob, "dupli_frames_off", text="Off")

                layout.prop(ob, "use_dupli_frames_speed", text="Speed")

            elif ob.dupli_type == 'VERTS':
                layout.prop(ob, "use_dupli_vertices_rotation", text="Rotation")

            elif ob.dupli_type == 'FACES':
                row = layout.row()
                row.prop(ob, "use_dupli_faces_scale", text="Scale")
                sub = row.row()
                sub.active = ob.use_dupli_faces_scale
                sub.prop(ob, "dupli_faces_scale", text="Inherit Scale")

            elif ob.dupli_type == 'GROUP':
                layout.prop(ob, "dupli_group", text="Group")

        col.prop_search(self, 'name_child', bpy.data, 'objects', text='child')
        col.separator()
        op_one = col.operator('node.flow_fdp_center_child', text='Center Child')
        op_one.name_child = self.name_child

    def process(self):
        objects = bpy.data.objects
        if self.name_parent and self.name_child:
            obj_parent = objects[self.name_parent]
            obj_child = objects[self.name_child]
            obj_child.parent = obj_parent

            print('does this!')
            if obj_child.use_dupli_vertices_rotation:
                print('should be rotatin')

                val = self.inputs['Rotations'].fget()
                if hasattr(val, 'any') and val.any():
                    verts = obj_parent.data.vertices
                    if not (len(val) == len(verts)):
                        print('sizes don\'t match')
                        print(len(val), len(verts))
                        return
                else:
                    print('no array')
                    return

                # only reaches here if they are the same size
                for v, norm in zip(verts, val):
                    print(norm[:3])
                    v.normal = norm[:3]
                    # v.normal = random(), random(), random()

                # race condition with bmesh node, this should be done last..
                # update is pointless I think..
                # obj_parent.data.update()


def register():
    bpy.utils.register_class(FlowDuplivertOne)
    bpy.utils.register_class(FLowDupliOperator)


def unregister():
    bpy.utils.unregister_class(FLowDupliOperator)
    bpy.utils.unregister_class(FlowDuplivertOne)
