import argparse
import time
import os
import math
import numpy
import random
import matplotlib.pyplot as plt
from amplpy import AMPL
from amplpy import DataFrame

def main ():
    inicio = time.time()
    args = parse_arguments()
    dat = gera_instancia(args.n)
    sol = call_ampl(dat)
    print('O resultado do AMPL foi:')
    print('Custo total de {}'.format(sol[0]))
    print('As seguintes rotas foram escolhidas: {}' .format(sol[1]))
    fim = time.time()
    print('O programa levou {} segundos' .format(fim - inicio))
    rota = numpy.copy(sol[1])
    cx = dat['cx']
    cy = dat['cy']
    for i in range(dat['n']):
        j = rota[i]
        a = i
        b = j

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

def call_ampl(dat):
    ampl = AMPL()
    ampl.read('MTZ.md')
    ampl.setOption('solver', 'cplex')

    n = ampl.getParameter('n')
    n.set(dat['n'])

    cx = ampl.getParameter('cx')
    cx.setValues(dat['cx'])

    cy = ampl.getParameter('cy')
    cy.setValues(dat['cy'])

    ampl.getOutput('solve;')

    fo = ampl.getObjective('fo').value()

    x = ampl.getVariable('x')

    rota = []
    for i in range(dat['n']):
        for j in range(dat['n']):
            if j != i:
                if x[i,j].value() > 0.9:
                    rota.append(j)
    return (fo, rota)


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
    dat = {}
    dat.update({'n': n})
    dat.update({'cx': cx})
    dat.update({'cy': cy})
    return dat

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='data file')  # Leitura da quantidade de cidades
    return parser.parse_args()

if __name__ == "__main__":
    random.seed(10)
    main()