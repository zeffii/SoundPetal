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
from bpy.props import StringProperty
from FLOW.node_tree import FlowCustomTreeNode
from FLOW.utils.osc_panel import osc_statemachine
from FLOW.core.variables_cache import soundpetal_vars
from FLOW.core.reversed_DAG import get_DAG


class MakeSynthDefOps(bpy.types.Operator):
    bl_idname = "node.sp_serialize_synthdef"
    bl_label = 'Make SynthDef'

    def execute(self, context):

        print(osc_statemachine)
        ng = context.space_data.node_tree
        ng_id = ng.name

        # call process on all nodes once more
        for node in ng.nodes:
            if hasattr(node, 'process'):
                node.process()

        temp_list = []
        temp_list3 = []

        def list_print(in_str):
            temp_list.append(in_str)

        def var_list_print(in_str):
            temp_list2.append(in_str)

        list_print('(')
        list_print('SynthDef.new("{0}", {{'.format(context.node.synth_name))
        list_print('    arg')

        petalkeys = sorted(soundpetal_vars.keys())
        num_items = len(petalkeys)
        for idx, varname in enumerate(petalkeys):
            varval = soundpetal_vars[varname]
            if idx < num_items-1:
                terminator = ','
            else:
                terminator = ';'
            if varname.endswith('__bus'):
                varval = '[0,1]'
            if varname.endswith('__in'):
                varval = '[0]'
            list_print('    {0} = {1}{2}'.format(varname, varval, terminator))

        list_print('')

        # this needs to be sorted to avoid undeclared references.
        temp_list2 = get_DAG(ng)
        temp_list3.append('}).add;\n)')

        joined_lists = '\n'.join(temp_list + temp_list2 + temp_list3)
        context.node.generated_synthdef = joined_lists
        return {'FINISHED'}


class SoundPetalSynthDef(bpy.types.Node, FlowCustomTreeNode):
    bl_idname = 'SoundPetalSynthDef'
    bl_label = 'SynthDef Maker'

    synth_name = StringProperty(description='identifies this ugen collection')
    generated_synthdef = StringProperty()

    def init(self, context):
        self.inputs.new('FlowTransferSocket', 'master')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'synth_name', text='name')
        col.operator("node.sp_serialize_synthdef", text='make synthdef')

    def process(self):
        pass

    def get_args(self):
        pass


def register():
    bpy.utils.register_class(SoundPetalSynthDef)
    bpy.utils.register_class(MakeSynthDefOps)


def unregister():
    bpy.utils.unregister_class(SoundPetalSynthDef)
    bpy.utils.unregister_class(MakeSynthDefOps)
