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
from bpy.props import FloatProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


class FlowArangeUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowArangeUgen '''
    bl_idname = 'FlowArangeUgen'
    bl_label = 'A range'
    bl_icon = 'OUTLINER_OB_EMPTY'

    start = FloatProperty(name='start', default=0.0, step=0.01, update=updateSD)
    end = FloatProperty(name='end', default=0.0, step=0.01, update=updateSD)
    step = FloatProperty(name='step', default=0.0, step=0.01, update=updateSD)

    def init(self, context):
        self.inputs.new('ScalarSocket', 'start').prop_name = 'start'
        self.inputs.new('ScalarSocket', 'end').prop_name = 'end'
        self.inputs.new('ScalarSocket', 'step').prop_name = 'step'
        self.outputs.new('ArraySocket', 'range')

    def process(self):
        a = self.inputs[0].fget(fallback=self.start, direct=True)
        b = self.inputs[1].fget(fallback=self.end, direct=True)
        c = self.inputs[2].fget(fallback=self.step, direct=True)
        print('a b c :: ', a, b, c)
        self.outputs[0].fset(np.arange(a, b, c))


def register():
    bpy.utils.register_class(FlowArangeUgen)


def unregister():
    bpy.utils.unregister_class(FlowArangeUgen)
