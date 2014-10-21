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


def cascading_trigger(context, downstream_nodes):
    ng = context.space_data.node_tree

    touched_links = []
    touched = touched_links.append

    DEBUG_MODE = True  # from settings
    if DEBUG_MODE:
        print('-----------from:', downstream_nodes)

    # assume a-cyclic
    major_counter = 0
    # last_node = None
    while(True):
        if major_counter >= len(ng.links):
            break

        current_downstream = set(downstream_nodes)
        downstream_nodes = set()
        for trigger_node in current_downstream:
            for link in ng.links:
                if not link.is_valid:
                    break
                if link in touched_links:
                    continue

                if link.from_node == trigger_node:
                    if DEBUG_MODE:
                        msg = 'calling {name}\'s .process()'
                        print(msg.format(name=link.to_node.name))

                    link.to_node.process()
                    downstream_nodes.add(link.to_node)

                elif link.to_node == trigger_node:
                    pass
                else:
                    continue

                touched(link)

        major_counter += 1


def updateSD(self, context):
    '''
    Update Self and Downstream. Whenever a property has this function
    attached, it passes update requests to the node it came from and
    the nodes that are downstream from it.

    TLDR;
    This propagates changes into the dependency graph.
    '''
    self.process()
    trigger_node = self

    ng = context.space_data.node_tree

    # if trigger_node has no socket connecting from it, end early
    links_first_pass = [i.from_node for i in ng.links]
    if not trigger_node in links_first_pass:
        return

    downstream_nodes = set([trigger_node])
    cascading_trigger(context, downstream_nodes)
