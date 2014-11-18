# -*- coding: utf-8 -*-
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


def get_DAG(ng):
    ''' from the synthdef'''
    # mark all non connected nodes- these can be ignored.

    # find SynthDef, (find immediate connections, recurse)
    # stop at first instance, should really disallow multiple
    # instances.. but for now it doesn't.
    count = 0
    for n in ng.nodes:
        if n.bl_idname == 'SoundPetalSynthDef':
            count += 1

    if count > 1:
        return 'too many synthdefs in layout'
    else:
        # this only gets triggered by a synthdef
        SDEF = 'SynthDef Maker'

    # if the direction is left to right, this will find the reverse
    # direction and branches.
    for p in ng.links:  # p = 'patch cable'
        print(p.from_node.name, '->', p.to_node.name)

    pass
