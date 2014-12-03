s.boot;

s.options.numOutputBusChannels = 4;
s.options.numInputBusChannels = 2;
s.reboot;

(
SynthDef.new(\reverb, {
	arg in, out=0;
	var sig;
	sig = In.ar(in, 2);  // 1, here monophonic
	sig = FreeVerb.ar(sig, 2.6, 2.2, 3.7)!2;  // !2 for 2 channels
	Out.ar(out, sig);
}).add;
)


(
SynthDef.new(\padsyn2, {
	arg
	freq=440,
	amp=0.2,
	attack=0.1,
	decay=2,
	pan=0,
	filtfreq=400,
	fibrato=5,  // filter sweep sin rate
	out=0;
	var signal, env;

	env = EnvGen.ar(Env.perc(attack, decay), doneAction:2);
	signal = Saw.ar(freq, env);

	signal = RLPF.ar(signal, SinOsc.kr(fibrato, mul:1200, phase: -0.5pi, add:2600));
	signal = RLPF.ar(signal, filtfreq);
	signal = Pan2.ar(signal*amp, pan);
	Out.ar(out, signal);
	}
).play;
)

/// TEST
y = Synth.new(\reverb, [\in, ~reverbBus]);   // do first
x = Synth.new(\padsyn2, [\out, ~reverbBus]);    // do second.
x.free;
y.free;


~reverbBus = Bus.audio(s, 2);  //mono. belongs to local server s
~reverbUnit = Synth.new(\reverb, [\in, ~reverbBus], s);


(
~chords = [
	[59, 61, 66],
    [52, 54, 57, 64],
	[49, 54, 57, 64],
	[42, 54, 57, 74]
];
)


(

~trif = {
	    arg idx=0, ffreq=400;
		~chords[idx].midicps.do{
			arg freq;
			Synth.new(\padsyn2, [
			    \freq, freq,
			    \fibrato, freq*0.02.reciprocal,
			    \filtfreq, ffreq,
			    \out, ~reverbBus.index
		    ], s);
		}
}
)


(
// "Sheduling Routines"
r = Routine({
    var delta;
	var idx = 0, times = [0.125, 0.125, 0.25];
    loop {
		delta = times.at(idx);
		~trif.value(idx: idx, ffreq: exprand(700, 1100));
		idx = idx + 1;
		if (idx > (times.size-1)) {
			idx = 0;
		};
        delta*1.5.yield;
    }
});

r.next;

TempoClock.default.sched(0, r);
)

r.stop;


