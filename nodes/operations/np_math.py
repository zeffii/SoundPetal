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

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


math_functors = {
    'MOD': lambda a, b: a % b,
    'ADD': lambda a, b: a + b,
    'SUB': lambda a, b: a - b,
    'DIV': lambda a, b: a / b,
    'TIMES': lambda a, b: a * b,
    'INTDIV': lambda a, b: a // b,
    'SIN': lambda a, b: np.sin(a),
    'COS': lambda a, b: np.cos(a),
    'SINB': lambda a, b: np.sin(a)*b,
    'COSB': lambda a, b: np.cos(a)*b,
    'NEG': lambda a, b: -a,
}


def do_math(a, b, op):
    functor = math_functors.get(op)

    # print('a b --->', a, b)

    ''' only interested in one socket, a '''
    if op in {'SIN', 'COS'}:
        return functor(a, None)

    a_is_array = hasattr(a, 'any')
    b_is_array = hasattr(b, 'any')

    ''' in the case of scalar a and b '''
    if not a_is_array and not b_is_array:
        return functor(a, b)

    if a_is_array:
        if isinstance(b, np.float64):
            return functor(a, b)

        if not b_is_array:
            return functor(a, b)

    ''' both are arrays but do they sync? '''
    if a_is_array and b_is_array:
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

    return np.array([])


class FlowScalarMathUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowScalarMathUgen '''

    bl_idname = 'FlowScalarMathUgen'
    bl_label = 'Scalar Math'
    bl_icon = 'OUTLINER_OB_EMPTY'

    A = FloatProperty(name='A', default=0.0, step=0.01, update=updateSD)
    B = FloatProperty(name='B', default=0.0, step=0.01, update=updateSD)

    # if you change these, keep it compatible with def draw_labels()
    operation_types = [
        # internal, ui, "", enumidx
        ("ADD",    "a + b",      "", 0),
        ("SUB",    "a - b",      "", 1),
        ("DIV",    "a / b",      "", 2),
        ("TIMES",  "a * b",      "", 3),
        ("INTDIV", "a / / b",    "", 4),
        ("SIN",    "sin(a)",     "", 5),
        ("COS",    "cos(a)",     "", 6),
        ("SINB",   "sin(a) * b", "", 7),
        ("COSB",   "cos(a) * b", "", 8),
        ("MOD",    "a % b",      "", 9),
        ("NEG",    "-a ",        "", 10),
    ]

    operation = EnumProperty(
        items=operation_types,
        name="Type of math op",
        description="math.fast.",
        default="ADD",
        update=updateSD)

    def init(self, context):
        self.inputs.new('FlowArraySocket', 'A').prop_name = 'A'
        self.inputs.new('FlowArraySocket', 'B').prop_name = 'B'
        self.outputs.new('FlowArraySocket', 'result')

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'operation', text='', icon='DRIVER')

    def process(self):
        self.inputs['B'].enabled = not (self.operation in {'SIN', 'COS', 'NEG'})
        a = self.inputs[0].fget2()
        b = self.inputs[1].fget2()

        if isinstance(a, list) and len(a) == 0:
            return
        if isinstance(b, list) and len(b) == 0:
            return

        self.outputs[0].fset(do_math(a, b, self.operation))

    def draw_label(self):
        if self.hide:
            ops = self.operation
            items = [i for i in self.operation_types if i[0] == ops][0]
            label = items[1]

            if self.inputs[0].links:
                a = 'A'
            else:
                a = str(round(self.A, 3))

            if self.inputs[1].links:
                b = 'B'
            else:
                b = str(round(self.B, 3))

            label = label.replace('a ', a + ' ')
            label = label.replace(' b', ' ' + b)
            label = label.replace('(a)', '(' + a + ')')
            return label
        else:
            return self.bl_label


def register():
    bpy.utils.register_class(FlowScalarMathUgen)


def unregister():
    bpy.utils.unregister_class(FlowScalarMathUgen)
