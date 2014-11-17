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


class UgenMoogFF(SoundPetalUgen):
    bl_idname = 'UgenMoogFF'
    bl_label = 'MoogFF'
    sp_args = "(in, freq: 100, gain: 2, reset: 0, mul: 1, add: 0)"
    sp_rate = SoundPetalUgen.sp_rate


class UgenLPF(SoundPetalUgen):
    bl_idname = 'UgenLPF'
    bl_label = 'LPF'
    sp_args = "(in: 0, freq: 440, mul: 1, add: 0)"
    sp_rate = SoundPetalUgen.sp_rate


class UgenRLPF(SoundPetalUgen):
    bl_idname = 'UgenRLPF'
    bl_label = 'RLPF'
    sp_args = "(in: 0, freq: 440, rq: 1, mul: 1, add: 0)"
    sp_rate = SoundPetalUgen.sp_rate


def register():
    bpy.utils.register_class(UgenMoogFF)
    bpy.utils.register_class(UgenLPF)
    bpy.utils.register_class(UgenRLPF)


def unregister():
    bpy.utils.unregister_class(UgenMoogFF)
    bpy.utils.unregister_class(UgenLPF)
    bpy.utils.unregister_class(UgenRLPF)
