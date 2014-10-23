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
from bpy.props import (
    IntProperty, BoolProperty, EnumProperty, StringProperty
)

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowArrayReShape(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowArrayReShape
    ==============

    flatten or unflatten array

    '''
    bl_idname = 'FlowArrayReShape'
    bl_label = 'Array ReShape'
    shape_str = StringProperty(description="repr of array.shape")

    def init(self, context):
        self.inputs.new('FlowArraySocket', "Array A")
        self.inputs.new('FlowScalarSocket', "Rows")
        self.inputs.new('FlowScalarSocket', "Items per Rows")        

        self.outputs.new('FlowArraySocket', "Reshaped")


    def draw_buttons(self, context, layout):
        l = layout.column()
        l.label(self.shape_str)

    def process(self):
        a = self.inputs[0].fget()
        outputs = self.outputs

        rows = outputs['Rows']
        cols = outputs['Columns']

        if a.any():
            shape = a.shape
            self.shape_str = str(shape)
            if len(shape) == 2:
                pass

            elif len(shape) == 1:
                pass
        else:
            self.shape_str = "(no shape)"


def register():
    bpy.utils.register_class(FlowArrayReShape)


def unregister():
    bpy.utils.unregister_class(FlowArrayReShape)
