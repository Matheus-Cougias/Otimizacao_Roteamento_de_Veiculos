param n default 20;
set N ordered := {1..n};
set A := {(i,j) in {N,N}: i != j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);

param c{(i,j) in A} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

param nh default 0;
set H := {1..nh};
set S{H} default {}; 

var x{A} binary;

minimize tour: sum{(i,j) in A} c[i,j] * x[i,j];
s.t. r1{i in N}: sum{(i,j) in A} x[i,j] = 1;
s.t. r2{j in N}: sum{(i,j) in A} x[i,j] = 1;
s.t. r3{h in H: card(S[h]) >= 2 and card(S[h]) <= n - 1}: sum{(i,j) in A: i in S[h] and j in S[h]} x[i,j] <= card(S[h]) - 1;

set T within N;
set V ordered within N default {};
set s;
param u;
param v;
param true := 1;
param false := 0;
param is_optimal default false;
param NEXT{N};
param lb;
param iteracao default 0;
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
end;