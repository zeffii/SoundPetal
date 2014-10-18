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


def combine(xyzw, edges, faces):
    geom_dict = {0: dict(verts=xyzw, edges=edges, faces=faces)}
    return dict(objects=geom_dict)


class FlowPackMeshUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    Flow Pack Mesh: Packs np.arrays of (performs no sanity checks)
    - 4*n of xyzw.
    - 2*n of edges
    - n faces
    '''

    bl_idname = 'FlowPackMeshUgen'
    bl_label = 'Pack Mesh'

    def init(self, context):
        self.inputs.new('FlowArraySocket', "xyzw")
        self.inputs.new('FlowArraySocket', "edges")
        self.inputs.new('FlowArraySocket', "faces")
        self.outputs.new('FlowGeometrySocket', "mesh")

    def process(self):
        xyzw = self.inputs[0].fget()
        edges = self.inputs[1].fget()
        faces = self.inputs[2].fget()
        data = combine(xyzw, edges, faces)
        self.outputs[0].fset(data)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(FlowPackMeshUgen)


def unregister():
    bpy.utils.unregister_class(FlowPackMeshUgen)
