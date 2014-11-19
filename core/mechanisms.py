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
from FLOW.core.variables_cache import global_name
from FLOW.utils.osc_panel import osc_statemachine

FOUND = 1
RUNNING = 3
DISABLED = 2
NOT_FOUND = 0

audiorate_dict = dict(AudioRate='ar', KontrolRate='kr', InitRate='ir')


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

        for m in ldict_from[n]:
            for idx, incoming in enumerate(ldict_to[m]):
                if incoming == n:
                    ldict_to[m][idx] = None
            if ldict_to[m].count(None) == len(ldict_to[m]):
                S.add(m)

        ldict_from[n] = []

    if any(ldict_from.values()):
        print('error (graph has at least one cycle')
        return []
    else:
        return L


def send_synthdef_osc_update(paramname, paramvalue):
    osc_msg = osc_statemachine.get('osc_msg')
    if osc_msg:

        msg = osc_msg(address='/flow/setSynthArg')
        msg.add_arg(paramname)
        msg.add_arg(paramvalue)
        msg = msg.build()

        client = osc_statemachine.get('client')
        print('sending synthdef set arg')
        client.send(msg)


def updateSD(self, context):
    '''
    Update Self and Downstream. Whenever a property has this function
    attached, it passes update requests to the node it came from and
    the nodes that are downstream from it.

    TLDR;
    This propagates changes into the dependency graph.

    '''
    if hasattr(context, 'socket'):
        short_paramname = context.socket.name
        paramname = global_name(self) + short_paramname
        paramvalue = self.inputs[short_paramname].fgetx()
        print(paramname, paramvalue)
        if osc_statemachine:
            if osc_statemachine['status'] == RUNNING:
                send_synthdef_osc_update(paramname, paramvalue)

    self.process()
    trigger_node = self

    ng = context.space_data.node_tree

    # if trigger_node has no socket connecting from it, end early
    links_first_pass = [i.from_node for i in ng.links]
    if not trigger_node in links_first_pass:
        return

    apex = get_apex(ng)
    L = prototype_cascade(ng, apex)

    # set the cache for the apex nodes
    for node in apex:
        node.process()
        #node.select = True

    # do full retrig
    for node in L:
        node.process()
        #node.select = True


def updateFromUI(self, context):
    '''
    Update Self and Downstream. Whenever a property has this function
    attached, it passes update requests to the node it came from and
    the nodes that are downstream from it.

    TLDR;
    This propagates changes into the dependency graph.
    '''
    updateSD(self.node, context)


def serialize_inputs(node):
    arglist = []
    for socket in node.inputs:
        variable_result = socket.fgetx()
        if isinstance(variable_result, str):
            if variable_result.endswith('__'):
                final_arg = variable_result
        else:
            final_arg = global_name(node) + socket.name
        arglist.append(final_arg)
    stringified_arglist = ', '.join(arglist)

    rate = audiorate_dict.get(node.sp_rate)
    return '{0}.{1}({2})'.format(node.bl_label, rate, stringified_arglist)


def args_to_sockets(node, chopped_args):
    ''' to be used by sp_init to create sockets from sp_args'''

    if chopped_args:
        if not ',' in chopped_args:
            return
        args = chopped_args.split(',')
        for _arg in args:
            arg = _arg.strip()

            is_boolean = False

            if ':' in arg:
                # this is  'somearg: somevariable'
                argname, argvalue = arg.split(':')
                argname = argname.strip()
                argvalue = argvalue.strip()

                if argvalue in {'true', 'false'}:
                    is_boolean = True
                    argvalue = {'true': True, 'false': False}.get(argvalue)

                # currently this is the most flexible.
                s = node.inputs.new("FlowTransferSocket", argname)

                if is_boolean:
                    s.prop_type = 'bool'
                    s.prop_int = argvalue

                elif argname in {'in', 'out', 'doneAction'}:
                    s.prop_type = 'int'
                    s.prop_int = node.convert(argvalue, int)
                else:
                    s.prop_type = 'float'
                    s.prop_float = node.convert(argvalue, float)

            else:
                # this is 'somearg'
                argname = arg.strip()
                s = node.inputs.new("FlowTransferSocket", argname)
