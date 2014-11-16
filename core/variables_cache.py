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

soundpetal_vars = {}


# helper
def global_name(node):
    '''all variables must start lowercase'''
    return node.name.replace('.', '_').lower() + '__'


# helper
def get_variables_for_node(node):
    return [n for n in soundpetal_vars.keys() if n.startswith(name)]


def store_variable(node, var_name, var_value):
    name = global_name(node) + var_name
    soundpetal_vars[name] = var_value


def free_variables(node):
    name = global_name(node)
    names = get_variables_for_node(node)
    for n in names:
        del soundpetal_vars[n]


def get_variables(node):
    names = get_variables_for_node(node)
    if not names:
        return

    minidict = {}
    for n in names:
        minidict[n] = soundpetal_vars.get(n)
    return minidict


def free_all_variables():
    soundpetal_vars = {}
