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
from bpy.props import IntProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowFrameInfoNode(bpy.types.Node, FlowCustomTreeNode):
    ''' Flow Frame Info Node '''

    bl_idname = 'FlowFrameInfoNode'
    bl_label = 'Scene Frame Info'

    frame_start = IntProperty(default=1, name='frame_start', update=updateSD)
    frame_end = IntProperty(default=40, name='frame_end', update=updateSD)
    frame_current = IntProperty(default=1, name='frame_current', update=updateSD)

    def init(self, context):
        self.outputs.new('FlowScalarSocket', 'frame_start').prop_name = 'frame_start'
        self.outputs.new('FlowScalarSocket', 'frame_end').prop_name = 'frame_end'
        self.outputs.new('FlowScalarSocket', 'frame_current').prop_name = 'frame_current'
        pass

    def draw_buttons(self, context, layout):
        context = bpy.context
        scene = context.scene
        screen = context.screen
        # scene.frame_subframe

        col = layout.column()
        #col.prop(scene, "frame_start", text="Start")
        #col.prop(scene, "frame_end", text="End")
        #col.prop(scene, "frame_current", text="current")

        #col.separator()

        row = layout.row(align=True)
        row.operator("screen.frame_jump", text="", icon='REW').end = False
        row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
        if not screen.is_animation_playing:
            row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
            row.operator("screen.animation_play", text="", icon='PLAY')
        else:
            sub = row.row(align=True)
            sub.scale_x = 2.0
            sub.operator("screen.animation_play", text="", icon='PAUSE')
        row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
        row.operator("screen.frame_jump", text="", icon='FF').end = True

    def process(Self):
        scene = boy.context.scene
        self.outputs[0].fset(scene.frane_start)
        self.outputs[1].fset(scene.frane_end)
        self.outputs[2].fset(scene.frane_current)


def register():
    bpy.utils.register_class(FlowFrameInfoNode)


def unregister():
    bpy.utils.unregister_class(FlowFrameInfoNode)
