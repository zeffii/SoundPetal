s.boot;

(
SynthDef.new(\padsyn2, {
	arg
	freq=440,
	amp=0.2,
	attack=0.1,
	decay=2,
	pan=0,
	filtfreq=400,
	fibrato=5;

	var out, signal, env;

	env = EnvGen.ar(Env.perc(attack, decay), doneAction:2);
	signal = Saw.ar(freq, env);

	signal = RLPF.ar(signal, SinOsc.kr(fibrato, mul:1200, phase: -0.5pi, add:2600));
	signal = RLPF.ar(signal, filtfreq);
	out = Pan2.ar(signal*amp, pan);
	// out = FreeVerb2.ar(out[0], out[1]);
	Out.ar(0, out);
	}
).play;
)

(
~chords = [
	[59, 61, 66],
    [52, 54, 57, 64],
	[49, 54, 57, 64]
];
)

(

~trif = {
	    arg idx=0, ffreq=400;
		~chords[idx].midicps.do{
			arg freq;
			Synth.new(\padsyn2, [\freq, freq, \fibrato, freq/225, \filtfreq, ffreq]);
		}
}
)

(
// "Sheduling Routines"
r = Routine({
    var delta;
    loop {
		delta = [0.125, 0.125, 0.25].choose*1.7;
		~trif.value(idx: [0,1,2].choose, ffreq: exprand(100, 1100));
        delta.yield;
    }
});

r.next;

TempoClock.default.sched(0, r);
)

r.stop;