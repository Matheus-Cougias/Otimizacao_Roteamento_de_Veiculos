import math
import random
import time
import numpy
from prettytable import PrettyTable


def Gera_Instancia(n):
    Pontos = []
    for i in range(0, n):
        X = random.uniform(0, 30)
        Y = random.uniform(0, 30)
        Pontos.append((X, Y))
    Distancias = numpy.zeros((n, n))
    i = 0
    while i < n:
        j = 0
        while j < n:
            Distancias[i][j] = math.sqrt((Pontos[i][0] - Pontos[j][0]) ** 2 + (Pontos[i][1] - Pontos[j][1]) ** 2)
            j += 1
        i += 1
    return Pontos, Distancias


def Gera_Solucao_Inicial(n):
    pontos = list(range(1, n))
    Rota = [0]
    while len(pontos) > 0:
        x = random.choice(pontos)
        Rota.append(x)
        pontos.remove(x)
    Rota.append(Rota[0])
    return Rota


def Gera_Tempo_Atendimento(n):
    Tempo = [0]
    for i in range(1, n):
        t = random.randint(0, 10)
        Tempo.append(t)
    return Tempo


def Gera_Janelas(n, rota, atendimento, distancia):
    tempoChegada = [0]
    tempo = atendimento[0]
    i = 1
    while i < len(rota) - 1:
        tempo += distancia[i - 1][i]
        tempoChegada.append(tempo)
        tempo += atendimento[i]
        i += 1
    janelas = [(0, random.randint(0, 50))]
    for i in range(1, n):
        min = tempoChegada[i] - random.randint(0, 50)
        if min < 0:
            min = 0
        max = tempoChegada[i] + random.randint(0, 50)
        janelas.append((min, max))
    return janelas


def Ordena(n, entrada, rota):
    vetor = [0] * n
    for i in rota:
        vetor[rota[i]] = entrada[i]
    return vetor

def Calcula_Custo(rotaAleatoria, atendimento, distancia):
    tempo = atendimento[0]
    i = 1
    while i < len(rotaAleatoria) - 1:
        tempo += distancia[i - 1][i]
        tempo += atendimento[i]
        i += 1
    return tempo

def Calcula_Clientes_Atendidos(solucao, custoCliente, janelas):
    total = 0
    for i in range(0, len(solucao)-1):
        if custoCliente[i] <= janelas[solucao[i]][1]:
            if custoCliente[i] >= janelas[solucao[i]][0]:
                total += 1
    return total

def Calcula_Custos(solucao, distancias, atendimento):
    custoTotal = atendimento[0]
    custoCliente = [0]
    for i in range(0, len(solucao)-1):
        custoTotal += distancias[solucao[i]][solucao[i+1]]
        custoCliente.append(custoTotal)
        custoTotal += atendimento[solucao[i]]
    i = solucao[-1]
    j = solucao[0]
    custoTotal += distancias[i][j]
    return custoTotal, custoCliente


'''
No caso da heur??stica, realizei uma modifica????o que far?? com que n??o seja escolhido o vizinho mais pr??ximo, mas
sim o ponto onde a m??dia da janela de tempo seja menor, dessa maneira buscando atender sempre o pr??ximo cliente
com o tempo "mais cr??tico" O c??digo come??ar?? a partir do cliente inicial da janela de tempo, que no caso ?? o
primeiro cliente da rota aleat??ria gerada. Nem sempre a rota final est?? saindo com valores aceit??veis para as
janelas de tempo.
'''
def Heuristica_Vizinho_Proximo(n, janelas, distancias, atendimento, rotaInicial):
    inicio = rotaInicial[0]
    custo = atendimento[inicio]
    custoCliente = [0]
    S = [inicio]
    V = list(range(n))
    V.remove(inicio)
    medias = []
    i = 0
    while i < n:
        media = (janelas[i][0] + janelas[i][1])/2
        medias.append(media)
        i += 1
    while len(V) > 0:
        i = S[-1]
        j1, med1 = min([(j, medias[j]) for j in V], key=lambda k: k[1])
        V.remove(j1)
        S.append(j1)
        custo += distancias[i][j1]
        if custo < janelas[j1][0]:
            custo = janelas[j1][0]
        custoCliente.append(custo)
        custo += atendimento[j1]
    i = S[-1]
    j = S[0]
    custo += distancias[i][j]
    S.append(j)
    return S, custo, custoCliente

