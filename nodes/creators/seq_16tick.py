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


class FlowSeq16Node(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowSeq16Node '''
    bl_idname = 'FlowSeq16Node'
    bl_label = 'Seq16'
    bl_icon = 'OUTLINER_OB_EMPTY'

    seq_row_1 = BoolVectorProperty(size=16, update=updateSD)

    def init(self, context):
        self.outputs.new('SinkHoleSocket', "send")

    def draw_buttons(self, context, layout):
        row = layout.row(align=True)
        row.prop(self, 'seq_row_1', toggle=True, text='')

    def process(self):
        self.outputs[0].fset(self.seq_row_1[:])
        print(self.name, 'did something')


def register():
    bpy.utils.register_class(FlowSeq16Node)


def unregister():
    bpy.utils.unregister_class(FlowSeq16Node)
