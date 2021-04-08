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
param d{i in Nc} := if (i == n+1) then tested[1] else tested[i];

param Q := sum{i in N} d[i]/m;

param c{(i,j) in Ac} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

param nh default 0;
set H := {1..nh};
set S{H} within {N diff {1}};

param coeficiente{H};

var x{Ac}, binary;
var f{(i,j) in Ac} >= 0;

minimize tour: sum{(i,j) in Ac} c[i,j] * x[i,j];

s.t. r1DI{i in Nc1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r2DI{j in Nc1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r3DI: sum{(1,j) in Ac} x[1,j] = m;
s.t. r4DI: sum{(i,n+1) in Ac} x[i,n+1] = m;
s.t. r5DI: sum{(i,1) in Ac} x[i,1] = 0;
s.t. r6DI: sum{(n+1,j) in Ac} x[n+1,j] = 0;
s.t. r7DI{h in H: card(S[h]) >= 2 and card(S[h]) <= n - 1}: sum{(i,j) in Ac: i in S[h] and j in S[h]} x[i,j] <= card(S[h]) - coeficiente[h];

s.t. r1DP{i in Nc1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r2DP{j in Nc1}: sum{(i,j) in Ac} x[i,j] = 1;
s.t. r3DP{j in Nc1}: sum{(i,j) in Ac} (f[i,j] - f[j,i]) = 2 * d[j];
s.t. r4DP: sum{j in Nc diff {1}} f[1,j] = sum{i in Nc1} d[i];
s.t. r5DP: sum{i in Nc diff {1}} f[i,1] = m*Q - sum{i in Nc1} d[i];
s.t. r6DP: sum{(n+1,j) in Ac} f[n+1,j] = m*Q;
s.t. r7DP: sum{(i,n+1) in Ac} f[i,n+1] = 0;
s.t. r8DP{(i,j) in Ac: i < j}: f[i,j] + f[j,i] = Q*(x[i,j] + x[j,i]);


set T within N;
set V ordered within Nc default {};
set s;
param u;
param v;
param true := 1;
param false := 0;
param is_optimal default false;
param NEXT{Nc} default -1;
param PRED{Nc} default -1;
param lb;
param iteracao default 0;
param inicio;
param nosTotais default 0;
param nosIteracao default 0;
param Rotas_Caminhoes{1..m} default 0;
param Rota_Caminhao default 0;
set Subrota default {};
param DemandaSubrota default 0;
param inicial;
param indice;
param Pontos_Visitados{Nc} default 0;
param mipgap;
param stop default false;
end;