(
s.boot;
Environment.clear;

~FlowClient = NetAddr.new("127.0.0.1", 7890);
NetAddr.localAddr;
)


(
OSCdef.new(\status,
    {
        arg msg, time, addr;
        "time: % origin: %\nmsg: %\n".postf(time, addr, msg);
    }, '/flow/status'
)

OSCdef.new(\evalSynthDef,
    {
        arg msg, time, addr;
        msg[1].asString.interpret;
    }, '/evalSynthDef'
)

OSCdef.new(\triggerSynth,
    {
        arg msg, time, addr;
        ~synth = Synth.new(msg[1]);
    }, '/triggerSynth'
)

OSCdef.new(\freeSynth,
    {
        // arg msg, time, addr;
        ~synth.free;
    },  '/freeSynth'
)

OSCdef.new(\setSynthArg,
    {
        arg msg, time, addr;
        msg[1].asSymbol.postln;
        msg[2].postln;
        ~synth.set(msg[1], msg[2].asFloat);
    },  '/setSynthArg'
)
)

s.freeAll;




