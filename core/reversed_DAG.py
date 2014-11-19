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

from collections import defaultdict
from FLOW.core.variables_cache import global_name
from FLOW.core.mechanisms import get_apex, prototype_cascade


def get_DAG(ng):
    varlist = []

    def varlist_print(_str_):
        varlist.append(_str_)

    apex = get_apex(ng)
    L = prototype_cascade(ng, apex)

    for node in L:
        arg_line = node.get_args()
        if arg_line:
            varlist_print('    ' + arg_line)

    return varlist
