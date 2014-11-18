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


class UgenXLine(SoundPetalUgen):
    '''Exponential Line'''
    bl_idname = 'UgenXLine'
    bl_label = 'XLine'
    sp_args = "(start: 1, end: 2, dur: 1, mul: 1, add: 0, doneAction: 0)"
    sp_rate = SoundPetalUgen.sp_rate
    modifiers = SoundPetalUgen.modifiers
    modifier_type = SoundPetalUgen.modifier_type


class UgenLine(SoundPetalUgen):
    '''Linear Line'''
    bl_idname = 'UgenLine'
    bl_label = 'Line'
    sp_args = "(start: 0, end: 1, dur: 1, mul: 1, add: 0, doneAction: 0)"
    sp_rate = SoundPetalUgen.sp_rate
    modifiers = SoundPetalUgen.modifiers
    modifier_type = SoundPetalUgen.modifier_type


def register():
    bpy.utils.register_class(UgenXLine)
    bpy.utils.register_class(UgenLine)


def unregister():
    bpy.utils.unregister_class(UgenXLine)
    bpy.utils.unregister_class(UgenLine)
