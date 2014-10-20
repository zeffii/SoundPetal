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
from math import pi, sin, cos

import bpy
from bpy.props import EnumProperty, IntProperty, FloatProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


TWO_PI = 2*pi


def make_geometry(node, n, r):

    m = np.arange(0, TWO_PI, TWO_PI/n)
    if node.axis == 'X':
        g = np.array([[0, sin(x)*r, cos(x)*r, 0] for x in m])
    elif node.axis == 'Y':
        g = np.array([[sin(x)*r, 0, cos(x)*r, 0] for x in m])
    elif node.axis == 'Z':
        g = np.array([[sin(x)*r, cos(x)*r, 0, 0] for x in m])

    return g


class TrigUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' TrigUgen '''
    bl_idname = 'TrigUgen'
    bl_label = 'Trig Ugen'
    bl_icon = 'OUTLINER_OB_EMPTY'

    num_verts = IntProperty(
        name='num_verts',
        min=2, step=1, default=2,
        update=updateSD)

    radius = FloatProperty(
        name="distance",
        step=0.2, default=0.4,
        update=updateSD)

    axis_options = [
        ("X", "X", "", 0),
        ("Y", "Y", "", 1),
        ("Z", "Z", "", 2)
    ]

    axis = EnumProperty(
        items=axis_options,
        name="Type of axis",
        description="offers plane to base trig on X|Y|Z",
        default="Z",
        update=updateSD)

    def init(self, context):
        self.inputs.new("FlowScalarSocket", "num_verts").prop_name = "num_verts"
        self.inputs.new("FlowScalarSocket", "radius").prop_name = "radius"
        self.outputs.new('FlowArraySocket', "send")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'axis', expand=True)

    def process(self):
        n = self.inputs['num_verts'].fget(fallback=self.num_verts, direct=True)
        r = self.inputs['radius'].fget(fallback=self.radius, direct=True)
        gref = make_geometry(self, n, r)
        self.outputs[0].fset(gref)


def register():
    bpy.utils.register_class(TrigUgen)


def unregister():
    bpy.utils.unregister_class(TrigUgen)
