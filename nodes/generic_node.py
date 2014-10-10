import bpy

from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
    IntVectorProperty,
    IntProperty
)

from node_tree import FlowCustomTreeNode


class NodeTemplate(bpy.types.Node, FlowCustomTreeNode):
    bl_idname = ""
    bl_label = ""
    bl_icon = 'OUTLINER_OB_EMPTY'

    def init(self):
        pass

    def update(self):
        pass

    def process(self):
        pass

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        pass
