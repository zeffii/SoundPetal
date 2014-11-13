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
import itertools

import bpy
from bpy.props import EnumProperty, FloatProperty, IntProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import SoundPetalUgen


class UgenSinOsc(SoundPetalUgen):
    ''' UgenSinOsc '''
    bl_idname = 'UgenSinOsc'
    bl_label = 'SinOsc Ugen'
    sp_args = "(freq: 440, phase: 0, mul: 1, add: 0)"

    def draw_buttons(self, context, layout):
        # row = layout.row()
        # row.prop(self, 'axis', expand=True)
        pass

    def process(self):
        # s = self.inputs['side'].fget2()
        # ns = self.inputs['num_sides'].fget2()
        # verts, faces = make_geometry(self, s, ns)
        # self.outputs[0].fset(verts)
        for i in self.inputs:
            print(i.name)
        self.outputs[0].fset("SinOsc(300, 2, 3)")


def register():
    bpy.utils.register_class(UgenSinOsc)


def unregister():
    bpy.utils.unregister_class(UgenSinOsc)
