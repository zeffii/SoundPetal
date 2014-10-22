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
    FloatProperty, IntProperty, EnumProperty, BoolProperty, StringProperty)

from FLOW.core.mechanisms import updateSD
from FLOW.node_tree import FlowCustomTreeNode


class FlowArrayRandomWSeed(bpy.types.Node, FlowCustomTreeNode):
    '''
    FlowArrayRandomWSeed
    ==================

    allows the creation of an array of random Int or Float

    '''
    bl_idname = 'FlowArrayRandomWSeed'
    bl_label = 'Array Randoms'

    inclusive = BoolProperty(description="includes max", update=updateSD)

    Seed = IntProperty(name="Seed", default=0, step=1, update=updateSD)
    Elements = IntProperty(name="Elements", min=1, default=10, step=1, update=updateSD)
    I_MIN = IntProperty(name='I_MIN', default=0, step=1, update=updateSD)
    I_MAX = IntProperty(name='I_MAX', default=2, step=1, update=updateSD)
    F_MIN = FloatProperty(name='F_MIN', default=0.0, step=0.1, update=updateSD)
    F_MAX = FloatProperty(name='F_MAX', default=1.0, step=0.1, update=updateSD)
    INT = IntProperty(name='INT', default=2, step=1, update=updateSD)
    FLOAT = FloatProperty(name='FLOAT', default=0.0, step=0.1, update=updateSD)

    int_valstr = StringProperty()
    float_valstr = StringProperty()
    seed_valstr = StringProperty()

    type_options = [
        ("INT", "Random Int", "", 0),
        ("FLOAT", "Random Float", "", 1),
    ]

    random_type = EnumProperty(
        items=type_options,
        name="Type of Random",
        description="",
        default="INT",
        update=updateSD)

    def init(self, context):
        new_input = self.inputs.new
        a = new_input('FlowScalarSocket', 'I_MIN')
        a.prop_name = 'I_MIN'
        a.enabled = True

        b = new_input('FlowScalarSocket', 'I_MAX')
        b.prop_name = 'I_MAX'
        b.enabled = True

        c = new_input('FlowScalarSocket', 'F_MIN')
        c.prop_name = 'F_MIN'
        c.enabled = False

        d = new_input('FlowScalarSocket', 'F_MAX')
        d.prop_name = 'F_MAX'
        d.enabled = False

        f = new_input('FlowScalarSocket', 'Elements')
        f.prop_name = 'Elements'
        f.enabled = True

        g = new_input('FlowScalarSocket', 'Seed')
        g.prop_name = 'Seed'
        g.enabled = True

        self.outputs.new('FlowArraySocket', "val")

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'random_type', text='')
        if self.random_type == 'INT':
            col.prop(self, 'inclusive', text='Inclusive')

    def process(self):

        # http://docs.scipy.org/doc/numpy/reference/routines.random.html
        # this is but a quick implementation

        # get element count
        inputs = self.inputs
        r_num = int(self.inputs['Elements'].fget2())
        r_num = max(r_num, 1)  # forces minimum length of 1

        # hide unhide sockets depending on type
        int_mode = (self.random_type == 'INT')
        inputs['I_MIN'].enabled = int_mode
        inputs['I_MAX'].enabled = int_mode
        inputs['F_MIN'].enabled = not int_mode
        inputs['F_MAX'].enabled = not int_mode

        # get seed
        seed = self.inputs['Seed']
        seed_val = int(seed.fget2())
        self.seed_valstr = str(seed_val)
        np.random.seed(seed_val)

        if int_mode:
            r_min = inputs['I_MIN'].fget2()
            r_max = inputs['I_MAX'].fget2()
            self.int_valstr = str(r_min) + '..' + str(r_max)
            if self.inclusive:
                val = np.random.random_integers(r_min, r_max, size=r_num)
            else:
                val = np.random.randint(r_min, r_max, size=r_num)

        else:
            r_min = inputs['F_MIN'].fget2()
            r_max = inputs['F_MAX'].fget2()
            val = np.random.random_sample((r_num,)) * (r_max-r_min) + r_min
            self.float_valstr = str(round(r_min, 3)) + '..' + str(round(r_max, 3))

        self.outputs[0].fset(val)

    def draw_label(self):
        if self.hide:
            if self.random_type == "INT":
                rng = self.int_valstr
            else:
                rng = self.float_valstr

            msg = 'RND {rng} | S {s}'
            return msg.format(rng=rng, s=self.seed_valstr)

        return self.bl_label


def register():
    bpy.utils.register_class(FlowArrayRandomWSeed)


def unregister():
    bpy.utils.unregister_class(FlowArrayRandomWSeed)
