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
from FLOW.core.node_factory import make_ugen_class


UgenSinOsc = make_ugen_class(
    'SinOsc',
    "(freq: 440, phase: 0, mul: 1, add: 0)")

UgenFSinOsc = make_ugen_class(
    'FSinOsc', "(freq: 440, iphase: 0, mul: 1, add: 0)")


UgenSinOscFB = make_ugen_class(
    'SinOscFB', "(freq: 440, feedback: 0, mul: 1, add: 0)")


def register():
    bpy.utils.register_class(UgenSinOsc)
    bpy.utils.register_class(UgenFSinOsc)
    bpy.utils.register_class(UgenSinOscFB)


def unregister():
    bpy.utils.unregister_class(UgenSinOsc)
    bpy.utils.unregister_class(UgenFSinOsc)
    bpy.utils.unregister_class(UgenSinOscFB)
