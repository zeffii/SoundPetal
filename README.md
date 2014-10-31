FLOW
====

GNU GPL 3.  Geometry Nodes for Blender

Based on NumPy's `np.Array` instead of Python's generic `Lists`. Using NumPy allows for very fast Linear Algebra operations and bypassing the use of bpy mathutils `Vector() ` and `Matrix()` etc. which are too slow for this purpose. The closest Blender analogue to FLOW is Sverchok, so if you are comfortable with Sverchok it will all be familiar but admittedly different. A massive caveat though: FLOW is experimental by nature.

Right now FLOW is a test area to experiment with a bit more than just a node, it aims to nodefy the parts of NumPy which are obviously handy. For geometry an Object can be described as an `n*4` array of `xyzw` Vertices. The W won't often be explicitely set by the user - it's there implicitely to make the `n*4 x 4*4` Matrix Math possible.
