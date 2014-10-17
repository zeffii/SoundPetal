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

_phi = (1 + sqrt(5))/2
constants = lambda: None
constants.PI_TIMES = pi
constants.PHI_TIMES = _phi
constants.E_TIMES = e


class FlowUVEdgeSurf(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowUVEdgeSurf
    ==================

    UV EdgeSurf takes an argument for number of verts in U and V,
    combined with two booleans to elect to make the surfaces or edgenet
    cyclic in U and/or V.

    '''
    bl_idname = 'FlowUVEdgeSurf'
    bl_label = 'UV EdgeSurf'
    bl_icon = 'OUTLINER_OB_EMPTY'

    count_u = IntProperty(name='count_u', min=0, step=1, update=updateSD)
    count_v = IntProperty(name='count_v', min=0, step=1, update=updateSD)
    cycle_u = IntProperty(name='cycle_u', min=0, max=1, update=updateSD)
    cycle_v = IntProperty(name='cycle_v', min=0, max=1, update=updateSD)

    topo_options = [
        ("EDGES", "Edges", "", 0),
        ("FACES", "Faces", "", 1),
    ]

    edgesurf = EnumProperty(
        items=topo_options,
        name="Type of topology",
        description="offers choice to make edges or faces",
        default="EDGES",
        update=updateSD)

    def init(self, context):
        self.inputs.new('ScalarSocket', "count u").prop_name = 'count_u'
        self.inputs.new('ScalarSocket', "count v").prop_name = 'count_v'
        self.inputs.new('ScalarSocket', "cycle u").prop_name = 'cycle_u'
        self.inputs.new('ScalarSocket', "cycle v").prop_name = 'cycle_v'
        self.outputs.new('ArraySocket', 'topology')

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'edgesurf', expand=True)

    def process(self):
        skip = 0
        nv = self.count_u
        nr = self.count_v

        dv = 0 if self.cycle_u == 1 else 1
        dr = 0 if self.cycle_v == 1 else 1
        num_poly = (nv-dv) * (nr-dr)

        p = [(i, i+1, i+nv, i+nv-1) for i in range(num_poly) if (i-skip) % (skip+1)]
        p += [[(i*(nv-1)), ((i+1)*(nv-1)), ((i+2)*(nv-1)-1), ((i+1)*(nv-1))-1] for i in range(nr)]
        val = np.array(p)
        self.outputs[0].fset(val)


def register():
    bpy.utils.register_class(FlowUVEdgeSurf)


def unregister():
    bpy.utils.unregister_class(FlowUVEdgeSurf)
