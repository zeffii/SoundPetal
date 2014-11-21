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


# import numpy as np

# import bpy
# from bpy.props import BoolProperty, BoolVectorProperty, StringProperty

# from FLOW.core.mechanisms import updateSD
# from FLOW.node_tree import FlowCustomTreeNode
# from FLOW.utils.fl_proto_util import sock



# def script_parser(script_name):
#     ''' 
#     script in data.texts must fullfil these criteria before it
#     can be loaded and used as a Node body.

#     '''
#     script_as_str = bpy.data.texts[script_name].as_string()
#     exec(script_as_str)
#     local = locals()
#     pclass = local.get('PrototypeScript')
#     if pclass:
#         return local


# class FlowPrototyperLoader(bpy.types.Operator):
#     '''
#     yeah stuff
#     '''
#     bl_idname = 'node.flow_protonode_loader'
#     bl_label = 'flow_protonode_loader'

#     def execute(self, context):
#         node = context.node
#         script_name = node.internal_script_name
#         local = script_parser(script_name)
#         pclass = local.get('PrototypeScript')

#         # # can happen between F8.
#         if not node.node_dict.get(hash(node)):
#             node.reset()

#         if not pclass:
#             booted = False
#             node.inputs.clear()
#             node.outputs.clear()
#             self.report({'INFO'}, 'failed')
#         else:
#             booted = True
#             node.node_dict[hash(node)]['pclass'] = pclass
#             globals().update(local)
#             node.prepare_from_script()

#         node.boot_strapped = booted
#         return {'FINISHED'}


# class FlowPrototyperUgen(bpy.types.Node, FlowCustomTreeNode):
#     '''
#     stuff
#     '''

#     bl_idname = 'FlowPrototyperUgen'
#     bl_label = 'Proto Script Node'

#     internal_script_name = StringProperty(
#         description='use this to point at a scripted node script')

#     boot_strapped = BoolProperty(
#         description='used to indicate the state of loading')

#     # internal storage
#     node_dict = {}

#     def init(self, context):
#         self.reset()

#     def reset(self):
#         self.node_dict[hash(self)] = {}

#     def draw_buttons(self, context, layout):
#         row = layout.row()
#         row.prop_search(self, 'internal_script_name', bpy.data, 'texts', text='')
#         row.operator('node.flow_protonode_loader', text='GO!')

#     def process(self):
#         if not self.boot_strapped:
#             print('not bootstrapped')
#             return 

#         this_dict = self.node_dict.get(hash(self))
#         pcl = this_dict.get('pclass')
#         if pcl:
#             inputs = [s.fget() for s in self.inputs]
#             pobject = pcl()
#             m = pobject.process(*inputs)
#             for key, val in m.items():
#                 self.outputs[key].fset(val)

#     def prepare_from_script(self):
#         this_dict = self.node_dict.get(hash(self))
#         if this_dict:
#             pcl = this_dict.get('pclass')
#             if pcl:
#                 pobject = pcl()
#                 self.inputs.clear()
#                 for sock in pobject.sockets_in:
#                     stype = sock.kind
#                     t = self.inputs.new(stype, sock.name)
#                     if isinstance(sock.default, (int, float)):
#                         if isinstance(sock.default, int):
#                             t.prop_type = 'int'
#                             t.prop_int = sock.default
#                         if isinstance(sock.default, float):
#                             t.prop_type = 'float'
#                             t.prop_float = sock.default

#                 self.outputs.clear()
#                 for sock in pobject.sockets_out:
#                     stype = sock.kind
#                     self.outputs.new(stype, sock.name)


# def register():
#     bpy.utils.register_class(FlowPrototyperLoader)
#     bpy.utils.register_class(FlowPrototyperUgen)


# def unregister():
#     bpy.utils.unregister_class(FlowPrototyperUgen)
#     bpy.utils.unregister_class(FlowPrototyperLoader)