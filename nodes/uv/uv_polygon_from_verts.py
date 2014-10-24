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
from bpy.props import IntProperty, BoolProperty, EnumProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowUVPolygon(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowUVPolygon
    ==================

    create an edge strip (looped or not) or polygon from a set of verts
    '''

    bl_idname = 'FlowUVPolygon'
    bl_label = 'Polygon from verts'

    topo_options = [
        ("EDGE", "Edge", "", 0),
        ("FACE", "Face", "", 1),
    ]

    edgesurf = EnumProperty(
        items=topo_options,
        name="Type of topology",
        description="offers choice to make edges or faces",
        default="EDGE",
        update=updateSD)

    loop = BoolProperty(update=updateSD)

    def init(self, context):
        self.inputs.new('FlowArraySocket', "verts")
        self.outputs.new('FlowArraySocket', 'topology')

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'edgesurf', expand=True)
        if self.edgesurf == 'EDGE':
            row = layout.row()
            row.prop(self, 'loop', toggle=True)

    def process(self):
        inputs = self.inputs
        v = inputs['verts'].fget()

        if hasattr(v, 'any') and not v.any():
            return
        if not (len(v.shape) == 2):
            return
        if not v.shape[1] == 4:
            return

        len_v = len(v)
        if self.edgesurf == 'FACE':
            val = np.array([np.arange(len_v)])
        else:
            pre_val = [[i, i+1] for i in range(len_v-1)]
            if self.loop:
                # hook up the tail to the head
                pre_val += [[len_v-1, 0]]
            val = np.array(pre_val)

        self.outputs[0].fset(val)

    def draw_label(self):
        if self.hide:
            return 'P.' + self.edgesurf
        else:
            return self.bl_label


def register():
    bpy.utils.register_class(FlowUVPolygon)


def unregister():
    bpy.utils.unregister_class(FlowUVPolygon)
