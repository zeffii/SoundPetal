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


def do_vector_lengths(A):
    if not isinstance(A, np.ndarray):
        return

    if not A.any():
        return

    sh = A.shape
    # single Vector
    if (len(sh) == 1) and (len(A) == 4):
        return np.sqrt(np.sum(np.power(A, 2)))

    # multiple vectors in one array (n*4 vectors)
    if (len(sh) == 2) and (sh[1] == 4):
        return np.sqrt(np.sum(np.power(A, 2), axis=1))


class FlowVectorLengthUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    take an np.ndarray of verts (or one vector) spit out the scalar
    length of the vector(s).

    The fact that this accepts Vector or Array of Vector input is 
    pure user convenience. It's only weird because that's the 
    kneejerk reaction to it. Once you know this is a predictable 
    behaviour for that socket, then it's second nature.
    '''

    bl_idname = 'FlowVectorLengthUgen'
    bl_label = 'Vector Length'

    def init(self, context):
        self.width = 20
        self.inputs.new('FlowVectorSocket', "xyzw")
        self.outputs.new('FlowArraySocket', "length(s)")

    def process(self):
        A = self.inputs[0].fget()
        x = do_vector_lengths(A)
        if isinstance(x, np.ndarray):
            self.outputs[0].fset(x)


def register():
    bpy.utils.register_class(FlowVectorLengthUgen)


def unregister():
    bpy.utils.unregister_class(FlowVectorLengthUgen)
