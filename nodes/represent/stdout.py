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

import bpy
from bpy.props import BoolProperty, BoolVectorProperty

from core.mechanisms import updateSD
from node_tree import FlowCustomTreeNode


class FlowStdOutNode(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowStdOutNode '''
    bl_idname = 'FlowStdOutNode'
    bl_label = 'StdOut'
    bl_icon = 'OUTLINER_OB_EMPTY'

    def init(self, context):
        self.inputs.new('SinkHoleSocket', "see me")

    def process(self):
        print('---input---', self.inputs[0].fget())


def register():
    bpy.utils.register_class(FlowStdOutNode)


def unregister():
    bpy.utils.unregister_class(FlowStdOutNode)
