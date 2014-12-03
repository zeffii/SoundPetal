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

    // auto ends because of doneAction: 2
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

x = Synth(\stab1);   // test

// a chord playing function
(
~playChord = {
	arg notes, volumes;

	notes.do{
		arg note, idx;
		Synth(\stab1, [freq: note.midicps, amp: volumes[idx]]);
		note.postln;
		idx.postln;
	}
};
)

~playChord.value([54,57,62],[0.3, 0.3, 0.3]);