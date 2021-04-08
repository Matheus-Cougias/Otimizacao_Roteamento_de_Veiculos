param n default 30;
param m default 4;
set N ordered := {1..n};
set Nc ordered := {1..n+1};
set Nc1 := Nc diff {1} diff {n+1};
set A := {(i,j) in {N,N}: i != j};
set Ac := {(i,j) in {Nc,Nc}: i != j};

param testex{N} := Uniform(0,100.0);
param testey{N} := Uniform(0,100.0);
param lx{i in Nc} := if (i == n+1) then testex[1] else testex[i];
param ly{i in Nc} := if (i == n+1) then testey[1] else testey[i];

param tested{N} := Uniform(1, 5);
param d{i in N} := if (i == n+1) then tested[1] else tested[i];

param Q := sum{i in N} d[i]/m;

param c{(i,j) in Ac} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

var x{Ac} binary;
var f{(i,j) in Ac} >= 0;

minimize tour: sum{(i,j) in Ac} c[i,j] * x[i,j];

s.t. r1{i in Nc1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r2{j in Nc1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r3{j in Nc1}: sum{(i,j) in Ac} (f[i,j] - f[j,i]) = 2 * d[j];
s.t. r4: sum{j in Nc diff {1}} f[1,j] = sum{i in Nc1} d[i];
s.t. r5: sum{i in Nc diff {1}} f[i,1] = m*Q - sum{i in Nc1} d[i];
s.t. r6: sum{(n+1,j) in Ac} f[n+1,j] = m*Q;
s.t. r7: sum{(i,n+1) in Ac} f[i,n+1] = 0;
s.t. r8{(i,j) in Ac: i < j}: f[i,j] + f[j,i] = Q*(x[i,j] + x[j,i]);


param v;
param NEXT{Nc};
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param mipgap;
end;