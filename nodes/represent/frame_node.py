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
from bpy.app.handlers import frame_change_pre, persistent

from bpy.props import IntProperty, StringProperty
from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode

node_ref = {}


@persistent
def flow_pre_frame_handler(scene):
    n = node_ref.get('starter')
    if n:
        # print('should be doing something')
        n.frame_start = scene.frame_start
        n.frame_end = scene.frame_end
        n.frame_current = scene.frame_current
        # n.process()


class FlowFrameOperator(bpy.types.Operator):
    bl_idname = 'node.flow_frame_ops'
    bl_label = 'start and stop frame change handler'

    fn = StringProperty()

    def execute(self, context):
        screen = context.screen
        node_ref['starter'] = context.node

        if 'Play' in self.fn:
            frame_change_pre.append(flow_pre_frame_handler)
            print('added frame handler')
            if 'Forward' in self.fn:
                bpy.ops.screen.animation_play()
            else:
                bpy.ops.screen.animation_play(reverse=True)
        else:
            # this toggles to off.
            bpy.ops.screen.animation_play()
            frame_change_pre.remove(flow_pre_frame_handler)
            print('removed frame handler')

        return {'FINISHED'}


class FlowFrameInfoNode(bpy.types.Node, FlowCustomTreeNode):
    ''' Flow Frame Info Node '''

    bl_idname = 'FlowFrameInfoNode'
    bl_label = 'Scene Frame Info'

    frame_start = IntProperty(default=1, name='frame_start')  # , update=updateSD)
    frame_end = IntProperty(default=40, name='frame_end')  # , update=updateSD)
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

        row = layout.row(align=True)
        row.operator("screen.frame_jump", text="", icon='REW').end = False
        row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False

        # @override
        flow = 'node.flow_frame_ops'
        if not screen.is_animation_playing:
            dir1 = row.operator(flow, text="", icon='PLAY_REVERSE')
            dir1.fn = 'Play Reverse'

            dir2 = row.operator(flow, text="", icon='PLAY')
            dir2.fn = 'Play Forward'
        else:
            sub = row.row(align=True)
            sub.scale_x = 2.0
            dir3 = sub.operator(flow, text="", icon='PAUSE')
            dir3.fn = 'Pause'

        row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
        row.operator("screen.frame_jump", text="", icon='FF').end = True

    def process(self):
        scene = bpy.context.scene
        self.outputs[0].fset(scene.frame_start)
        self.outputs[1].fset(scene.frame_end)
        self.outputs[2].fset(scene.frame_current)


def register():
    bpy.utils.register_class(FlowFrameInfoNode)
    bpy.utils.register_class(FlowFrameOperator)


def unregister():
    bpy.utils.unregister_class(FlowFrameOperator)
    bpy.utils.unregister_class(FlowFrameInfoNode)
