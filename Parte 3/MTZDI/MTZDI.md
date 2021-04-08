param n default 30;
param m default 4;
set N ordered := {1..n};
set A := {(i,j) in {N,N}: i != j};

param lx{N} := Uniform(0,100.0);
param ly{N} := Uniform(0,100.0);
param d{N} := Uniform(1, 5);

param Q := sum{i in N} d[i]/m;

param c{(i,j) in A} := sqrt( (lx[i] - lx[j])^2 + (ly[i] - ly[j])^2 );

var x{A}, binary;
var z{N};

param nh default 0;
set H := {1..nh};
set S{H} within {N diff {1}};

param coeficiente{H};

minimize tour: sum{(i,j) in A} c[i,j] * x[i,j];

s.t. r1MTZ{i in N diff {1}}: sum{(i,j) in A} x[i,j] = 1;
s.t. r2MTZ{j in N diff {1}}: sum{(i,j) in A} x[i,j] = 1;
s.t. r3MTZ: sum{j in N: j != 1} x[1,j] = m;
s.t. r4MTZ: sum{i in N: i != 1} x[i,1] = m;
s.t. r5MTZ{(i,j) in A: j != 1}: z[j] >= z[i] + d[i] + Q*(x[i,j] - 1);
s.t. r6MTZ{i in N: i != 1}: z[i] >= d[i];
s.t. r7MTZ: z[1] >= 0;

s.t. r1DI{i in N diff {1}}: sum{(i,j) in A} x[i,j] = 1;
s.t. r2DI{j in N diff {1}}: sum{(i,j) in A} x[i,j] = 1;
s.t. r3DI: sum{(1,j) in A} x[1,j] = m;
s.t. r4DI: sum{(i,1) in A} x[i,1] = m;
s.t. r5DI{h in H: card(S[h]) >= 2 and card(S[h]) <= n - 1}: sum{(i,j) in A: i in S[h] and j in S[h]} x[i,j] <= card(S[h]) - coeficiente[h];

set T within N;
set V ordered within N default {};
set s;
param u;
param v;
param true := 1;
param false := 0;
param is_optimal default false;
param NEXT{N} default -1;
param PRED{N} default -1;
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
param Pontos_Visitados{N} default 0;
param mipgap;
param stop default false;
end;