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
from bpy.props import BoolProperty, BoolVectorProperty, StringProperty, FloatProperty

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode

FOUND = 1
RUNNING = 3
DISABLED = 2
NOT_FOUND = 0

try:
    from pythonosc import osc_message_builder
    from pythonosc import udp_client
    STATUS = FOUND
except:
    print('python osc not found!')
    STATUS = NOT_FOUND

osc_statemachine = {'status': STATUS}


def start_server_comms():
    ip = "127.0.0.1"
    # port = 6449 # renoise
    port = 57120 # SuperCollider
    client = udp_client.UDPClient(ip, port)
    osc_statemachine['status'] = RUNNING
    osc_msg = osc_message_builder.OscMessageBuilder
    osc_statemachine['osc_msg'] = osc_msg
    osc_statemachine['client'] = client


def trigger_event():
    # can change for each trigger.
    instrument = -1
    track = 0
    note_val = 60
    velocity = 90
    note_out_list = [instrument, track, note_val, velocity]

    # with more nodes it will become necessary to include
    # identifiers.
    osc_msg = osc_statemachine.get('osc_msg')
    if osc_msg:
        # msg = osc_msg(address="/renoise/trigger/note_on")
        msg = osc_msg(address="/main/toggle1")
        for i in note_out_list:
            msg.add_arg(i)

        print(note_out_list)
        msg = msg.build()
        client = osc_statemachine.get('client')
        client.send(msg)


class FlowOscServerOps(bpy.types.Operator, object):

    """Operator which runs its self from a timer"""
    bl_idname = "wm.flow_osc_server"
    bl_label = "start n stop osc server"

    _timer = None
    mode = StringProperty(default='')
    node_name = StringProperty(default='')
    node_group = StringProperty(default='')
    speed = FloatProperty()

    def modal(self, context, event):
        if self.node_group and self.node_name:
            ng = bpy.data.node_groups.get(self.node_group)
            n = ng.nodes[self.node_name]
        else:
            return {'PASS_THROUGH'}

        if not (event.type == 'TIMER'):
            return {'PASS_THROUGH'}

        if not n.active:
            self.cancel(context)
            return {'FINISHED'}

        self.process(ng, n)
        return {'PASS_THROUGH'}

    def process(self, ng, n):
        ''' reaches here only if event is TIMER and n.active '''
        trigger_event()
        print('meee!', ng, n)

    def event_dispatcher(self, context, type_op):
        if type_op == 'start':
            context.node.active = True
            wm = context.window_manager
            self._timer = wm.event_timer_add(self.speed, context.window)
            wm.modal_handler_add(self)

            # start osc server.
            status = osc_statemachine.get('status')
            if status in {FOUND, DISABLED}:
                start_server_comms()
            else:
                print('pythonosc module is needed but not found')

        if type_op == 'end':
            osc_statemachine['status'] == DISABLED
            context.node.active = False

    def execute(self, context):
        n = context.node
        self.node_name = context.node.name
        self.node_group = context.node.id_data.name

        self.event_dispatcher(context, self.mode)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


class FlowOscServer(bpy.types.Node, FlowCustomTreeNode):

    ''' FlowOscServer '''
    bl_idname = 'FlowOscServer'
    bl_label = 'OSC Server'

    draw_to_host = BoolProperty(
        description="switch it on and off", default=0, name='draw_to_host')
    active = BoolProperty(
        description="current state", default=0, name='comms on')
    State = FloatProperty(default=1.0, name='State')
    speed = FloatProperty(default=1.0)

    def init(self, context):
        self.outputs.new('FlowSinkHoleSocket', "send")

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'speed')
        flash_operator = 'wm.flow_osc_server'
        tstr = 'start' if not self.active else 'end'

        osc_serv = col.operator(flash_operator, text=tstr)
        osc_serv.mode = tstr
        osc_serv.speed = self.speed

    def process(self):
        # self.outputs[0].fset(self.seq_row_1[:])
        pass


def register():
    bpy.utils.register_class(FlowOscServer)
    bpy.utils.register_class(FlowOscServerOps)


def unregister():
    bpy.utils.unregister_class(FlowOscServer)
    bpy.utils.unregister_class(FlowOscServerOps)