'''
Na heur??stica de melhoria pensei em montar uma heur??stica que troca os pontos de lugar na solu????o gerada pela 
heur??stica do vizinho mais pr??ximo. Dessa maneira, ele adotar?? a nova solu????o caso a solu????o atual tenha mais
clientes sendo atendidos dentro de sua janela de tempo. No caso desse n??mero de clientes sendo igual nas
duas solu????es comparadas, ele adotar?? aquela solu????o que tem o menor custo final. Para os casos onde o resultado
da heur??stica inicial atendeu um baixo n??mero de janelas, a heur??stica de melhoria se mostrou bem eficaz.
'''
def Melhoria(solucaoInicial, custoInicial, custoClientes, janelas, distancias, atendimento):
    melhorSolucao = solucaoInicial
    melhorCusto = custoInicial
    melhorCustoClientes = custoClientes
    melhorTotal = Calcula_Clientes_Atendidos(melhorSolucao, melhorCustoClientes, janelas)
    for i in range(1, len(solucaoInicial)-2):
        for j in range(1, len(solucaoInicial)-2):
            if j > i:
                solucaoAtual = solucaoInicial.copy()
                auxi = solucaoAtual[i]
                auxj = solucaoAtual[j]
                solucaoAtual[i] = auxj
                solucaoAtual[j] = auxi
                custoSolucaoAtual, custoClienteAtual = Calcula_Custos(solucaoAtual, distancias, atendimento)
                clientesAtendidosAtual = Calcula_Clientes_Atendidos(solucaoAtual, custoClienteAtual, janelas)
                if clientesAtendidosAtual > melhorTotal:
                    melhorSolucao = solucaoAtual
                    melhorCusto = custoSolucaoAtual
                    melhorCustoClientes = custoClienteAtual
                    melhorTotal = clientesAtendidosAtual
                elif clientesAtendidosAtual == melhorTotal:
                    if custoSolucaoAtual < melhorCusto:
                        melhorSolucao = solucaoAtual
                        melhorCusto = custoSolucaoAtual
                        melhorCustoClientes = custoClienteAtual
                        melhorTotal = clientesAtendidosAtual
    return melhorSolucao, melhorCustoClientes, melhorCusto



def main():
    inicio = time.time()
    '''----------------------------- GERA????O DA INSTANCIA -----------------------------------'''''
    Numero_de_Pontos = 100
    Coordenadas, Distancias = Gera_Instancia(Numero_de_Pontos)
    Rota_Inicial = Gera_Solucao_Inicial(Numero_de_Pontos)
    Tempo_Atendimento = Gera_Tempo_Atendimento(Numero_de_Pontos)
    Janelas = Gera_Janelas(Numero_de_Pontos, Rota_Inicial, Tempo_Atendimento, Distancias)
    Janelas = Ordena(Numero_de_Pontos, Janelas, Rota_Inicial)

    '''----------------------------- HEUR??STICA CONSTRUTIVA -----------------------------------'''''
    Rota_Final, Custo_Final, Custo_Clientes = Heuristica_Vizinho_Proximo(Numero_de_Pontos, Janelas, Distancias, Tempo_Atendimento, Rota_Inicial)
    Janelas_Atendidas = Calcula_Clientes_Atendidos(Rota_Final, Custo_Clientes, Janelas)
    min = []
    max = []
    for i in Rota_Final[:Numero_de_Pontos]:
        min.append(Janelas[i][0])
        max.append(Janelas[i][1])
    fim = time.time()
    print('Ap??s {} segundos, um total de {} clientes foram atendidos em sua janela de tempo:' .format(fim - inicio, Janelas_Atendidas))
    x = PrettyTable()
    x.add_column('Ponto', Rota_Final[:Numero_de_Pontos])
    x.add_column('Minimo', min)
    x.add_column('Maximo', max)
    x.add_column('Atendimento', Custo_Clientes)
    print(x)

    '''----------------------------- HEUR??STICA DE MELHORIA -----------------------------------'''''
    inicio = time.time()
    Rota_Inicial = Rota_Final.copy()
    Custo_Inicial = Custo_Final
    Rota_Final, Custo_Clientes, Custo_Final =  Melhoria(Rota_Inicial, Custo_Inicial, Custo_Clientes, Janelas, Distancias, Tempo_Atendimento)
    Janelas_Atendidas = Calcula_Clientes_Atendidos(Rota_Final, Custo_Clientes, Janelas)
    fim = time.time()
    print('Ap??s {} segundos, um total de {} clientes foram atendidos em sua janela de tempo:' .format(fim - inicio, Janelas_Atendidas))
    x = PrettyTable()
    x.add_column('Ponto', Rota_Final[:Numero_de_Pontos])
    x.add_column('Minimo', min)
    x.add_column('Maximo', max)
    x.add_column('Atendimento', Custo_Clientes[:Numero_de_Pontos])
    print(x)


if __name__ == "__main__":
    main()
