param n default 300;
set N ordered := {1..n};
set N1 ordered := {2..n};
set A := {(i,j) in {N,N}: i != j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);

param c{(i,j) in A} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

var x{A} binary;
var f{(i,j) in A} >= 0;


minimize tour : sum{(i,j) in A} c[i,j] * x[i,j];

s.t. r1{i in N}: sum{(i,j) in A} x[i,j] = 1;
s.t. r2{j in N}: sum{(i,j) in A} x[i,j] = 1;
s.t. r3: sum{(1,j) in A} f[1,j] = n - 1;
s.t. r4{j in N1}: sum{(i,j) in A} f[i,j] - sum{(j,i) in A} f[j,i] = 1;
s.t. r5{(i,j) in A}: f[i,j] <= (n-1) * x[i,j];

param v;
param NEXT{N};
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param mipgap;
end;