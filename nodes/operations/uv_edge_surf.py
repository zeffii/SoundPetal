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

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


def polygon_iterator(num_u, cyclic_u, num_v, cyclic_v):
    _Up = np.array([(i, i+1, i+num_u+2, i+num_u+1) for i in range(num_u)])
    for poly in _Up:
        for idx in poly:
            yield idx

    if cyclic_u:
        _UpClose = np.array([[num_u, 0, num_u+1, 2*(num_u+1)-1]])
        p = np.concatenate((_Up, _UpClose), 0)
        for poly in _UpClose:
            for idx in poly:
                yield idx
    else:
        p = _Up

    # perform V polygon make
    if True:
        for j in range(1, num_v):
            offset = j*(num_u+1)
            next_level = p+offset
            for poly in next_level:
                for idx in poly:
                    yield idx

        if cyclic_v:
            offset = num_u+1
            m = next_level+offset
            mod = m[0][0]
            # print(m.T)
            mT = m.T
            mT0 = mT[0]
            mT1 = np.roll(mT[1] % mod, 1)
            mT2 = mT[1] % mod
            mT3 = np.roll(mT[0], -1)
            d = np.array([mT0, mT3, mT2, mT1])
            dT = d.T
            for poly in dT:
                for idx in poly:
                    yield idx


def wrap_uv(num_u, num_v, cyclic_u, cyclic_v):
    # adjust_to_index
    num_u -= 1
    num_v -= 1
    num_u = max(2, num_u)
    num_v = max(2, num_v)

    iterable = polygon_iterator(num_u, cyclic_u, num_v, cyclic_v)
    j = np.fromiter(iterable, int)
    total_flat = len(j)
    p = j.reshape(total_flat // 4, 4)
    return p


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

    num_poly = IntProperty(default=6, min=1, update=updateSD)
    modulo_verts = IntProperty(name='modulo_verts', min=0, step=1, update=updateSD)
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
        self.inputs.new('FlowArraySocket', "verts")
        self.inputs.new('FlowScalarSocket', "modulo_verts").prop_name = 'modulo_verts'
        self.inputs.new('FlowScalarSocket', "cycle u").prop_name = 'cycle_u'
        self.inputs.new('FlowScalarSocket', "cycle v").prop_name = 'cycle_v'
        self.outputs.new('FlowArraySocket', 'topology')

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'edgesurf', expand=True)

    def process(self):
        inputs = self.inputs
        v = inputs['verts'].fget()
        modulo_verts = inputs['modulo_verts'].fget(fallback=self.modulo_verts, direct=True)

        ## fix this soon.
        if isinstance(modulo_verts, (list,)):
            if len(modulo_verts) == 1:
                modulo_verts = modulo_verts[0]

        # when using a//b produces 4.0 not 4
        try:
            modulo_verts = int(modulo_verts)
        except:
            self.outputs[0].fset([])
            return

        if not v.any():
            return

        if not (len(v.shape) == 2):
            return

        x = modulo_verts
        y = (len(v) // modulo_verts)
        val = wrap_uv(x, y, self.cycle_u, self.cycle_v)
        self.outputs[0].fset(val)
        # print('xy: {x},{y}:'.format(x=x, y=y))


def register():
    bpy.utils.register_class(FlowUVEdgeSurf)


def unregister():
    bpy.utils.unregister_class(FlowUVEdgeSurf)
