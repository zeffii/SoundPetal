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
from bpy.props import FloatProperty, IntProperty, EnumProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode

_phi = (1 + sqrt(5))/2
constants = lambda: None
constants.PI_TIMES = pi
constants.PHI_TIMES = _phi
constants.E_TIMES = e


class FlowScalarMakeUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowScalarMakeUgen
    ==================

    allow to switch between outputting Integers or Floats.

    '''
    bl_idname = 'FlowScalarMakeUgen'
    bl_label = 'Scalar int float'
    bl_icon = 'OUTLINER_OB_EMPTY'

    INT = IntProperty(name='INT', default=0, step=1, update=updateSD)
    FLOAT = FloatProperty(name='FLOAT', default=0.0, step=0.1, update=updateSD)
    PI_TIMES = FloatProperty(name='PI_TIMES', default=1.0, step=0.5, update=updateSD)
    E_TIMES = FloatProperty(name='E_TIMES', default=1.0, step=0.5, update=updateSD)
    PHI_TIMES = FloatProperty(name='PHI_TIMES', default=1.0, step=0.5, update=updateSD)

    type_options = [
        ("INT", "Integer", "", 0),
        ("FLOAT", "Float", "", 1),
        ("PI_TIMES", "n * Pi", "", 2),
        ("E_TIMES", "n * e", "", 3),
        ("PHI_TIMES", "n * Phi", "", 4),
    ]

    scalar_type = EnumProperty(
        items=type_options,
        name="Type of variable",
        description="Scalar can be integer or float",
        default="INT",
        update=updateSD)

    def init(self, context):
        self.outputs.new('FlowScalarSocket', "val").prop_name = self.scalar_type

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'scalar_type', text="")

    def process(self):
        val = getattr(self, self.scalar_type)

        # only set if it is different, perhaps it would be clearer
        # to just set anyway.
        if not (self.scalar_type == self.outputs[0].prop_name):
            self.outputs[0].prop_name = self.scalar_type

        if self.scalar_type in {'PI_TIMES', 'E_TIMES', 'PHI_TIMES'}:
            self.outputs[0].fset(val * getattr(constants, self.scalar_type))
            return

        self.outputs[0].fset(val)


def register():
    bpy.utils.register_class(FlowScalarMakeUgen)


def unregister():
    bpy.utils.unregister_class(FlowScalarMakeUgen)
