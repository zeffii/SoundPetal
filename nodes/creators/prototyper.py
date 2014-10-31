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
from bpy.props import BoolProperty, BoolVectorProperty, StringProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode
from FLOW.utils.fl_proto_util import sock


'''
class PrototypeScript(object):
    
    sockets_in = [
        sock(type='array', name='nx4', var='array_in'),
        sock(type='scalar', name='multiplier'), 
    ]
    
    sockets_out = [
        sock(type='array', name='generated', var='gen')
    ]

    @classmethod
    def process(self, *args):
        array_in = args[0]
        multiplier = args[1]
        
        gen = [0,2,3,4,5,6, multiplier]         
        
        return gen

'''


def script_parser(script_name):
    ''' 
    script in data.texts must fullfil these criteria before it
    can be loaded and used as a Node body.

    '''
    script_as_str = bpy.data.texts[script_name].as_string()
    exec(script_as_str)
    local = locals()
    pclass = local.get('PrototypeScript')
    if pclass:
        return pclass


class FlowPrototyperLoader(bpy.types.Operator):
    '''
    yeah stuff
    '''
    bl_idname = 'node.flow_protonode_loader'
    bl_label = 'flow_protonode_loader'

    def execute(self, context):
        node = context.node
        script_name = node.internal_script_name
        booted = node.boot_strapped
        pclass = script_parser(script_name)

        if not pclass:
            booted = False
            node.inputs.clear()
            node.outputs.clear()
            self.report({'INFO'}, 'failed')
        else:
            booted = True
            print(node.node_dict)
            node.node_dict[hash(node)]['pclass'] = pclass
            node.prepare_from_script()

        return {'FINISHED'}


class FlowPrototyperUgen(bpy.types.Node, FlowCustomTreeNode):
    '''
    stuff
    '''

    bl_idname = 'FlowPrototyperUgen'
    bl_label = 'Proto Script Node'

    internal_script_name = StringProperty(
        description='use this to point at a scripted node script')

    boot_strapped = BoolProperty(
        description='used to indicate the state of loading')

    # internal storage
    node_dict = {}

    def init(self, context):
        self.reset(context)

    def reset(self, context):
        self.node_dict[hash(self)] = {}

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop_search(self, 'internal_script_name', bpy.data, 'texts', text='')
        row.operator('node.flow_protonode_loader', text='GO!')

    def process(self):
        pass

    def prepare_from_script(self):
        this_dict = self.node_dict.get(hash(self))
        if this_dict:
            pcl = this_dict.get('pclass')
            if pcl:
                pobject = pcl()
                m = pobject.process('20', 30)
                print(m)


def register():
    bpy.utils.register_class(FlowPrototyperLoader)
    bpy.utils.register_class(FlowPrototyperUgen)


def unregister():
    bpy.utils.unregister_class(FlowPrototyperUgen)
    bpy.utils.unregister_class(FlowPrototyperLoader)
