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


class MakeSynthDefOps(bpy.types.Operator):
    bl_idname = "node.sp_serialize_synthdef"
    bl_label = 'Make SynthDef'

    def execute(self, context):
        ng = context.space_data.node_tree
        ng_id = ng.name

        temp_list = []

        def list_print(in_str):
            temp_list.append(in_str)

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
            list_print('    {0} = {1}{2}'.format(varname, varval, terminator))

        list_print('\n')

        for node in ng.nodes:
            arg_line = node.get_args()
            if arg_line:
                list_print('    ' + arg_line)

        list_print('});')

        print(osc_statemachine)

        print()
        for line in temp_list:
            print(line)

        return {'FINISHED'}


class SoundPetalSynthDef(bpy.types.Node, FlowCustomTreeNode):
    bl_idname = 'SoundPetalSynthDef'
    bl_label = 'SynthDef Maker'

    synth_name = StringProperty(description='identifies this ugen collection')

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
