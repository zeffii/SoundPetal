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
from bpy.props import FloatProperty, IntProperty, EnumProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


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

    type_options = [
        ("INT", "Integer", "", 0),
        ("FLOAT", "Float", "", 1),
    ]

    scalar_type = EnumProperty(
        items=type_options,
        name="Type of variable",
        description="Scalar can be integer or float",
        default="INT",
        update=updateSD)

    def init(self, context):
        self.outputs.new('ScalarSocket', "val").prop_name = self.scalar_type

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'scalar_type', text="")
        # col.prop(self, self.scalar_type, text='')

    def process(self):
        val = getattr(self, self.scalar_type)

        # only reset of it is different, perhaps it would be clearer
        # to just set anyway.
        if not (self.scalar_type == self.outputs[0].prop_name):
            self.outputs[0].prop_name = self.scalar_type

        self.outputs[0].fset(val)


def register():
    bpy.utils.register_class(FlowScalarMakeUgen)


def unregister():
    bpy.utils.unregister_class(FlowScalarMakeUgen)
