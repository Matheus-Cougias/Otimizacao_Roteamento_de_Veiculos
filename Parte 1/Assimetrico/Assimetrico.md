param n default 20;
set N ordered := {1..n};
set E := {(i,j) in {N,N}: i < j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);

param c{(i,j) in E} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

param nh default 0;
set H := {1..nh};
set S{H} default {}; 

var x{E} binary;

minimize tour : sum{(i,j) in E} c[i,j] * x[i,j];
s.t. r1{i in N}: sum{(i,j) in E} x[i,j] + sum{(j,i) in E} x[j,i] = 2;

s.t. sec{h in H}: sum{(i,j) in E: i in S[h] and j in S[h]} x[i,j] <= card(S[h]) - 1;


set T within N;
set _E within E default {};
set _N ordered within N default {};
param u;
param v;
param true := 1;
param false := 0;
param is_optimal default false;
param nhold default 0;
param nxt{N};
param lb;
param iteracao default 0;
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
end;