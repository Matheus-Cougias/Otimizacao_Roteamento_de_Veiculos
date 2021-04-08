param n default 200;
set N ordered := {1..n};
set N1 ordered := {2..n};
set A := {(i,j) in {N,N}: i != j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);

param c{(i,j) in A} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

var x{A}, binary;
var f{(i,j) in A, k in N1} >= 0;

minimize tour: sum{(i,j) in A} c[i,j] * x[i,j];

s.t. r1{i in N}: sum{(i,j) in A} x[i,j] = 1;
s.t. r2{j in N}: sum{(i,j) in A} x[i,j] = 1;
s.t. r3{k in N1}: sum{(1,j) in A} f[1,j,k] = 1;
s.t. r4{k in N1, j in N1 : k != j}: sum{(i,j) in A: i != k} f[i,j,k] = sum{(i,j) in A} f[j,i,k];
s.t. r5{k in N1}: sum{(i,k) in A} f[i,k,k] = 1;
s.t. r6{(i,j) in A, k in N1}: f[i,j,k] <= x[i,j];

param v;
param NEXT{N};
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param mipgap;
end;