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
from bpy.props import (
    IntProperty, BoolProperty, EnumProperty, StringProperty
)

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


fldescr_cols = "\
if 0: reshape=(len) else: \
if -1: then cols is inferred from what is possible given the value of rows."

fldescr_rows = "if 0: reshape=(len//cols, cols) else: reshape=(cols, rows)"


class FlowArrayReShape(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowArrayReShape
    ==============
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html
    flatten or unflatten array, (also called roll, unroll)

    '''
    bl_idname = 'FlowArrayReShape'
    bl_label = 'A.ReShape'

    Rows = IntProperty(
        default=0, step=1,
        name='Rows',
        description=fldescr_rows, update=updateSD)

    Cols = IntProperty(
        default=4, step=1,
        name='Cols',
        description=fldescr_cols, update=updateSD)

    shape_str = StringProperty(description="repr of array.shape")

    def init(self, context):
        self.inputs.new('FlowArraySocket', "Array")
        self.inputs.new('FlowScalarSocket', "Rows").prop_name = 'Rows'
        self.inputs.new('FlowScalarSocket', "Cols").prop_name = 'Cols'
        self.outputs.new('FlowArraySocket', "Reshaped")

    def draw_buttons(self, context, layout):
        l = layout.column()
        l.label(self.shape_str)

    def process(self):
        inputs = self.inputs
        outputs = self.outputs

        # convenience, fget2 is for scalar specifically with prop_name and no np.array wrapping
        a = inputs["Array"].fget()
        r = inputs['Rows'].fget2()
        c = inputs['Cols'].fget2()

        if hasattr(a, 'any') and a.any():
            shape = a.shape
            self.shape_str = str(shape)
            # if len(shape) == 2:
            #     # only meaningful operations are (for now)
            #     # - can be flattened
            #     # - reshaped
            #     pass

            # elif len(shape) == 1:
            #     # only meaningful operations are (for now)
            #     # - unflattened to (len//rows, rows)
            #     # - converting to 1-element rows
            #     pass
            # else:
            #     print('shape not handled yet..')
            reshaped_array = np.reshape(a, (r, c))
            outputs['Reshaped'].fset(reshaped_array)
        else:
            self.shape_str = "(no shape)"


def register():
    bpy.utils.register_class(FlowArrayReShape)


def unregister():
    bpy.utils.unregister_class(FlowArrayReShape)
