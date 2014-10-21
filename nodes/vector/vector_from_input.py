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

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowVecFromInput(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowVecFromInput '''
    bl_idname = 'FlowVecFromInput'
    bl_label = 'Vector From Input'

    x_comp = FloatProperty(default=1.0, step=0.1, name='x_comp', update=updateSD)
    y_comp = FloatProperty(default=1.0, step=0.1, name='y_comp', update=updateSD)
    z_comp = FloatProperty(default=1.0, step=0.1, name='z_comp', update=updateSD)

    def init(self, context):
        self.inputs.new('FlowScalarSocket', 'x').prop_name = 'x_comp'
        self.inputs.new('FlowScalarSocket', 'y').prop_name = 'y_comp'
        self.inputs.new('FlowScalarSocket', 'z').prop_name = 'z_comp'
        self.outputs.new('FlowVectorSocket', "v out")

    def process(self):
        inputs = self.inputs
        x = inputs[0].fget(fallback=self.x_comp, direct=True)
        y = inputs[1].fget(fallback=self.y_comp, direct=True)
        z = inputs[2].fget(fallback=self.z_comp, direct=True)
        ftvec = np.array([x, y, z, 0])
        print('ftvec', ftvec)
        self.outputs[0].fset(ftvec)

    def draw_buttons(self, context, layout):
        # without this line, we get artefacts
        pass


def register():
    bpy.utils.register_class(FlowVecFromInput)


def unregister():
    bpy.utils.unregister_class(FlowVecFromInput)
