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
from bpy.props import EnumProperty, FloatProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


def make_geometry(self, s):
    half = s / 2.0
    axis = self.axis

    v = []
    if axis == 'X':
        v = [[0, -s, -s], [0, s, -s], [0, s, s], [0, -s, s]]
    elif axis == 'Y':
        v = [[-s, 0, -s], [s, 0, -s], [s, 0, s], [-s, 0, s]]
    else:
        v = [[-s, -s, 0], [s, -s, 0], [s, s, 0], [-s, s, 0]]

    verts = np.array(v)
    faces = np.array([np.arange(4)])
    return verts, faces


class FlowPlanesNode(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowPlanesNode '''
    bl_idname = 'FlowPlanesNode'
    bl_label = 'Planes'

    Side = FloatProperty(name='Side', update=updateSD)

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
        self.inputs.new("FlowScalarSocket", "Side").prop_name = "Side"
        self.outputs.new("FlowArraySocket", "verts")
        self.outputs.new("FlowArraySocket", "faces")

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'axis', expand=True)

    def process(self):
        s = self.inputs['Side'].fget2()
        verts, faces = make_geometry(self, s)
        self.outputs[0].fset(verts)
        self.outputs[1].fset(faces)


def register():
    bpy.utils.register_class(FlowPlanesNode)


def unregister():
    bpy.utils.unregister_class(FlowPlanesNode)
