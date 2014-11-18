SoundPetal
====

SuperCollider Wrapper for Blender's Custom Python Nodes.
License: GNU GPL 3.  

![img2](https://cloud.githubusercontent.com/assets/619340/5063043/11c664de-6dd7-11e4-98de-39a57b2f2641.png)

SoundPetal is a thin wrapper around SuperCollider 3 Ugens. Most of the node UIs are inherrited from the `SoundPetalUGen` SuperClass. `Ugen` classes are defined by succintly passing their name and arglist to [`core.node_factory.make_ugen_class`](). 

Certain nodes are not generated this way, like `in`, `out`, and `Make SynthDef`, these have dedicated node Class definitions because their UI interface is sufficiently different.