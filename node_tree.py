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

import numpy as np

import bpy

from bpy.props import (
    StringProperty, BoolProperty, FloatVectorProperty,
    IntProperty, FloatProperty, EnumProperty
)

from bpy.types import (
    NodeTree, NodeSocket, NodeSocketStandard
)

from FLOW.core.flow_cache import cache_set, cache_get, flowcache
from FLOW.core.variables_cache import (
    store_variable, free_variables, get_variables,
    free_all_variables, global_name
)

from FLOW.core.mechanisms import updateFromUI
from FLOW.core.mechanisms import updateSD
from FLOW.core.mechanisms import serialize_inputs
from FLOW.core.mechanisms import args_to_sockets
from nodeitems_utils import NodeCategory, NodeItem

fl_matrix_col = (.2, .8, .8, 1.0)
fl_arrays_col = (.99, .99, .99, 1.0)
fl_vector_col = (.9, .6, .2, 1.0)
fl_scalar_col = (.69, .9, .69, 1.0)
fl_text_col = (.2, .6, .5, 1.0)
fl_sink_col = (.0, .0, .0, 1.0)
fl_geom_col = (.99, .3, .3, 1.0)
fl_transfer_col = (0.7, 0.9, 1.0, 1.0)


class FlowSocket(NodeSocket):
    """ Socket type to inherit several useful class functions """
    bl_idname = "FlowGenericFSocket"
    bl_label = "generic fsocket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4, default=(1, 1, 1, 1))

    prop_int = IntProperty()
    prop_float = FloatProperty()
    prop_type = StringProperty()

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info())
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""

    def fset(self, data):
        cache_set(self, data)


class FlowTransferSocket(FlowSocket):
    '''Transfer Any Type: Use primarily for everything SoundPetal'''
    bl_idname = "FlowTransferSocket"
    bl_label = "Transfer Socket"

    prop_int = IntProperty(update=updateFromUI)
    prop_float = FloatProperty(update=updateFromUI)
    prop_bool = BoolProperty(update=updateFromUI)
    prop_type = StringProperty()

    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4, default=fl_transfer_col)

    def draw(self, context, layout, node, text):
        if self.is_output and self.prop_name:
            row = layout.row()
            row.prop(node, self.prop_name)
        else:
            if self.is_linked:
                layout.label(text)
                return

            if self.prop_type:
                row = layout.row()
                if self.prop_type == 'int':
                    row.prop(self, 'prop_int', text=self.name)
                if self.prop_type == 'float':
                    row.prop(self, 'prop_float', text=self.name)
                if self.prop_type == 'bool':
                    row.prop(self, 'prop_bool', text=self.name)

                return

            if not self.prop_name:
                layout.label(text)
                return

            layout.prop(node, self.prop_name)

    def fgetx(self):
        '''
        if unconnected: should return the value
        if connected: should return the node_id as str
        '''
        if self.links and self.links[0]:
            return cache_get(self)
        else:
            if self.prop_type == 'int':
                return self.prop_int
            if self.prop_type == 'float':
                return self.prop_float
            if self.prop_type == 'bool':
                return self.prop_bool

            # print(self, self.node.name, 'failed to implement fgetx')


''' T r e e '''


class FlowCustomTree(NodeTree):
    ''' SoundPetal Nodes, (FLow) '''
    bl_idname = 'FlowCustomTreeType'
    bl_label = 'Flow Custom Tree'
    bl_icon = 'SEQ_CHROMA_SCOPE'

    def update(self):
        try:
            is_ready = bpy.data.node_groups[self.id_data.name]
        except:
            return


class FlowCustomTreeNode(object):
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'FlowCustomTreeType'

    def draw_buttons(self, context, layout):
        # this helps some nodes which don't have buttons but do have sliders
        # to not be visually weird. (else the effect is cropping in y direction)
        # this somehow adds a few pixels.
        pass

    def free(self):
        '''
        This function deals with removing a Node from flowcache. flowcache contains
        tuples as keys, and socket data as values. The first element of those keys is the
        hash of the node name, the second element being the hash of the socket.

        {(hash(node), hash(node.to_socket)) : values, ..}

        The following procedure will walk through all keys (as a list) and pop those keys
        where the first element is the same as the hash of the node.
        '''

        DEBUG = True
        if DEBUG:
            print('attempting removal:', self.name)
            print(flowcache)

        if not flowcache:
            return

        for k in list(flowcache.keys()):
            if not k[0] == hash(self.name):
                continue
            if DEBUG:
                print(k, '|', hash(self.name), self.name)
                print('removed', flowcache.pop(k))
            else:
                flowcache.pop(k)

modifier_rewrites = {
    "RoundN":       (0, ".round"),
    "RoundG":       (1, ".round({0}"),
    "Recip":        (0, ".reciprocal"),
    "RecipMult":    (1, ".reciprocal * {0}"),
    "Range":        (2, ".range({0},{1})"),
    "Exprange":     (2, ".exprange({0},{1})")
}


class SoundPetalUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
        SoundPetal nodes will behave differently and the interface
        should be defined some other way than hardcoding individual Ugens.

    '''
    bl_idname = ""

    # control rate or audio rate features on many Ugens
    rate_options = [
        ("AudioRate", ".ar", "", 0),
        ("KontrolRate", ".kr", "", 1),
        ("InitRate", ".ir", "", 2)
    ]

    rate_options2 = [
        ("AudioRate", ".ar", "", 0),
        ("KontrolRate", ".kr", "", 1),
    ]

    sp_rate = EnumProperty(
        items=rate_options,
        name="Type of rate",
        description='audiorate, controlrate and initrate',
        default="AudioRate",
        update=updateSD)

    sp_rate2 = EnumProperty(
        items=rate_options2,
        name="Type of rate",
        description='audiorate or controlrate',
        default="AudioRate",
        update=updateSD)

    # modifier -----------------------------
    modifiers = BoolProperty()

    modifier_options = [
        ("RoundN", ".round", "", 0),
        ("RoundG", ".round(x)", "", 1),
        ("Recip",  ".reciprocal", "", 2),
        ("RecipMult",  ".reciprocal * x", "", 3),
        ("Range",  ".range(x,y)", "", 4),
        ("Exprange",  ".exprange(x,y)", "", 5),
    ]

    modifier_type = EnumProperty(
        items=modifier_options,
        name="Type of modifier",
        description='append a modifier',
        default='Range',
        update=updateSD)

    modifier_xf = FloatProperty()
    modifier_yf = FloatProperty()
    # modifier_xi = IntProperty()
    # modifier_yi = IntProperty()
    # --------------------------------------

    sp_args = StringProperty()

    def init(self, context):
        self.outputs.new("FlowTransferSocket", 'Out')
        self.sp_init(context)

    def convert(self, in_str, to_type):
        m = -3000
        try:
            m = to_type(in_str)
        except ValueError:
            print("Not a", to_type)
        return m

    def sp_init(self, context):
        if not self.sp_args:
            error_str = '{}: error, sp_args not provided in node definition'
            msg = error_str.format(self.bl_idname)
            return

        # remove parents.
        args = self.sp_args
        if args[0] == '(' and args[-1] == ')':
            args = args[1:-1]
        else:
            print(self.bl_idname, ': error, args unparsable, wrap in parens')
            return

        args_to_sockets(self, args)

    def draw_buttons_ext(self, context, layout):
        # row = layout.row()
        # row.label('yoko!')
        pass

    # for most ugens this is enough drawing.. else override.
    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, 'sp_rate', expand=True)

        col = layout.column()

        if hasattr(self, 'modifiers'):
            col.prop(self, 'modifiers')
            if self.modifiers:
                col.prop(self, 'modifier_type', text='')

                # modifier_rewrites = {
                #     "RoundN":       (0, ".round"),
                #     "RoundG":       (1, ".round({0}"),
                #     "Recip":        (0, ".reciprocal"),
                #     "RecipMult":    (1, ".reciprocal * {0}"),
                #     "Range":        (2, ".range({0},{1})"),
                #     "Exprange":     (2, ".exprange({0},{1})")
                # }

                row = layout.row()
                ops = modifier_rewrites.get(self.modifier_type)

                if ops[0] == 1:
                    row.prop(self, 'modifier_xf', text='')
                elif ops[0] == 2:
                    row.prop(self, 'modifier_xf', text='')
                    row.prop(self, 'modifier_yf', text='')

    # a generic implementation suitable for most ugens, else override
    def process(self):

        if not self.sp_args:
            return

        # if inputs does not match number of args, return early.
        if not len(self.inputs) == (self.sp_args.count(',') + 1):
            return

        sanitized_name = global_name(self)
        self.outputs[0].fset(sanitized_name)

        for socket in self.inputs:
            variable_result = socket.fgetx()
            if isinstance(variable_result, str):
                if variable_result.endswith('__'):
                    continue
            if isinstance(variable_result, bool):
                variable_result = str(variable_result).lower()
            if isinstance(variable_result, float):
                variable_result = round(variable_result, 5)

            store_variable(self, socket.name, variable_result)
            # print('stored')

    def get_args(self):
        varname = self.get_varname()
        sanitized_name = global_name(self)

        args = serialize_inputs(self)
        part2 = ""
        if hasattr(self, 'modifiers') and self.modifiers:
            ops = modifier_rewrites.get(self.modifier_type)
            if ops[0] == 1:
                part2 = ops[1].format(
                    round(self.modifier_xf, 6))
            if ops[0] == 2:
                part2 = ops[1].format(
                    round(self.modifier_xf, 6),
                    round(self.modifier_yf, 6))

        part1 = 'var {0} = {1}'.format(sanitized_name, args)
        return part1 + part2 + ';'

    def get_varname(self):
        return self.name.replace('.', '_')


class FlowNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'FlowCustomTreeType'


tree_classes = [
    FlowSocket,
    FlowCustomTree,
    FlowTransferSocket,
]


def register():
    for c in tree_classes:
        bpy.utils.register_class(c)


def unregister():
    for c in tree_classes:
        bpy.utils.unregister_class(c)
