param n > 0;	# Numero de nos

set N := {0..n-1};    # Conjunto de nos
set N1 := {1..n-1};   # Conjunto N \ {0}
param cx{N} >= 0;  # Distribuicao de locais
param cy{N} >= 0;  # Distribuicao de locais

set A := {(i,j) in {N,N}: i != j};	# Matriz dos arcos entre nos
param C{(i,j) in A} default sqrt( (cx[i] - cx[j])^2 + (cy[i] - cy[j])^2 );	# Matriz dos custos de cada arco entre os nos

var x{A}, binary;	# Variavel de decisao da rota ocorrer ou nao
var f{(i,j) in A, k in N1} >= 0;		# Porcentagem de fluxo com destino ao n� k que passa pelo arco i j 

minimize fo: sum{(i,j) in A} C[i,j] * x[i,j];	# Objetivo de minimizar a distancia percorrida

s.t. r1{i in N}: sum{(i,j) in A} x[i,j] = 1;	# A rota deve chegar a todo no uma vez
s.t. r2{j in N}: sum{(i,j) in A} x[i,j] = 1;	# A rota deve sair de todo no uma vez
s.t. r3{k in N1}: sum{(0,j) in A} f[0,j,k] = 1;			# Porcentagem total de cada produto que passa pela rota deve ser 100% = 1
s.t. r4{k in N1, j in N1 : k != j}: sum{(i,j) in A: i != k} f[i,j,k] = sum{(i,j) in A} f[j,i,k];
s.t. r5{k in N1}: sum{(i,k) in A} f[i,k,k] = 1;
s.t. r6{(i,j) in A, k in N1}: f[i,j,k] <= x[i,j];