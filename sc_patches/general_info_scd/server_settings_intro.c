// if you hear clicks or get messages in the post window like 'late <some number>'
// then, for whatever reason, your soundcard isn't getting enough of each frame processed
// in time for the audio to be glitch-free
s.options.blockSize = 1024;   // must be a multiple of 64
s.latency = 1  // 1 second,  0.2 = 1/5 second etc.