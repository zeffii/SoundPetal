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

# this is not great :)


_phi = (1 + sqrt(5))/2
constants = lambda: None
constants.PI_TIMES = pi
constants.PHI_TIMES = _phi
constants.TAU_TIMES = 2 * pi
constants.E_TIMES = e
constants.DIV_PI = pi
constants.DIV_PHI = _phi
constants.DIV_TAU = 2 * pi
constants.DIV_E = e


class FlowConstantsUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowConstantsUgen
    ==================

    allow constants and multiples of them.

    '''
    bl_idname = 'FlowConstantsUgen'
    bl_label = 'Constants and multiples'
    bl_icon = 'OUTLINER_OB_EMPTY'

    PI_TIMES = FloatProperty(name='PI_TIMES', default=1.0, step=0.5, update=updateSD)
    TAU_TIMES = FloatProperty(name='TAU_TIMES', default=1.0, step=0.5, update=updateSD)
    PHI_TIMES = FloatProperty(name='PHI_TIMES', default=1.0, step=0.5, update=updateSD)
    E_TIMES = FloatProperty(name='E_TIMES', default=1.0, step=0.5, update=updateSD)
    DIV_E = FloatProperty(name='DIV_E', default=1.0, step=0.5, update=updateSD)
    DIV_PI = FloatProperty(name='DIV_PI', default=1.0, step=0.5, update=updateSD)
    DIV_TAU = FloatProperty(name='DIV_TAU', default=1.0, step=0.5, update=updateSD)
    DIV_PHI = FloatProperty(name='DIV_PHI', default=1.0, step=0.5, update=updateSD)

    type_options = [
        ("PI_TIMES",  "N X PI",  "", 0),
        ("TAU_TIMES", "N X TAU", "", 1),
        ("PHI_TIMES", "N X PHI", "", 2),
        ("E_TIMES",   "N X E",   "", 3),
        ("DIV_E",     "E / N",   "", 4),
        ("DIV_PI",    "PI / N",  "", 5),
        ("DIV_TAU",   "TAU / N", "", 6),
        ("DIV_PHI",   "PHI / N", "", 7),
    ]

    scalar_type = EnumProperty(
        items=type_options,
        name="Type of constant",
        description="constant and multiples of",
        default="TAU_TIMES",
        update=updateSD)

    def init(self, context):
        self.outputs.new('FlowScalarSocket', "val").prop_name = self.scalar_type

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'scalar_type', text="")

    def process(self):
        val = getattr(self, self.scalar_type)
        self.outputs[0].prop_name = self.scalar_type
        constant = getattr(constants, self.scalar_type)

        if self.scalar_type in {'PI_TIMES', 'TAU_TIMES', 'PHI_TIMES', 'E_TIMES'}:
            outputvalue = val * constant
        else:
            outputvalue = constant / val

        self.outputs[0].fset(outputvalue)


def register():
    bpy.utils.register_class(FlowConstantsUgen)


def unregister():
    bpy.utils.unregister_class(FlowConstantsUgen)
