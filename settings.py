import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, FloatVectorProperty, EnumProperty

import data_structure
from core import handlers
from utils import sv_tools
FLOW_NAME = __package__


class FlowPreferences(AddonPreferences):

    bl_idname = __package__

    show_icons = BoolProperty(
        name="show_icons",
        default=False,
        description="Use icons in menu")

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="General")
        col.prop(self, "show_icons")


def register():
    bpy.utils.register_class(FlowPreferences)


def unregister():
    bpy.utils.unregister_class(FlowPreferences)
