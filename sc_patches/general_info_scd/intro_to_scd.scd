// execute this line
s.options.dump;

// set higher if you experience many 'late <some number>' messages 
// low is 64. high is 512 or more -- high will introduce latency, 
// but reduces underruns (clicking, garbled sound)
s.options.blockSize = 512;

// another option is to change the latency explicitely 
s.latency = 0.05  // 50 ms
s.latency = 0.2   // default, 5th of a second..

s.boot;