param n > 0;	# Numero de nos

set N := {0..n-1};    # Conjunto de nos
set N1 := {1..n-1};   # Conjunto N \ {0}
param cx{N} >= 0;  # Distribuicao de locais
param cy{N} >= 0;  # Distribuicao de locais

set A := {(i,j) in {N,N}: i != j};	# Matriz dos arcos entre nos
param C{(i,j) in A} default sqrt( (cx[i] - cx[j])^2 + (cy[i] - cy[j])^2 );	# Matriz dos custos de cada arco entre os nos

var x{A}, binary;	# Variavel de decisao da rota ocorrer ou nao
var f{A} >= 0;	# Vari�vel de fluxo imagin�rio

minimize fo: sum{(i,j) in A} C[i,j] * x[i,j];	# Objetivo de minimizar a distancia percorrida

s.t. r1{i in N}: sum{(i,j) in A} x[i,j] = 1;	# A rota deve chegar a todo no uma vez
s.t. r2{j in N}: sum{(i,j) in A} x[i,j] = 1;	# A rota deve sair de todo no uma vez
s.t. r3: sum{(0,j) in A} f[0,j] = n - 1;			# Quantidade total de produto imagin�rio deve ser de n - 1
s.t. r4{j in N1}: sum{(i,j) in A} f[i,j] - sum{(j,i) in A} f[j,i] = 1;		# Quantidade de produto que passa por cada subrota deve ser igual a 1
s.t. r5{(i,j) in A}: f[i,j] <= (n - 1) * x[i,j];