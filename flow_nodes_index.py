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

    node_cats["vector"] = [
        ["FlowVecMakeNode",     "Vector"],
        ["FlowVecFromInput",    "Vector from input"],
        ['FlowVectorLengthUgen', "Vector Length(s)"]
    ]

    node_cats["creators"] = [
        ["FlowLinesNode",       "Line",                  "GRIP"],
        ["FlowPlanesNode",      "Plane",           "MESH_PLANE"],
        ["FlowSeq16Node",       "16tick seq"],
        ["TrigUgen",            "basic trig"],
        ['FlowScalarMakeUgen',  'int or float'],
        ['FlowConstantsUgen',   'constants'],
        ['FlowOscServer',       'Osc Server'],
        ['FlowPrototyperUgen',  'sn prototyper'],
    ]

    node_cats["represent"] = [
        ["FlowStdOutNode",      "std out"],
        ["FlowMeshFilterUgen",  "filter mesh"],
        ["FlowBmeshUgen",       "bmesh"],
        ["Fl3DviewPropsNode",   "3dview props"],
        ['FlowFrameInfoNode',   "Frame Info"],
    ]

    node_cats['pack'] = [
        ["FlowPackVertsUgen",   "pack verts"],
        ["FlowPackMeshUgen",    "pack mesh"],
        ["FlowUnpackVertsUgen", "un-pack mesh"],
    ]

    node_cats['array'] = [
        ['FlowArangeUgen',      'Int Array (np.arange)'],
        ['FlowLinspaceUgen',    'Float Array (np.linspace)'],
        ['FlowArrayConcatenate', 'Concatenate'],
        ['FlowArrayShape',      'Get Shape'],
        ['FlowArrayRandomWSeed', 'Array of Random values'],
        ['FlowArrayReShape',     'Reshape'],
    ]

    node_cats["operations"] = [
        ["FlowScalarMathUgen",  "scalar math"],
        ["FlowVertsTransformUgen", "verts transform"],
        ['FlowDuplivertOne',    'Dupli Obj'],
        ['FlowTreeUpdateUgen',  'Update Trigger'],
    ]

    node_cats["uv"] = [
        ['FlowUVEdgeSurf',      'UV.EdgeSurf'],
        ['FlowUVPolygon',       'UV.Polygon'],
    ]

    node_cats["sv_ugen_osc"] = [
        ['UgenSinOsc',      'SinOsc'],
        ['UgenFSinOsc',     'FSinOsc'],
        ['UgenSinOscFB',    'SinOscFB'],
        ['UgenBlip',        'Blip'],
        ['UgenSawOsc',      'SawOsc'],
        ['UgenRLPF',        'RLPF'],
        ['UgenXLine',       'XLine'],
        ['UgenLine',        'Line'],
        ['UgenIn',          'In'],
        ['UgenOut',         'Out'],
        ['UgenSplay',       'Splay'],
        ['SoundPetalOscServer', 'SP OscServer'],
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
