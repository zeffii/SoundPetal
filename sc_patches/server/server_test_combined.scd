(
// by default SuperCollider listens for input on port 57120
s.boot;
NetAddr.langPort;  // verify
)
s.plotTree;

// first try with monophonic synth
// from the docs http://doc.sccode.org/Guides/OSC_communication.html
(
f = { |msg, time, addr|
	// if(msg[0] != '/status.reply') {
	// 	"time: % sender: %\nmessage: %\n".postf(time, addr, msg);
	// };

	if(msg[0] == '/flow/evalSynthDef') {
	    msg[1].postln;
	    msg[1].asString.interpret;
	};

	if(msg[0] == '/flow/triggerSynth') {
        ~synth = Synth.new(msg[1]);
	};

	if(msg[0] == '/flow/freeSynth') {
        ~synth.free;
	};

	if(msg[0] == '/flow/freeAll') {
        s.freeAll;
	};

	if(msg[0] == '/flow/setSynthArg') {
		"setting % = %\n".postf(msg[1], msg[2].asFloat);
        ~synth.set(msg[1], msg[2].asFloat);
    };
};

thisProcess.addOSCRecvFunc(f);
);
s.plotTree;
s.freeAll;

//
// x = Synth.new(\tone, [\gate, 1]);  // test it
// x.set(\freq, 120);                 // change other arg variables
// x.set(\gate, 0);                   // gate=0 to release
//
s.freeAll;
s.plotTree;

// stop posting.
thisProcess.removeOSCRecvFunc(f);
