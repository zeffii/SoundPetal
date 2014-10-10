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

from nodeitems_utils import NodeCategory, NodeItem


class GenericSocket(NodeSocket):
    '''Flow sockets inherit from this class'''
    bl_idname = ""
    bl_label = ""
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(size=4)

    def fget(self):
        pass

    def fset(self, data):
        pass

    def draw(self, context, layout, node, text):
        if self.is_linked:
            text += (self.get_info(self))
        layout.label(text)

    def draw_color(self, context, node):
        return self.socket_col

    def get_info(self):
        return ""


class MatrixSocket(GenericSocket):
    '''n x n matrix Socket_type'''
    bl_idname = "MatrixSocket"
    bl_label = "Matrix Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(
        size=4, value=(.2, .8, .8, 1.0))


class ArraySocket(NodeSocketStandard):
    '''n x n array Socket_type'''
    bl_idname = "ArraySocket"
    bl_label = "Array Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(
        size=4, value=(.2, .3, .3, 1.0))


class VectorSocket(GenericSocket):
    '''Vector Socket Type'''
    bl_idname = "VectorSocket"
    bl_label = "Vector Socket"
    prop_name = StringProperty(default='')
    socket_col = FloatVectorProperty(
        size=4, value=(0.9, 0.6, 0.2, 1.0))


class TextSocket(NodeSocketStandard):
    '''Text, human readable characters'''
    bl_idname = "StringsSocket"
    bl_label = "Strings Socket"

    prop_name = StringProperty(default='')
    prop_type = StringProperty(default='')
    prop_index = IntProperty()

    def fget(self):
        pass

    def fset(self, data):
        pass

    def draw(self, context, layout, node, text):
            if self.is_linked:
                text += (self.get_info(self))
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)


class FlowNodeTree(NodeTree):
    ''' FLow nodes, pragma '''
    bl_idname = 'FlowNodeTreeType'
    bl_label = 'Flow NodeTree'
    bl_icon = 'RNA'

    def update(self):
        try:
            is_ready = bpy.data.node_groups[self.id_data.name]
        except:
            return
        finally:
            self.process()

    def process(self):
        pass


class FlowCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'FlowNodeTreeType'


class FlowNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'FlowNodeTreeType'


tree_classes = [
    FlowNodeTree,
    MatrixSocket,
    ArraySocket,
    VectorSocket,
    TextSocket
]


def register():
    for c in tree_classes:
        bpy.utils.register_class(c)


def unregister():
    for c in tree_classes:
        bpy.utils.unregister_class(c)
