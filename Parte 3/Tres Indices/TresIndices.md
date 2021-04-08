param n default 30;
param m default 4;
set N ordered := {1..n};
set K ordered := {1..m};
set A := {(i,j) in {N,N}: i != j};
set B := {(i,k) in {N,K}: i != 1};
set C := {(i,j,k) in {N,N,K}: i != j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);
param d{N} := Uniform(1, 5);

param Q := sum{i in N} d[i]/m;

param c{(i,j) in A} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

param nh default 0;
set H := {1..nh};
set S{H} within {N diff {1}};

var x{C}, binary;
var y{B}, binary;

minimize tour: sum{k in K}(sum{(i,j) in A}( c[i,j] * x[i,j,k]));

s.t. r1{k in K}: sum{(1,j) in A} x[1,j,k] = 1;
s.t. r2{k in K}: sum{(i,1) in A} x[i,1,k] = 1;
s.t. r3{k in K}: sum{i in N diff {1}} d[i] * y[i,k] <= Q;
s.t. r4{i in N diff {1}}: sum{k in K} y[i,k] = 1;
s.t. r5{i in N diff {1}, k in K}: sum{(i,j) in A} x[i,j,k] = y[i,k];
s.t. r6{j in N diff {1}, k in K}: sum{(i,j) in A} x[i,j,k] = y[j,k];
s.t. r7{k in K, h in H, z in S[h]: card(S[h]) >= 2 and card(S[h]) <= n - 1}: sum{(i,j) in A: i in S[h] and j in S[h]} x[i,j,k] <= (sum{i in S[h]} y[i,k]) - y[z,k]; 
s.t. r8{k1 in K,k2 in K: k1 < k2}: sum{(i,k2) in B} y[i,k2] <= sum{(i,k1) in B}y[i,k1];




set T within N;
set V ordered within N default {};
set W ordered within K default {};
set s;
param u;
param v;
param true := 1;
param false := 0;
param is_optimal default false;
param NEXT{N,K};
param CAMINHAO{N} default 0;
param PRED{N,K} default 0;
param NumeroRotas default 0;
param lb;
param iteracao default 0;
param indice default 0;
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param banivel default 0;
end;