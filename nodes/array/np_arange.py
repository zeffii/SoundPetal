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
from bpy.props import FloatProperty, StringProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowArangeUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowArangeUgen '''
    bl_idname = 'FlowArangeUgen'
    bl_label = 'A range'
    bl_icon = 'OUTLINER_OB_EMPTY'

    start = FloatProperty(name='start', default=0.0, step=0.01, update=updateSD)
    end = FloatProperty(name='end', default=0.0, step=0.01, update=updateSD)
    step = FloatProperty(name='step', default=0.0, step=0.01, update=updateSD)
    range_label = StringProperty()

    def init(self, context):
        self.inputs.new('FlowScalarSocket', 'start').prop_name = 'start'
        self.inputs.new('FlowScalarSocket', 'end').prop_name = 'end'
        self.inputs.new('FlowScalarSocket', 'step').prop_name = 'step'
        self.outputs.new('FlowArraySocket', 'range')

    def process(self):
        a = self.inputs[0].fget(fallback=self.start, direct=True)
        b = self.inputs[1].fget(fallback=self.end, direct=True)
        c = self.inputs[2].fget(fallback=self.step, direct=True)
        try:
            self.outputs[0].fset(np.arange(a, b, c))
            msg = 'R: {a:.2f} | {b:.2f} | {c:.2f}'
            self.range_label = msg.format(a=a, b=b, c=c)
            self.width_hidden = 120
        except:
            self.range_label = ""
            msg = 'failed:\nnp.arange({a}, {b}, {c})'
            print(msg.format(a=a, b=b, c=c))

    def draw_label(self):
        if self.hide and self.range_label:
            return self.range_label

        return self.bl_label


def register():
    bpy.utils.register_class(FlowArangeUgen)


def unregister():
    bpy.utils.unregister_class(FlowArangeUgen)
