param n default 10;
param m default 2;
set N ordered := {1..n};
set A := {(i,j) in {N,N}: i != j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);
param d{N} := Uniform(1, 5);

param Q := sum{i in N} d[i]/m;

param c{(i,j) in A} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

var x{A}, binary;
var z{N};

minimize tour: sum{(i,j) in A} c[i,j] * x[i,j];

s.t. r1{i in N diff {1}}: sum{(i,j) in A} x[i,j] = 1;
s.t. r2{j in N diff {1}}: sum{(i,j) in A} x[i,j] = 1;
s.t. r3: sum{j in N: j != 1} x[1,j] = m;
s.t. r4: sum{i in N: i != 1} x[i,1] = m;
s.t. r5{(i,j) in A: j != 1}: z[j] >= z[i] + d[i] + Q*(x[i,j] - 1);
s.t. r6{i in N: i != 1}: z[i] >= d[i];
s.t. r7: z[1] >= 0;

param v;
param root_it;
param NEXT{N};
param PRED{N};
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param mipgap;
end;