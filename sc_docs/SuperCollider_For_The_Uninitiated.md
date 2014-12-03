#### SuperCollider For The Uninitiated.

This paper aims to cover, quite rapidly, the important parts of the SC3 language to someone who understands the concept and practicality of a modular synth. It's not intended to be a primer or a pleasant read, think of it more as a quick reference, and an index of examples that explain concepts in deeper detail. If this paper is too abstract then search for the `SuperCollider 3 .pdf by David Michael Cottle 2006`. That's an extensive 400 page Free workbook.

Who am I? Let's just say I'm writing this paper to create a reference I can go back to and jump right to the parts of interest. SC3 is a big topic, and the docs are extensive but often distracting.

## Ugens

Broadly speaking; all things that either 1) produce sound or 2) produce a control signal. Some examples are Noise generators, Sine wave generators and Envelope generators. There are over 200 Ugens.

    SinOsc, Saw, LFNoise, RHPF, RLPF, BPF, Line, Env, EnvGen

## Signals

There are two main types of signal; `ar`, `kr`. There's a third type `ir` which I won't discuss (yet). `ar` stands for _Audio Rate_, and `kr` stands for _Control Rate_. Audio Rate generates values at the rate of the soundcard sample rate (44.1 / 48.0 / etc.) Control Rate generates values every n samples, where n is the size of your buffer, usually 64 by default but can be larger or smaller.

It doesn't make sense to update certain Ugen parameters more often than once per buffer chunk anyway, if it can't be perceived it is wasted computation. Signals at `.kr` are used to modify parameteres of Ugens that you can't hear.For instance the frequency of a SinOsc is an example of when it's OK to modify the parameter less frequently, there's a threshold of perception. There are exceptions to this, [read]().

    SinOsc.ar(330);   // will output at audio rate, values between -1 and 1
    SinOsc.kr(330);   // will output at buffer rate, values between -1 and 1

## Ugen parameters

Ugens output signals that are a function of their input parameters. The parameters available for each Ugen can be found doing ctrl+D / command+D with the name of the UGen highlighted -- this will spawn the SC3 Help Browser.

Specifically i'd like to mention a few, most of them share the same set of
arguments.

| UGen    |  Parameters / Defaults               | 
| ------- | ------------------------------------ |
| SinOSc  | freq=440, phase=0, mul=1, add=0      |
| Saw     | .. ..                                |
| TriOsc  | .. ..                                |

## Simple SynthDefs

```
s.boot;


(
SynthDef(\stab1, {
    arg 
    freq=440, 
    amp=0.4, 
    attack=0.02, 
    decay=1.2,
    level_0=1.0, 
    level_1=0.2, 
    level_2=0.01;
    
    var 
    env, 
    out, 
    signal=0;
    
    env = EnvGen.kr(Env.perc(attack, decay), doneAction: 2);
    signal = signal + SinOsc.ar(freq, mul: env* level_0);
    signal = signal + Saw.ar(freq, mul: env * level_1);
    signal = signal + PinkNoise.ar(freq, mul: env * level_2);
    signal = signal * amp;
    signal = Pan2.ar(signal, 0);
    Out.ar(0, signal)
    }

).add;
)

x = Synth(\stab1);
```

more more more? 

## variables, globals.

Global variables are prefixed with a `~`. `~some_variable`. The entire lowercase alphabet is available as predeclared global, however: `s` is best to leave untouched because it is used as a convenience for referencing the server.

## do loops
    
    ~notes = [54,57,62];
    ~volumes = [0.3, 0.3, 0.3];
    ~notes.do{
        arg note, idx;
        Synth(\stab1, [freq: note.midicps, amp: ~volumes[idx]]);
        note.postln;
        idx.postln;
    }

The equivalent python is (minus the synth line)

    notes = [54, 547, 62]
    volumes = [0.3, 0.3, 0.3]
    for idx, notes in enumerate(notes):
        print(note)
        print(idx)

Notice in SC3 args the element reference is first, then element index. In Python this is of course the other way around.

