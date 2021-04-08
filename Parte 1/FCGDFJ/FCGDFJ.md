param n default 10;
set N ordered := {1..n};
set Nc ordered := {1..n+1};
set Nc1 := Nc diff {1} diff {n+1};
set A := {(i,j) in {N,N}: i != j};
set Ac := {(i,j) in {Nc,Nc}: i != j};

param testex{N} := Uniform(0,100.0);
param testey{N} := Uniform(0,100.0);

param lx{i in Nc} := if (i == n+1) then testex[1] else testex[i];
param ly{i in Nc} := if (i == n+1) then testey[1] else testey[i];

param c{(i,j) in Ac} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

param nh default 0;
set H := {1..nh};
set S{H} default {}; 

var x{Ac} binary;
var f{(i,j) in Ac} >= 0;

minimize tour: sum{(i,j) in Ac} c[i,j] * x[i,j];

s.t. r1{i in Nc: i != n+1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r2{j in Nc: j != 1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r3DFJ{h in H: card(S[h]) >= 2 and card(S[h]) <= n - 1}: sum{(i,j) in Ac: i in S[h] and j in S[h]} x[i,j] <= card(S[h]) - 1;
s.t. r4DFJ: x[1,n+1] = 0;
s.t. r3FCG: sum{(1,j) in Ac} f[1,j] = n - 1;
s.t. r4FCG: sum{(i,1) in Ac} f[i,1] = 0;
s.t. r5FCG: sum{(i,n+1) in Ac} f[i,n+1] = 0;
s.t. r6FCG: sum{(n+1,j) in Ac} f[n+1,j] = n - 1;
s.t. r7FCG{j in Nc1}: sum{(i,j) in Ac} f[i,j] - sum{(j,i) in Ac} f[j,i] = 2;
s.t. r8FCG{j in Nc1}: sum{(i,j) in Ac} f[i,j] + sum{(j,i) in Ac} f[j,i] = 2 * (n - 1);
s.t. r9FCG{(i,j) in Ac: i < j}: f[i,j] + f[j,i] = (n - 1) * (x[i,j] + x[j,i]);

set T within Nc;
set V ordered within Nc default {};
set s;
param u;
param v;
param true := 1;
param false := 0;
param is_optimal default false;
param stop default false;
param mipgap default 0;
param NEXT{Nc};
param lb;
param iteracao default 0;
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
end;