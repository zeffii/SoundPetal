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

from collections import OrderedDict

from nodeitems_utils import NodeItem
from FLOW.node_tree import FlowNodeCategory


def make_node_cats():

    node_cats = OrderedDict()
    '''  bl_idname,             shortname,     <icon> (optional)

    |   |                       |                              |
    '''
    node_cats["oscillators"] = [
        ['UgenSinOsc',      'SinOsc'],
        ['UgenFSinOsc',     'FSinOsc'],
        ['UgenSinOscFB',    'SinOscFB'],
        ['UgenBlip',        'Blip'],
        ['UgenPulse',       'Pulse'],
        ['UgenSaw',         'Saw'],
    ]

    node_cats["filters"] = [
        ['UgenLPF',         'LPF'],
        ['UgenRLPF',        'RLPF'],
        ['UgenMoogFF',      'MoogFF'],
    ]

    node_cats["noise"] = [
        ['UgenLFNoise0',    'LFNoise0'],
        ['UgenLFNoise1',    'LFNoise1'],
        ['UgenLFNoise2',    'LFNoise2'],
    ]

    node_cats["envelope"] = [
        ['UgenXLine',       'XLine'],
        ['UgenLine',        'Line'],
    ]

    node_cats["transport"] = [
        ['UgenIn',          'In'],
        ['UgenOut',         'Out'],
        ['UgenSplay',       'Splay'],
        ['SoundPetalSynthDef', 'Make SynthDef'],
    ]

    return node_cats


def make_categories():
    node_cats = make_node_cats()
    node_categories = []
    for category, nodes in node_cats.items():
        name_big = "FLOW_" + category.replace(' ', '_')

        items = [NodeItem(props[0], props[1]) for props in nodes]
        node_items = FlowNodeCategory(name_big, category, items=items)
        node_categories.append(node_items)

    return node_categories
