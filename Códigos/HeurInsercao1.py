import argparse
import time
import os
import math
import numpy
import random
import matplotlib.pyplot as plt


def main():
    inicio = time.time()
    args = parse_arguments()
    dat = gera_instancia(args.n)
    sol = heuristica(dat)
    fim = time.time()
    print('O custo total da rota é de: {}' .format(sol[1]))
    print('A rota selecionada foi: {}' .format(sol[0]))
    print('O tempo de execução foi de {} segundos' .format(fim - inicio))
    cx = dat['cx']
    cy = dat['cy']
    rota = numpy.copy(sol[0])
    for i in range(dat['n']):
        j = i + 1
        a = rota[i]
        b = rota[j]

        img = plt.axes()
        head_length = 30
        dx = cx[b] - cx[a]
        dy = cy[b] - cy[a]
        vec_ab_magnitude = math.sqrt(dx ** 2 + dy ** 2)
        dx = dx / vec_ab_magnitude
        dy = dy / vec_ab_magnitude
        vec_ab_magnitude = vec_ab_magnitude - head_length
        img.arrow(cx[a], cy[a], vec_ab_magnitude * dx, vec_ab_magnitude * dy, head_width=15, head_length=20,
                  fc='black', ec='black')
        plt.scatter(cx[a], cy[a], color='grey')
        plt.scatter(cx[b], cy[b], color='grey')
        img.annotate(a, (cx[a] + 10, cy[a] + 10), fontsize=7)

    plt.show()


'''########################################## MAIS PERTO ################################################'''
def nearest(S, C, V, n):
    while len(V) > 0:
        k, _ = min([(k, C[i][k]) for i in S for k in V], key=lambda k: k[1])
        custos = [0] * (len(S) - 1)
        for i in range(len(S) - 1):
            j = i + 1
            a = S[i]
            b = S[j]
            custos[i] = C[a][k] + C[k][b] - C[a][b]
        i, _ = min([(i, custos[i]) for i in range(len(S) - 1)], key=lambda k: k[1])
        S.insert(i + 1, k)
        V = V.difference([k])
    S.append(S[0])
    custo = 0
    for i in range(n):
        j = i+1
        a = S[i]
        b = S[j]
        custo += C[a][b]
    return S, custo


'''############################################ ARBITRARIO ##############################################'''
def arbitrary(S, C, V, n):
    while len(V) > 0:
        k = random.choice(list(V))
        custos = [0] * (len(S)-1)
        for i in range(len(S)-1):
            j = i+1
            a = S[i]
            b = S[j]
            custos[i] = C[a][k] + C[k][b] - C[a][b]
        i, _ = min([(i, custos[i]) for i in range(len(S)-1)], key=lambda k: k[1])
        S.insert(i+1, k)
        V = V.difference([k])
    S.append(S[0])
    custo = 0
    for i in range(n):
        j = i+1
        a = S[i]
        b = S[j]
        custo += C[a][b]
    return S, custo


def primeiro_no(S, C, V):
    i1 = S[-1]
    j1, c1 = min([(j, C[i1][j]) for j in V], key=lambda k: k[1])
    V = V.difference([j1])
    S.append(j1)
    return S, V



def heuristica(dat):
    modelo = int(input('Qual modelo deseja utilizar? \n(1) Arbitrary; \n(2) Nearest '))
    n = dat['n']
    C = dat['C']
    V = set(range(n))
    u = 0
    V = V.difference([u])
    S = [0]
    if modelo == 1:
        S, V, = primeiro_no(S, C, V)
        sol = arbitrary(S, C, V, n)
        return sol
    if modelo == 2:
        S, V, = primeiro_no(S, C, V)
        sol = arbitrary(S, C, V, n)
        return sol


def gerar_matriz(n):
    matriz = []
    for _ in range(n):
        matriz.append([0] * n)
    return matriz


def gera_instancia(n):
    cx = []
    cy = []
    contador = 0
    while contador < n:
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        cx.append(x)
        cy.append(y)
        contador += 1
    C = gerar_matriz(n)
    i = 0
    while i < n:
        j = 0
        while j < n:
            C[i][j] = math.sqrt((cx[i] - cx[j]) ** 2 + (cy[i] - cy[j]) ** 2)
            j += 1
        i += 1
    dat = {}
    dat.update({'n': n})
    dat.update({'cx': cx})
    dat.update({'cy': cy})
    dat.update({'C': C})
    return dat


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='data file')  # Leitura da quantidade de cidades
    return parser.parse_args()


if __name__ == "__main__":
    random.seed(10)
    main()