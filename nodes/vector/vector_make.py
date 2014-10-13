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

import numpy as np

import bpy
from bpy.props import FloatVectorProperty

from node_tree import FlowCustomTreeNode


class FlowVecMakeNode(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowVecMakeNode '''
    bl_idname = 'FlowVecMakeNode'
    bl_label = 'VectorMake'
    bl_icon = 'OUTLINER_OB_EMPTY'

    tvec = FloatVectorProperty(size=3)

    def init(self, context):
        self.width = 220
        self.outputs.new('VectorSocket', "v out")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'tvec', text="")

    # def update(self):
    #     if not (len(self.outputs) == 1):
    #         return
    #     if not self.outputs[0].links:
    #         return

    #     self.process()

    def process(self):
        x, y, z = self.tvec[:]
        ftvec = np.array([x, y, z, 0])
        self.outputs[0].fset(ftvec)


def register():
    bpy.utils.register_class(FlowVecMakeNode)


def unregister():
    bpy.utils.unregister_class(FlowVecMakeNode)
