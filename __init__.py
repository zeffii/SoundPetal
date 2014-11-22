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

bl_info = {
    "name": "SoundPetal (Flow)",
    "author": "Dealga McArdle (Based in part on Sverchok) ",
    "version": (0, 1),
    "blender": (2, 7, 2),
    "location": "Nodes > CustomNodesTree > Add user nodes",
    "description": "Flow based SuperCollider interface for Blender",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"}

import os
import sys
import importlib
import numpy
from collections import OrderedDict

FLOW = 'FLOW'

if __name__ != FLOW:
    sys.modules[FLOW] = sys.modules[__name__]

if FLOW:
    print("\n> Loading", __name__)

    # storage
    imported_modules = []
    node_list = []

    core_modules = [
        "flow_cache",
        "mechanisms",
        "variables_cache",
        "reversed_DAG",
        "node_factory",
    ]

    root_modules = [
        "node_tree",
        "flow_nodes_index",
    ]

    util_modules = [
        'fl_bmesh_utils',
        'fl_proto_util',
        'osc_panel',
    ]

    ui_modules = []

    # alias alias alias alias
    take = importlib.import_module
    store = imported_modules.append


def make_node_list(nodes):
    node_list = []
    for category, names in nodes.nodes_dict.items():
        take('FLOW.nodes.{c}'.format(c=category))
        for name in names:
            node = take('FLOW.nodes.{c}.{n}'.format(n=name, c=category))
            node_list.append(node)
    print('> node categories: {}'.format(len(nodes.nodes_dict)))
    print('> node count     : {}'.format(len(node_list)))
    return node_list

if FLOW:

    for m in root_modules:
        im = take('FLOW.{root_module}'.format(root_module=m))
        store(im)

    #settings = take('.settings', __name__)
    #store(settings)

    # get (core, utils, ui)
    flow_modules = OrderedDict()
    flow_modules['core'] = core_modules
    flow_modules['utils'] = util_modules
    flow_modules['ui'] = ui_modules

    for module_name, module_content in flow_modules.items():
        x = take('FLOW.{}'.format(module_name))
        store(x)
        for m in module_content:
            im = take("FLOW.{mod}.{m}".format(mod=module_name, m=m))
            store(im)

    nodes = take('FLOW.nodes')
    store(nodes)


def all_registerables():
    return imported_modules + make_node_list(nodes)


def FLOW_nodecats(perform):
    import nodeitems_utils as nu
    node_categories = nu._node_categories

    if perform == 'unregister':
        if FLOW in node_categories:
            nu.unregister_node_categories(FLOW)

    elif perform == 'register':
        from FLOW.flow_nodes_index import make_categories
        if not (FLOW in node_categories):
            nu.register_node_categories(FLOW, make_categories())


def FLOW_modules(perform):
    if perform == "register":
        for m in all_registerables():
            if hasattr(m, "register"):
                m.register()

    elif perform == "unregister":
        for m in reversed(all_registerables()):
            if hasattr(m, "unregister"):
                m.unregister()


if "bpy" in locals():
    importlib.reload(nodes)

    for im in all_registerables():
        importlib.reload(im)

    FLOW_nodecats('unregister')
    FLOW_nodecats('register')


import bpy


def register():
    FLOW_modules("register")
    FLOW_nodecats('register')


def unregister():
    FLOW_nodecats('unregister')
    FLOW_modules("unregister")
