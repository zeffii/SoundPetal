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

from collections import OrderedDict, defaultdict


def get_apex(ng):
    to_nodes = {link.to_node for link in ng.links}
    from_nodes = {link.from_node for link in ng.links}

    trigger_set = set()
    for link in ng.links:
        node = link.from_node
        # find all nodes are are start points.
        # this automatically excludes disjoint nodes.
        if not (node in to_nodes):
            trigger_set.add(node)
    return trigger_set


def links_dict_from(links):
    ''' {from_node: [list_of_child_nodes]}'''
    ldict = defaultdict(list)
    for link in links:
        ldict[link.from_node].append(link.to_node)
    return ldict


def links_dict_to(links):
    ''' {to_node: [list_of_parent_nodes]}'''
    ldict = defaultdict(list)
    for link in links:
        ldict[link.to_node].append(link.from_node)
    return ldict


def prototype_cascade(ng, apex):
    # http://en.wikipedia.org/wiki/Topological_sorting

    L = []  # Empty list that will contain the sorted elements
    S = set(apex)  # Set of all nodes with no incoming edges
    add_to_L = L.append

    ldict_from = links_dict_from(ng.links)
    ldict_to = links_dict_to(ng.links)

    while S:  # is non-empty do
        n = S.pop()  # remove a node n from S
        add_to_L(n)  # add n to tail of L

        # for each node m with an edge e from n to m do
        #     remove edge e from the graph
        #     if m has no other incoming edges then
        #         insert m into S
        for m in ldict_from[n]:
            for idx, incoming in enumerate(ldict_to[m]):
                if incoming == n:
                    ldict_to[m][idx] = None
            if ldict_to[m].count(None) == len(ldict_to[m]):
                S.add(m)

        ldict_from[n] = []

    if any(ldict_from.values()):
        # print(ldict_from.values())
        print('error (graph has at least one cycle')
        return []
    else:
        # (in topologically sorted order)
        return L


# def cascading_trigger(context, downstream_nodes):
#     ng = context.space_data.node_tree

#     touched_links = []
#     touched = touched_links.append

#     DEBUG_MODE = True  # from settings
#     if DEBUG_MODE:
#         print('-----------from:', downstream_nodes)

#     # assume a-cyclic
#     major_counter = 0
#     # last_node = None
#     while(True):
#         if major_counter >= len(ng.links):
#             break

#         current_downstream = set(downstream_nodes)
#         downstream_nodes = set()
#         for trigger_node in current_downstream:
#             for link in ng.links:
#                 if not link.is_valid:
#                     break
#                 if link in touched_links:
#                     continue

#                 if link.from_node == trigger_node:
#                     if DEBUG_MODE:
#                         msg = 'calling {name}\'s .process()'
#                         print(msg.format(name=link.to_node.name))

#                     link.to_node.process()
#                     downstream_nodes.add(link.to_node)

#                 elif link.to_node == trigger_node:
#                     pass
#                 else:
#                     continue

#                 touched(link)

#         major_counter += 1


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

    # this works..triggers all upstream.
    # - assumes their cache is valid
    # - hence doesn't behave well on F8
    # downstream_nodes = set([trigger_node])
    # cascading_trigger(context, downstream_nodes)

    apex = get_apex(ng)
    L = prototype_cascade(ng, apex)

    # set the cache for the apex nodes
    # print('apex:', [n.name for n in apex])
    for node in apex:
        node.process()
        #node.select = True

    # do full retrig
    # print('L:', [n.name for n in L])
    for node in L:
        node.process()
        #node.select = True

    #cascading_trigger(context, L)


def updateFromUI(self, context):
    '''
    Update Self and Downstream. Whenever a property has this function
    attached, it passes update requests to the node it came from and
    the nodes that are downstream from it.

    TLDR;
    This propagates changes into the dependency graph.
    '''
    updateSD(self.node, context)
