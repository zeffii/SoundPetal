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


class UgenSawOsc(SoundPetalUgen):
    ''' UgenSawOsc '''
    bl_idname = 'UgenSawOsc'
    bl_label = 'Saw'
    sp_args = "(freq: 440, mul: 1, add: 0)"
    sp_rate = SoundPetalUgen.sp_rate
    modifiers = SoundPetalUgen.modifiers
    modifier_type = SoundPetalUgen.modifier_type
    modifier_xf = SoundPetalUgen.modifier_xf
    modifier_yf = SoundPetalUgen.modifier_yf


def register():
    bpy.utils.register_class(UgenSawOsc)


def unregister():
    bpy.utils.unregister_class(UgenSawOsc)
