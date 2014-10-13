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
    "name": "Flow",
    "author": "Dealga McArdle (Based in part on Sverchok) ",
    "version": (0, 1),
    "blender": (2, 7, 2),
    "location": "Nodes > CustomNodesTree > Add user nodes",
    "description": "Generic Flow based interface for Blender",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"}

import os
import sys
import importlib
# import numpy
from collections import OrderedDict

FLOW = 'FLOW'

current_path = os.path.dirname(__file__)
if not current_path in sys.path:
    sys.path.append(current_path)
    print("\n> Loading Flow.")

# storage
imported_modules = []
node_list = []
core_modules = ["flow_cache", "mechanisms"]
root_modules = ["node_tree", "flow_nodes_enum"]
#utils_modules = []
ui_modules = []

# alias alias alias alias
take = importlib.import_module
store = imported_modules.append


def make_node_list(nodes):
    node_list = []
    for category, names in nodes.nodes_dict.items():
        node_cats = take('.{}'.format(category), 'nodes')
        for name in names:
            node = take('.{}'.format(name), 'nodes.{}'.format(category))
            node_list.append(node)
    print('> node categories: {}'.format(len(nodes.nodes_dict)))
    print('> node count     : {}'.format(len(node_list)))
    return node_list


# get root
for m in root_modules:
    im = take(m, __name__)
    store(im)

# get settings
#settings = take('.settings', __name__)
#store(settings)

# get (core, utils, ui)
flow_modules = OrderedDict()
flow_modules['core'] = core_modules
#flow_modules['utils'] = utils_modules
flow_modules['ui'] = ui_modules

for module_name, module_content in flow_modules.items():
    x = take(module_name)
    store(x)
    for m in module_content:
        im = take('.' + m, module_name)
        store(im)

# get nodes!
nodes = take('nodes')
store(nodes)

node_list = make_node_list(nodes)


def all_registerables():
    return imported_modules + node_list


def FLOW_nodecats(perform):
    import nodeitems_utils

    if perform == 'unregister':
        if FLOW in nodeitems_utils._node_categories:
            nodeitems_utils.unregister_node_categories(FLOW)

    elif perform == 'register':
        from flow_nodes_enum import make_categories
        if not (FLOW in nodeitems_utils._node_categories):
            nodeitems_utils.register_node_categories(FLOW, make_categories())


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
    # this handles only existing nodes,
    # new nodes are not yet detected

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
