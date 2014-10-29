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
from numpy import sin, cos

import bpy
from bpy.props import FloatProperty, EnumProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


def do_transform(A, b, node):
    ops = node.operation
    axis = node.axis

    if ops == "ROTATE":

        if axis == 'X':
            x = [
                [1,       0,      0, 0],
                [0,  cos(b), sin(b), 0],
                [0, -sin(b), cos(b), 0],
                [0,       0,      0, 1]]
            T = np.array(x)

        elif axis == 'Y':
            y = [
                [cos(b), 0, -sin(b), 0],
                [0,      1,       0, 0],
                [sin(b), 0,  cos(b), 0],
                [0,      0,       0, 1]]
            T = np.array(y)

        elif axis == 'Z':
            z = [
                [cos(b),  sin(b), 0, 0],
                [-sin(b), cos(b), 0, 0],
                [0,            0, 1, 0],
                [0,            0, 0, 1]]
            T = np.array(z)

        return A.dot(T)

    if ops == "TRANSLATE":
        return A + b

    elif ops == "SCALE":
        tmat = [[b[0], 0,    0,    0],
                [0,    b[1], 0,    0],
                [0,    0,    b[2], 0],
                [0,    0,    0,    1]]

    # elif ops == "REFLECT":
    #     T = np.ident.tolist()
    # elif ops == "SHEER":
    #     T = np.ident.tolist()

    T = np.array(tmat)
    return A.dot(T)


def make_multiple_transforms(A, r, self):

    def make_iterable(k):
        for row_geom in A:
            for co in row_geom:
                yield co

        for row in r:
            geom = do_transform(A, row, self)
            for row_geom in geom:
                for co in row_geom:
                    yield co

    num_verts = len(A)
    iterable = make_iterable(A)
    j = np.fromiter(iterable, float)
    total_flat = len(j)
    return j.reshape(total_flat // 4, 4)


def make_multiple_scales(A, r, self):

    # arguably, this should be joined with the above function..
    def make_iterable(k):

        for row in r:
            print('row; ', row)
            geom = do_transform(A, row, self)
            for row_geom in geom:
                for co in row_geom:
                    print(co)
                    yield co

    num_verts = len(A)
    iterable = make_iterable(A)
    j = np.fromiter(iterable, float)
    total_flat = len(j)
    return j.reshape(total_flat // 4, 4)


class FlowVertsTransformUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowVertsTransformUgen
    ======================

    The point of this Node is to make chaining transforms possible.
    This makes explicit the order in which transforms are processed.
    '''

    bl_idname = 'FlowVertsTransformUgen'
    bl_label = 'Verts Transform'

    operation_types = [
        # internal,     ui,             "", enumidx
        ("ROTATE",      "Rotate",       "", 0),
        ("TRANSLATE",   "Translate",    "", 1),
        ("SCALE",       "Scale",        "", 2),
        # ("REFLECT",     "Reflect",      "", 3),
        # ("SHEER",       "Sheer",        "", 4),
    ]

    operation = EnumProperty(
        items=operation_types,
        name="Type of Transform",
        description="math.transform",
        default="TRANSLATE",
        update=updateSD)

    axis_options = [
        ("X", "X", "", 0),
        ("Y", "Y", "", 1),
        ("Z", "Z", "", 2)
    ]

    axis = EnumProperty(
        items=axis_options,
        name="Type of axis",
        description="offers plane to base transform on X|Y|Z",
        default="Z",
        update=updateSD)

    def init(self, context):
        self.inputs.new('FlowArraySocket', '4*n verts')
        self.inputs.new('FlowVectorSocket', 'vector')
        s = self.inputs.new('FlowScalarSocket', 'scalar')
        s.enabled = False

        self.outputs.new('FlowArraySocket', 'result')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'operation', text='')
        if (self.operation == 'ROTATE'):
            row = col.row()
            row.prop(self, 'axis', expand=True)

    def process(self):
        A = self.inputs[0].fget()

        is_rotation = (self.operation == 'ROTATE')
        is_scale = (self.operation == 'SCALE')
        self.inputs['scalar'].enabled = is_rotation
        self.inputs['vector'].enabled = not is_rotation

        # maybe use isinstance(A, np.ndarray)..
        if hasattr(A, 'any') and A.any():

            # the function 'do_transform' looks at self.operation to
            # perform scale, rotate, or translate .

            if is_rotation:
                r = self.inputs['scalar'].fget()
                if isinstance(r, (float, int)):
                    self.outputs[0].fset(do_transform(A, r, self))
                    return

                if isinstance(r, np.ndarray):
                    shape = r.shape
                    items = len(shape)
                    if items == 1:
                        kt = make_multiple_transforms(A, r, self)
                        self.outputs[0].fset(kt)
                        return

            elif is_scale:
                b = self.inputs['vector'].fget()

                # could be this
                # -if flat array, uniformly scale by each value
                # -if 1*4, then single object
                # -if n*4, then repeat with individual vectors.

                if isinstance(b, np.ndarray) and b.any():
                    shape = b.shape
                    if ((len(shape) == 1) and (len(b) == 4)):
                        print('does single vector')
                        do_func = do_transform
                    elif ((len(shape) == 2) and (shape[1] == 4)):
                        print('# shape is 2, and n*4')
                        do_func = make_multiple_scales
                    else:
                        return
                    ck = do_func(A, b, self)
                    print(ck)
                    self.outputs[0].fset(ck)

            else:
                b = self.inputs['vector'].fget()
                if isinstance(b, np.ndarray) and b.any():
                    self.outputs[0].fset(do_transform(A, b, self))
                    return

        # undefined operation, output A
        self.outputs[0].fset(A)


def register():
    bpy.utils.register_class(FlowVertsTransformUgen)


def unregister():
    bpy.utils.unregister_class(FlowVertsTransformUgen)
