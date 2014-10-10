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

FLOW = 'FLOW'

current_path = os.path.dirname(__file__)
if not current_path in sys.path:
    sys.path.append(current_path)
    print("\n> Loading Flow.")

imported_modules = []
core_modules = []
root_modules = []
ui_modules = []
utils_modules = []
node_list = []


def all_registerables():
    return []


def FLOW_nodecats(perform):
    import nodeitems_utils

    if perform == 'unregister':
        if FLOW in nodeitems_utils._node_categories:
            nodeitems_utils.unregister_node_categories(FLOW)

    if perform == 'register':
        from flow_nodes_menu import make_categories
        nodeitems_utils.register_node_categories(FLOW, make_categories())


if "bpy" in locals():
    importlib.reload(nodes)

    for im in all_registerables():
        importlib.reload(im)

    FLOW_nodecats('unregister')
    FLOW_nodecats('register')


import bpy


def register():
    import nodeitems_utils._node_categories as current_categories

    categories = make_categories()
    for m in all_registerables():
        if hasattr(m, "register"):
            m.register()

    if not (FLOW in current_categories):
        FLOW_nodecats('register')


def unregister():
    import nodeitems_utils
    for m in reversed(all_registerables()):
        if hasattr(m, "unregister"):
            m.unregister()

    FLOW_nodecats('unregister')
