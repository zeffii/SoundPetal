FLOW
====

GNU GPL 3.  "Just Another Nodes Framework" for Blender

My goal is to implement something that works for me, the way I like it. I'm not seeking to please anyone or fullfil feature requests (but you are welcome to suggest them, i'm not closed to cool ideas).

This implementation focusses on Geometry with a heavy reliance on NumPy's `np.Array` instead of Python's generic `Lists`. Using NumPy allows for very fast Linear Algebra operations without first casting to mathutils `Vector() ` and `Matrix()` etc. The closest Blender analogue to FLOW is Sverchok, so if you are comfortable with Sverchok then all will be familiar but admittedly different. A massive caveat though: FLOW is experimental by nature.

Right now FLOW is a test area to experiment with a bit more than just a node, it aims to nodefy the parts of NumPy which are obviously handy. For geometry an Object can be described as an `n*4` array of `xyzw` Vertices. The W won't often be explicitely set by the user - it's there implicitely to make the `n*4 x 4*4` Matrix Math possible.
