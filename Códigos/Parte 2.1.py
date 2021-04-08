import math
import random
import time
import numpy
from prettytable import PrettyTable

def Gera_Instancia(n):
    Pontos = []
    for i in range(0,n):
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
    for i in range(0, n):
        t = random.randint(0, 10)
        Tempo.append(t)
    return Tempo

def Gera_Janelas(n, rota, atendimento, distancia):
    tempoChegada = [0]
    tempo = atendimento[0]
    i = 1
    while i < len(rota)-1:
        tempo += distancia[i-1][i]
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

'''
No caso da heurística, realizei uma modificação que fará com que não seja escolhido o vizinho mais próximo, mas
sim o ponto onde a média da janela de tempo seja menor, dessa maneira buscando atender sempre o próximo cliente
com o tempo "mais crítico" O código começará a partir do cliente inicial da janela de tempo, que no caso é o
primeiro cliente da rota aleatória gerada. Nem sempre a rota final está saindo com valores aceitáveis para as
janelas de tempo
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


def main():
    inicio = time.time()
    Numero_de_Pontos = 100
    Coordenadas, Distancias = Gera_Instancia(Numero_de_Pontos)
    Rota_Inicial = Gera_Solucao_Inicial(Numero_de_Pontos)
    Tempo_Atendimento = Gera_Tempo_Atendimento(Numero_de_Pontos)
    Janelas = Gera_Janelas(Numero_de_Pontos, Rota_Inicial, Tempo_Atendimento, Distancias)
    Janelas = Ordena(Numero_de_Pontos, Janelas, Rota_Inicial)
    Rota_Final, Custo_Final, Custo_Clientes = Heuristica_Vizinho_Proximo(Numero_de_Pontos, Janelas, Distancias, Tempo_Atendimento, Rota_Inicial)
    min = []
    max = []
    for i in Rota_Final[:Numero_de_Pontos]:
        min.append(Janelas[i][0])
        max.append(Janelas[i][1])
    fim = time.time()
    print('Após {} segundos, o resultado encontrado foi:' .format(fim - inicio))
    x = PrettyTable()
    x.add_column('Ponto', Rota_Final[:Numero_de_Pontos])
    x.add_column('Minimo', min)
    x.add_column('Maximo', max)
    x.add_column('Atendimento', Custo_Clientes)
    print(x)


if __name__ == "__main__":
    main()