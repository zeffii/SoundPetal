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

flowcache = {}


def ident(socket):
    return (hash(socket.node.name), hash(socket.name))


def from_ident(socket):
    link = socket.links[0]
    from_name = link.from_node.name
    from_socket = link.from_socket.name
    return (hash(from_name), hash(from_socket))


def cache_wipe():
    global flowcache
    flowcache = {}


def cache_set(socket, data):
    global flowcache
    flowcache[ident(socket)] = data


def cache_get(socket):
    return flowcache.get(from_ident(socket), [])
