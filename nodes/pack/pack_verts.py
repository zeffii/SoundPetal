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


def add_repeat_last(c, diffsize):
    if len(c) == 0:
        return np.zeros(diffsize)
    c2 = np.array([c[-1]]).repeat(diffsize)
    return np.concatenate((c, c2), 0)


def combine(x, y, z, w):
    is_nparray = lambda k: hasattr(w, 'any')
    len_or_zero = lambda c: len(c) if is_nparray(c) else 0

    if is_nparray(x) or is_nparray(y) or is_nparray(z) or is_nparray(w):
        m = [len_or_zero(c) for c in (x, y, z, w)]
        x_len, y_len, z_len, w_len = m
        longest = max(m)

        if not (x_len == longest):
            x = add_repeat_last(x, (longest - x_len))
        if not (y_len == longest):
            y = add_repeat_last(y, (longest - y_len))
        if not (z_len == longest):
            z = add_repeat_last(z, (longest - z_len))
        if not (w_len == longest):

            if w_len == 0:
                w = np.ones(longest)
            else:
                w = add_repeat_last(w, (longest - w_len))

        return np.vstack((x, y, z, w)).T
    else:
        return np.array([])


class FlowPackVertsUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    Flow Pack Mesh

    Packs np.arrays of X Y and Z values to a single verts object.
    Inserts repeat 0 arrays when socket is empty.
    '''

    bl_idname = 'FlowPackVertsUgen'
    bl_label = 'Pack Verts'

    def init(self, context):
        self.width = 20
        self.inputs.new('FlowArraySocket', "x")
        self.inputs.new('FlowArraySocket', "y")
        self.inputs.new('FlowArraySocket', "z")
        self.inputs.new('FlowArraySocket', "w")
        self.outputs.new('FlowArraySocket', "4*n")

    def process(self):
        self.width = 20
        x = self.inputs[0].fget()
        y = self.inputs[1].fget()
        z = self.inputs[2].fget()
        w = self.inputs[3].fget()
        data = combine(x, y, z, w)
        self.outputs[0].fset(data)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(FlowPackVertsUgen)


def unregister():
    bpy.utils.unregister_class(FlowPackVertsUgen)
