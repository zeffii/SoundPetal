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
from bpy.props import BoolProperty, BoolVectorProperty, StringProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowUnpackVertsUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    UnPack Mesh

    unPacks np.arrays of n*4 to separate X, Y, Z and W.
    '''

    bl_idname = 'FlowUnpackVertsUgen'
    bl_label = 'UnPack Verts'

    def init(self, context):
        self.width = 20
        self.inputs.new('FlowArraySocket', "n*4")
        self.outputs.new('FlowArraySocket', "x")
        self.outputs.new('FlowArraySocket', "y")
        self.outputs.new('FlowArraySocket', "z")
        self.outputs.new('FlowArraySocket', "w")

    def process(self):
        self.width = 20
        A = self.inputs[0].fget()
        x, y, z, w = A.T
        self.outputs[0].fset(x)
        self.outputs[1].fset(y)
        self.outputs[2].fset(z)
        self.outputs[3].fset(w)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(FlowUnpackVertsUgen)


def unregister():
    bpy.utils.unregister_class(FlowUnpackVertsUgen)
