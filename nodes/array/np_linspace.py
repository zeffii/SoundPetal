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
from bpy.props import FloatProperty, StringProperty, IntProperty, BoolProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowLinspaceUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowLinspaceUgen

    use linspace are per
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html

    This is temporary, might implement other linspace features.

    '''
    bl_idname = 'FlowLinspaceUgen'
    bl_label = 'Float Range'

    start = FloatProperty(name='start', default=0.0, step=0.1, update=updateSD)
    end = FloatProperty(name='end', default=1.0, step=0.1, update=updateSD)
    num = IntProperty(name='num', default=20, step=1, update=updateSD)
    end_point = BoolProperty(name='end_point', default=1, update=updateSD)
    range_label = StringProperty()

    def init(self, context):
        self.inputs.new('FlowScalarSocket', 'start').prop_name = 'start'
        self.inputs.new('FlowScalarSocket', 'end').prop_name = 'end'
        self.inputs.new('FlowScalarSocket', 'step').prop_name = 'step'
        self.outputs.new('FlowArraySocket', 'range')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'end_point', text='incl endpoint', toggle=True)

    def process(self):
        a = self.inputs[0].fget2()
        b = self.inputs[1].fget2()
        c = self.inputs[2].fget2()
        try:
            self.outputs[0].fset(np.linspace(a, b, c, endpoint=self.end_point))
            msg = 'R: {a:.2f} | {b:.2f} | {c:.2f}'
            self.range_label = msg.format(a=a, b=b, c=c)
            self.width_hidden = 120
        except:
            self.range_label = ""
            msg = 'failed:\nnp.linspace({a}, {b}, {c})'
            print(msg.format(a=a, b=b, c=c))

    def draw_label(self):
        if self.hide and self.range_label:
            return self.range_label

        return self.bl_label


def register():
    bpy.utils.register_class(FlowLinspaceUgen)


def unregister():
    bpy.utils.unregister_class(FlowLinspaceUgen)
