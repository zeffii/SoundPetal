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
from bpy.props import FloatProperty, EnumProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


math_functors = {
    'ADD': lambda a, b: a + b,
    'SUB': lambda a, b: a - b,
    'DIV': lambda a, b: a / b,
    'TIMES': lambda a, b: a * b,
    'INTDIV': lambda a, b: a // b,
    'SIN': lambda a, b: np.sin(a),
    'COS': lambda a, b: np.cos(a),
    'SINB': lambda a, b: np.sin(a)*b,
    'COSB': lambda a, b: np.cos(a)*b,
}


def do_math(a, b, op):
    functor = math_functors.get(op)

    print('a b --->', a, b)

    if a.any() and b.any():
        if len(a) == 1 and len(b) == 1:
            return functor(a[0], b[0])

        elif len(a) > 1 and len(b) == 1:
            return functor(a, b[0])

        elif (len(a) == len(b)) and (len(a) > 1):
            return functor(a, b)

        elif len(a) > 1 and len(b) > 1:
            if len(a) > len(b):
                diffsize = len(a) - len(b)
                b2 = np.array([b[-1]]).repeat(diffsize)
                b = np.concatenate((b, b2), 0)
            else:
                diffsize = len(b) - len(a)
                a2 = np.array([a[-1]]).repeat(diffsize)
                a = np.concatenate((a, a2), 0)

            return functor(a, b)
    elif a.any() and not b.any():
        return functor(a, None)

    return np.array([])


class FlowScalarMathUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowScalarMathUgen '''

    bl_idname = 'FlowScalarMathUgen'
    bl_label = 'Scalar Math'
    bl_icon = 'OUTLINER_OB_EMPTY'

    A = FloatProperty(name='A', default=0.0, step=0.01, update=updateSD)
    B = FloatProperty(name='B', default=0.0, step=0.01, update=updateSD)

    operation_types = [
        # internal, ui, "", enumidx
        ("ADD", "a+b", "", 0),
        ("SUB", "a-b", "", 1),
        ("DIV", "a/b", "", 2),
        ("TIMES", "a*b", "", 3),
        ("INTDIV", "a//b", "", 4),
        ("SIN", "sin(a)", "", 5),
        ("COS", "cos(a)", "", 6),
        ("SINB", "sin(a)*b", "", 7),
        ("COSB", "cos(a)*b", "", 8),
    ]

    operation = EnumProperty(
        items=operation_types,
        name="Type of math op",
        description="math.fast.",
        default="ADD",
        update=updateSD)

    def init(self, context):
        self.inputs.new('ArraySocket', 'A').prop_name = 'A'
        self.inputs.new('ArraySocket', 'B').prop_name = 'B'
        self.outputs.new('ArraySocket', 'result')

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'operation', text='', icon='DRIVER')

    def process(self):
        a = self.inputs[0].fget()
        b = self.inputs[1].fget()
        self.outputs[0].fset(do_math(a, b, self.operation))


def register():
    bpy.utils.register_class(FlowScalarMathUgen)


def unregister():
    bpy.utils.unregister_class(FlowScalarMathUgen)
