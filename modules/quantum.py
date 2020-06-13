OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

u3(pi * 0.5,pi * 0.5,pi * 0.5) q[0];
u3(pi/2,pi/2,pi/2) q[1];
u3(pi/2,pi/2,pi/2) q[2];
x q[0];
x q[1];
x q[2];
h q[0];
cx q[1],q[0];
cx q[2],q[0];
h q[0];
id q[1];
id q[2];
x q[0];
x q[1];
x q[2];
h q[0];
h q[1];
h q[2];
barrier q[0];
barrier q[1];
barrier q[2];