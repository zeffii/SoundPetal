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
from FLOW.node_tree import SoundPetalUgen
from FLOW.core.variables_cache import global_name
from FLOW.core.mechanisms import serialize_inputs


class UgenIn(SoundPetalUgen):
    bl_idname = 'UgenIn'
    bl_label = 'In'
    sp_args = "(bus, channelsArray)"
    sp_rate = SoundPetalUgen.sp_rate2

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'sp_rate', expand=True)


class UgenOut(SoundPetalUgen):
    bl_idname = 'UgenOut'
    bl_label = 'Out'
    sp_args = "(bus, channelsArray)"
    sp_rate = SoundPetalUgen.sp_rate2

    def get_args(self):
        varname = self.get_varname()
        sanitized_name = global_name(self)

        args = serialize_inputs(self)
        return '{0};'.format(args)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'sp_rate', expand=True)


class UgenSplay(SoundPetalUgen):
    bl_idname = 'UgenSplay'
    bl_label = 'Splay'
    sp_args = "(inArray, spread: 1, level: 1, center: 0, levelComp: true)"
    sp_rate = SoundPetalUgen.sp_rate2

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'sp_rate', expand=True)


def register():
    bpy.utils.register_class(UgenIn)
    bpy.utils.register_class(UgenOut)
    bpy.utils.register_class(UgenSplay)


def unregister():
    bpy.utils.unregister_class(UgenIn)
    bpy.utils.unregister_class(UgenOut)
    bpy.utils.unregister_class(UgenSplay)
