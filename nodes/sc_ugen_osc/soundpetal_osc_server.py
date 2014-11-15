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


default_synthdef = r"""
(
SynthDef.new(\tone, {
    arg freq=40, nharm=12, detune=0.2, gate=0,
    pan=0, amp=1, out=0;
    var sig, env;
    env = EnvGen.kr(Env.adsr(0.05, 0.1, 0.5, 3), gate);
    sig = Blip.ar(
        freq *
        LFNoise1.kr(0.2!16).bipolar(detune.neg, detune).midiratio,
        nharm
    );
    sig = sig * LFNoise1.kr(0.5!16).exprange(0.1, 1);
    sig = Splay.ar(sig);
    sig = Balance2.ar(sig[0], sig[1], pan);
    sig = sig * env * amp;
    Out.ar(out, sig);
}).add
)
"""


def start_server_comms():
    ip = "127.0.0.1"
    port = 57120  # SuperCollider
    client = udp_client.UDPClient(ip, port)
    osc_statemachine['status'] = RUNNING
    osc_msg = osc_message_builder.OscMessageBuilder
    osc_statemachine['osc_msg'] = osc_msg
    osc_statemachine['client'] = client


class SoundPetalOscServerOps(bpy.types.Operator, object):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.spflow_osc_server"
    bl_label = "start n stop osc server"

    mode = StringProperty(default='')
    node_name = StringProperty(default='')
    node_group = StringProperty(default='')

    def event_dispatcher(self, context, type_op):
        if type_op == 'start':
            context.node.active = True
            # start osc server.
            status = osc_statemachine.get('status')
            if status in {FOUND, DISABLED}:
                print('opening server comms')
                start_server_comms()
            else:
                print('pythonosc module is needed but not found')

        if type_op == 'end':
            # doesn't end OSC listener.
            osc_statemachine['status'] == DISABLED
            context.node.active = False

    def execute(self, context):
        n = context.node
        self.node_name = context.node.name
        self.node_group = context.node.id_data.name
        self.event_dispatcher(context, self.mode)
        return {'RUNNING_MODAL'}


def send_synthdef_str(_str_):
    osc_msg = osc_statemachine.get('osc_msg')
    if osc_msg:

        msg = osc_msg(address='/flow/evalSynthDef')
        msg.add_arg(_str_)
        msg = msg.build()

        client = osc_statemachine.get('client')
        print('sending synthdef over osc')
        client.send(msg)


class SoundPetalSendSynthdef(bpy.types.Operator, object):
    """Send SynthDef over OSC"""
    bl_idname = "wm.spflow_eval_synthdef"
    bl_label = "start n stop osc server"

    mode = StringProperty(default='')
    node_name = StringProperty(default='')
    node_group = StringProperty(default='')

    def event_dispatcher(self, context, type_op):
        if type_op == 'send':
            if not osc_statemachine['status'] == RUNNING:
                return
            else:
                print('sending synthdef to operator')
                send_synthdef_str(default_synthdef)

    def execute(self, context):
        n = context.node
        self.node_name = context.node.name
        self.node_group = context.node.id_data.name
        self.event_dispatcher(context, self.mode)
        return {'RUNNING_MODAL'}


class SoundPetalOscServer(bpy.types.Node, FlowCustomTreeNode):
    '''
    SoundPetalOscServer
    : intended to handle io of OSC messages

    '''

    bl_idname = 'SoundPetalOscServer'
    bl_label = 'SP OSC Server'

    draw_to_host = BoolProperty(
        description="switch it on and off",
        default=0, name='draw_to_host')

    active = BoolProperty(
        description="current state",
        default=0, name='comms on')

    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        col = layout.column()
        tstr = 'start' if not self.active else 'end'
        col.operator('wm.spflow_osc_server', text=tstr).mode = tstr
        col.operator('wm.spflow_eval_synthdef', text='send').mode = 'send'

    def process(self):
        pass


def register():
    bpy.utils.register_class(SoundPetalOscServer)
    bpy.utils.register_class(SoundPetalOscServerOps)
    bpy.utils.register_class(SoundPetalSendSynthdef)


def unregister():
    bpy.utils.unregister_class(SoundPetalOscServer)
    bpy.utils.unregister_class(SoundPetalOscServerOps)
    bpy.utils.unregister_class(SoundPetalSendSynthdef)
