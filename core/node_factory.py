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


def make_ugen_class(ugenname, sp_args, basename='Ugen', rate_type=''):
    '''sp_rate can be: sp_rate or sp_rate2 '''

    name = basename + ugenname
    bl_idname = name
    bl_label = ugenname
    property_overwrites = {
        'bl_idname': name,
        'bl_label': ugenname,
        'sp_args': sp_args,
        'sp_rate': getattr(SoundPetalUgen, ('sp_rate' + str(rate_type))),
        'modifiers': SoundPetalUgen.modifiers,
        'modifier_type': SoundPetalUgen.modifier_type,
        'modifier_xf': SoundPetalUgen.modifier_xf,
        'modifier_yf': SoundPetalUgen.modifier_yf
    }

    return type(name, (SoundPetalUgen,), property_overwrites)
