param n > 0;	# Numero de nos

set N := {1..n};    # Conjunto de nos
param cx{N} >= 0;  # Distribuicao de locais
param cy{N} >= 0;  # Distribuicao de locais

set A := {(i,j) in {N,N}: i != j};	# Matriz dos arcos entre nos
param C{(i,j) in A} default sqrt( (cx[i] - cx[j])^2 + (cy[i] - cy[j])^2 );	# Matriz dos custos de cada arco entre os nos

param nsec default 0;
set H := {1..nsec};
set S{H} within N;

var x{A}, binary;	# Variavel de decisao da rota ocorrer ou nao

minimize of: sum{(i,j) in A} c[i,j] * x[i,j];	# Objetivo de minimizar a distancia percorrida

s.t. r1{i in N}: sum{(i,j) in A} x[i,j] = 1;	# A rota deve chegar a todo no uma vez
s.t. r2{j in N}: sum{(i,j) in A} x[i,j] = 1;	# A rota deve sair de todo no uma vez
s.t. r3{h in H: card(S[h]) >= 2 and card(S[h]) <= n - 1}: sum{(i,j) in A: i in S[h] and j in S[h]} x[i,j] <= card(S[h]) - 1;