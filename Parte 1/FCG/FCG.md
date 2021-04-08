param n default 300;
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


var x{Ac} binary;
var f{(i,j) in Ac} >= 0;

minimize tour: sum{(i,j) in Ac} c[i,j] * x[i,j];

s.t. r1{i in Nc: i != n+1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r2{j in Nc: j != 1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r3: sum{(1,j) in Ac} f[1,j] = n - 1;
s.t. r4: sum{(i,1) in Ac} f[i,1] = 0;
s.t. r5: sum{(i,n+1) in Ac} f[i,n+1] = 0;
s.t. r6: sum{(n+1,j) in Ac} f[n+1,j] = n - 1;
s.t. r7{j in Nc1}: sum{(i,j) in Ac} f[i,j] - sum{(j,i) in Ac} f[j,i] = 2;
s.t. r8{j in Nc1}: sum{(i,j) in Ac} f[i,j] + sum{(j,i) in Ac} f[j,i] = 2 * (n - 1);
s.t. r9{(i,j) in Ac: i < j}: f[i,j] + f[j,i] = (n - 1) * (x[i,j] + x[j,i]);

param v;
param NEXT{Nc};
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param mipgap;
end;