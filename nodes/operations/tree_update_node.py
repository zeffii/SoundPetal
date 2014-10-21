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

import numpy as np

import bpy

from FLOW.core.mechanisms import updateSD, cascading_trigger
from FLOW.node_tree import FlowCustomTreeNode


def creative_matrix(ng):

    num_nodes = len(ng.nodes)
    num_links = len(ng.links)
    nodes = ng.nodes

    node_table = {node.name: idx for idx, node in enumerate(nodes)}

    M = np.zeros((num_nodes, num_nodes))
    I = np.zeros((num_nodes, num_links))
    for idx, link in enumerate(ng.links):
        name_x = link.from_node.name
        name_y = link.to_node.name
        x = node_table.get(name_x)
        y = node_table.get(name_y)
        M[x][y] += 1
        I[x][idx] += 1
        I[y][idx] += 1

    reverse_node_table = {idx: node.name for idx, node in enumerate(nodes)}
    k = np.sum(I, axis=1) == 0
    KK = M.dot(I)
    JK = (I - KK)
    F = np.sum(JK, axis=1)

    summer = []
    for idx, val in enumerate(F):
        summer.append([val, reverse_node_table.get(idx)])

    return [j[1] for j in sorted(summer) if j[0] < 0]


class FlowNodeUpdateOperator(bpy.types.Operator):
    bl_idname = "node.flow_nodeupdate_operator"
    bl_label = "triggers cascading update"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ng = context.space_data.edit_tree

        # to_nodes = {link.to_node for link in ng.links}
        # from_nodes = {link.from_node for link in ng.links}

        # trigger_set = set()
        # for link in ng.links:
        #     node = link.from_node
        #     if not (node in to_nodes):
        #         trigger_set.add(node)
        #         # updateSD(node, context)
        #         node.select = True

        # if trigger_set:
        #     cascading_trigger(context, trigger_set)
        #     return {'FINISHED'}
        # else:
        #     return {'CANCELLED'}

        nodename_list = creative_matrix(ng)
        for name in nodename_list:
            node = ng.nodes[name]
            updateSD(node, context)

        return {'CANCELLED'}


class FlowTreeUpdateUgen(bpy.types.Node, FlowCustomTreeNode):
    ''' FlowTreeUpdateUgen '''
    bl_idname = 'FlowTreeUpdateUgen'
    bl_label = 'Flow Tree Update'

    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.operator('node.flow_nodeupdate_operator', text='rarww')

    def process(self):
        pass


def register():
    bpy.utils.register_class(FlowTreeUpdateUgen)
    bpy.utils.register_class(FlowNodeUpdateOperator)


def unregister():
    bpy.utils.unregister_class(FlowNodeUpdateOperator)
    bpy.utils.unregister_class(FlowTreeUpdateUgen)
