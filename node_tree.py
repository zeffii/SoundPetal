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

import bpy

from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatVectorProperty,
    IntProperty
)

from bpy.types import (
    NodeTree,
    NodeSocket,
    NodeSocketStandard
)

from core.flow_cache import cache_set, cache_get
from nodeitems_utils import NodeCategory, NodeItem

fl_matrix_col = (.2, .8, .8, 1.0)
fl_arrays_col = (.2, .3, .3, 1.0)
fl_vector_col = (.9, .6, .2, 1.0)
fl_text_col = (.2, .6, .5, 1.0)
fl_sink_col = (.0, .0, .0, 1.0)


class MatrixSocket(NodeSocket):
    '''n x n matrix Socket_type'''
    bl_idname = "MatrixSocket"
    bl_label = "Matrix Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4, default=fl_matrix_col)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info())
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""

    def fget(self):
        return cache_get(self)

    def fset(self, data):
        cache_set(self, data)


class ArraySocket(NodeSocketStandard):
    '''n x n array Socket_type'''
    bl_idname = "ArraySocket"
    bl_label = "Array Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4, default=fl_arrays_col)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info())
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""

    def fget(self):
        return cache_get(self)

    def fset(self, data):
        cache_set(self, data)


class VectorSocket(NodeSocket):
    '''Vector Socket Type'''
    bl_idname = "VectorSocket"
    bl_label = "Vector Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4, default=fl_vector_col)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info())
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""

    def fget(self):
        return cache_get(self)

    def fset(self, data):
        cache_set(self, data)


class TextSocket(NodeSocketStandard):
    '''Text, human readable characters'''
    bl_idname = "TextSocket"
    bl_label = "Text Socket"

    prop_name = StringProperty(default='')
    prop_type = StringProperty(default='')
    prop_index = IntProperty()
    socket_col = FloatVectorProperty(size=4, default=fl_text_col)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info())
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""

    def fget(self):
        return cache_get(self)

    def fset(self, data):
        cache_set(self, data)


class SinkHoleSocket(NodeSocket):
    '''Sink Hole Socket Type'''
    bl_idname = "SinkHoleSocket"
    bl_label = "SinkHole Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4, default=fl_sink_col)
    # this socket can take anything.

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info())
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""

    def fget(self):
        return cache_get(self)

    def fset(self, data):
        cache_set(self, data)


class FlowCustomTree(NodeTree):
    ''' FLow nodes, pragma '''
    bl_idname = 'FlowCustomTreeType'
    bl_label = 'Flow Custom Tree'
    bl_icon = 'SEQ_CHROMA_SCOPE'

    def update(self):
        try:
            is_ready = bpy.data.node_groups[self.id_data.name]
        except:
            return


class FlowCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'FlowCustomTreeType'


class FlowNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'FlowCustomTreeType'


tree_classes = [
    FlowCustomTree,
    MatrixSocket,
    ArraySocket,
    VectorSocket,
    TextSocket,
    SinkHoleSocket
]


def register():
    for c in tree_classes:
        bpy.utils.register_class(c)


def unregister():
    for c in tree_classes:
        bpy.utils.unregister_class(c)
