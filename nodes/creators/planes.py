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
import itertools

import bpy
from bpy.props import EnumProperty, FloatProperty, IntProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


def faces_iterator(num_sides):
    up_one = num_sides + 1
    for i in range(num_sides):
        for j in range(num_sides):
            a = i * up_one + j
            yield a
            b = a+1
            yield b
            c = b + up_one
            yield c
            yield c - 1


def make_geometry(self, s, ns):
    s = s / 2.0
    axis = self.axis

    # more code, but less execution overall.

    if ns <= 1:
        v = []
        if axis == 'X':
            v = [[0, -s, -s], [0, s, -s], [0, s, s], [0, -s, s]]
        elif axis == 'Y':
            v = [[-s, 0, -s], [s, 0, -s], [s, 0, s], [-s, 0, s]]
        else:
            v = [[-s, -s, 0], [s, -s, 0], [s, s, 0], [-s, s, 0]]
        verts = np.array(v)
        faces = np.array([np.arange(4, -1)])
    else:
        s = np.linspace(-s, s, ns+1)
        combos = itertools.product(s, s)
        if axis == 'X':
            verts = np.array([(0, y, z) for y, z in combos])
        elif axis == 'Y':
            verts = np.array([(x, 0, z) for x, z in combos])
        else:
            verts = np.array([(x, y, 0) for x, y in combos])

        fit = faces_iterator(ns)
        faces = np.fromiter(fit, int).reshape(ns*ns, 4)

    return verts, faces


class FlowPlanesNode(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowPlanesNode '''
    bl_idname = 'FlowPlanesNode'
    bl_label = 'Planes'

    side = FloatProperty(name='side', update=updateSD)

    num_sides = IntProperty(
        default=1, min=1, step=1, max=50,
        name='num_sides', update=updateSD
    )

    axis_options = [
        ("X", "X", "", 0),
        ("Y", "Y", "", 1),
        ("Z", "Z", "", 2)
    ]

    axis = EnumProperty(
        items=axis_options,
        name="Type of axis",
        description="offers plane X|Y|Z",
        default="Z",
        update=updateSD)

    def init(self, context):
        self.inputs.new("FlowScalarSocket", "side").prop_name = "side"
        self.inputs.new("FlowScalarSocket", "num_sides").prop_name = "num_sides"
        self.outputs.new("FlowArraySocket", "verts")
        self.outputs.new("FlowArraySocket", "faces")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'axis', expand=True)

    def process(self):
        s = self.inputs['side'].fget2()
        ns = self.inputs['num_sides'].fget2()
        verts, faces = make_geometry(self, s, ns)
        self.outputs[0].fset(verts)
        self.outputs[1].fset(faces)


def register():
    bpy.utils.register_class(FlowPlanesNode)


def unregister():
    bpy.utils.unregister_class(FlowPlanesNode)
