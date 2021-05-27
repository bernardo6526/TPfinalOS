# Lembre-se de usar um SOLVER que aceite Programação Linear Inteira
# ampl: option solver cplex;
set itens;


param capacidade:=6; # Capacidade Máxima da Mochila

param valor {j in itens}; # vetor de valor
param peso {j in itens}; # vetor de pesos
param mitico {j in itens}; # vetor de mitico
param bota {j in itens}; # vetor de bota


var X {i in itens} integer >= 0; # variáveis de decisao (vetor X)

#maximiza o ganho
maximize Status: 
sum {i in itens} valor[i] * X[i];

#nao pode ultrapassar 6 itens
subject to Capacidade: 
sum {j in itens} peso[j] * X[j] <= capacidade;

#nao pode levar itens repetidos
subject to Item_Unico {j in itens}:
X[j] <= 1;

#nao pode levar mais de 1 item do tipo mitico
subject to Mitico_Unico:
sum {j in itens} mitico[j] * X[j] <= 1;

#nao pode levar mais de 1 item do tipo bota
subject to Bota_Unica:
sum {j in itens} bota[j] * X[j] <= 1;


