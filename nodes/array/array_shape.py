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
from math import pi, sqrt, e

import bpy
from bpy.props import (
    IntProperty, BoolProperty, EnumProperty, StringProperty)

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowArrayShape(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowArrayShape
    ==============

    Use to get information about dimensions
    - col / row,
    - items

    '''
    bl_idname = 'FlowArrayShape'
    bl_label = 'Array Shape'
    shape_str = StringProperty(description="repr of array.shape")

    def init(self, context):
        self.inputs.new('FlowArraySocket', "Array A")
        self.outputs.new('FlowScalarSocket', "Rows")
        self.outputs.new('FlowScalarSocket', "Columns")
        m = self.outputs.new('FlowScalarSocket', "items")
        m.enabled = False

    def draw_buttons(self, context, layout):
        l = layout.column()
        l.label(self.shape_str)

    def process(self):
        a = self.inputs[0].fget()
        outputs = self.outputs

        rows = outputs['Rows']
        cols = outputs['Columns']
        itms = outputs['items']

        if a.any():
            shape = a.shape
            # print("shape:{}".format(shape))
            self.shape_str = str(shape)
            if len(shape) == 2:
                r, c = shape
                rows.enabled = 1
                cols.enabled = 1
                itms.enabled = 0
                rows.fset(r)
                cols.fset(c)
            elif len(shape) == 1:
                rows.enabled = 0
                cols.enabled = 0
                itms.enabled = 1
                itms.fset(shape[0])
            else:
                msg = 'arrays of dims {shape} not handled yet'
                print(msg.format(shape=self.shape_str))
        else:
            self.shape_str = "(no shape)"


def register():
    bpy.utils.register_class(FlowArrayShape)


def unregister():
    bpy.utils.unregister_class(FlowArrayShape)
