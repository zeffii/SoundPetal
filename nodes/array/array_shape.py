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
from bpy.props import IntProperty, BoolProperty, EnumProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


class FlowArrayDimensions(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowArrayDimensions
    ==================

    Use to get information about dimensions
    - col / row, 
    - items

    '''
    bl_idname = 'FlowArrayDimensions'
    bl_label = 'Array Dimensions'

    def init(self, context):
        self.inputs.new('ArraySocket', "Array A")
        self.outputs.new('ScalarSocket', "Rows")
        self.outputs.new('ScalarSocket', "Columns")
        m = self.outputs.new('ScalarSocket', "items")
        m.enabled = False

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        a = self.inputs[0].fget()

        rows = outputs['Rows']
        cols = outputs['Columns']
        itms = outputs['items']

        if a.any():
            shape = a.shape
            outputs = self.outputs
            if len(shape) == 2:
                r, c = shape
                rows.enabled = 1
                cols.enabled = 1
                itms.enabled = 0
                rows.fset(r)
                cols.fset(c)

            if len(shape) == 1:
                rows.enabled = 0
                cols.enabled = 0
                itms.enabled = 1
                itms.fset(shape[0])
            else:
                msg = 'arrays of dims {shape} not handled yet'
                print(msg.format(str(shape)))


def register():
    bpy.utils.register_class(FlowArrayDimensions)


def unregister():
    bpy.utils.unregister_class(FlowArrayDimensions)
