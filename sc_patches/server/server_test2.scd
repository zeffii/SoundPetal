(
// by default SuperCollider listens for input on port 57120
s.boot;
NetAddr.langPort;  // verify
)
s.plotTree;

// first try with monophonic synth

(
OSCdef.new(
	\evalSynthDef, {
        arg msg;
	    msg[1].postln;
	    msg[1].asString.interpret;
    }, '/flow/evalSynthDef'
))

(
OSCdef.new(
	\triggerSynth, {
        arg msg, time, addr;
        // ~synth = Synth.new(msg[1]);
        ~synth = Synth.new(\tone, [\gate, 1]);
    }, '/flow/triggerSynth'
))

(
OSCdef.new(
	\freeSynth, {
        arg msg, time, addr;
        ~synth.free;
    },  '/flow/freeSynth'
))

(
OSCdef.new(
	\setSynthArg, {
        arg msg, time, addr;
        msg[1].asSymbol.postln;
        msg[2].postln;
        ~synth.set(msg[1], msg[2].asFloat);
    },  '/flow/setSynthArg'
))



x = Synth.new(\tone, [\gate, 1]);  // test it
x.set(\freq, 120);                 // change other arg variables
x.set(\gate, 0);                   // gate=0 to release

s.freeAll;
s.plotTree;