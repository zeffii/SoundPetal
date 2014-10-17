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


class FlowArrayConcatenate(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowArrayConcatenate
    ==================

    Allows combination of 2 arrays into one. 
    uses np.concatenate((a,b), 0)

    '''
    bl_idname = 'FlowArrayConcatenate'
    bl_label = 'Array Concatenate'
    bl_icon = 'OUTLINER_OB_EMPTY'

    def init(self, context):
        self.inputs.new('ArraySocket', "Array A")
        self.inputs.new('ArraySocket', "Array B")
        self.outputs.new('ArraySocket', "conc(A, B)")

    def draw_buttons(self, context, layout):
        pass

    def process(self):
        inputs = self.inputs
        a = inputs[0].fget()
        b = inputs[1].fget()
        if a.any() and b.any():
            self.outputs[0].fset(np.concatenate((a, b), 0))


def register():
    bpy.utils.register_class(FlowArrayConcatenate)


def unregister():
    bpy.utils.unregister_class(FlowArrayConcatenate)
