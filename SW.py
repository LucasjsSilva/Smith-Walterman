import numpy as np
from prettytable import PrettyTable as Pt
table = Pt()

def AdicionaU(vert, hori):
    vert, hori = 'U' + vert, 'U' + hori
    return vert, hori

def EncontraMaioreCaminhos(setas):
    maior = -1000
    caminho = []
    for tupla in setas:
        if tupla[0] >= maior:
            maior = tupla[0]
    for tupla in setas:
        if tupla[0] == maior:
            caminho.append(tupla[1])

    return maior, caminho

def GeraMatriz(vert, hori, gap, miss, match):
    tamv = len(vert)
    tamh = len(hori)
    caminhos = {}
    listav, listah = list(vert), list(hori)
    matriz = np.zeros((tamv, tamh), dtype=int)

    k = 0
    for alt in range(tamv-1, -1, -1):
        matriz[alt][0] = k * (gap)
        caminhos[(alt, 0)] = ['B']
        k += 1

    for larg in range(1, tamh):
        matriz[tamv-1][larg] = larg * (gap)
        caminhos[(tamv-1, larg)] = ['L']

    for larg in range(1, tamh):
        k = 0
        for alt in range(tamv-2, -1, -1):
            k += 1
            if listah[larg] != listav[k]:
                setas = [(matriz[alt + 1][larg] + gap, 'B'), (matriz[alt][larg - 1] + gap, 'L'), (matriz[alt+1][larg-1] + miss, 'D')]
            else:
                setas = [(matriz[alt + 1][larg] + gap, 'B'), (matriz[alt][larg - 1] + gap, 'L'), (matriz[alt+1][larg-1] + match, 'D')]

            matriz[alt][larg], caminhos[(alt, larg)] = EncontraMaioreCaminhos(setas)

    return matriz, caminhos

def BackTrace(caminhos, vert, hori):
    alinhamentos = []
    tamv = len(vert)
    tamh = len(hori)
    listav, listah = list(vert), list(hori)

    maisdeum = True
    while maisdeum:
        seq1 = ''
        seq2 = ''
        alt, larg = 0, tamh - 1
        posv, posh = tamv - 1, tamh - 1
        maisdeum = False
        while alt != tamv-1 and larg >= 0:
            if caminhos[(alt, larg)][0] == 'D':
                seq1 += listav[posv]
                seq2 += listah[posh]
                if len(caminhos[(alt, larg)]) > 1 and not maisdeum:
                    maisdeum = True
                    caminhos[(alt, larg)].pop(0)
                alt += 1
                larg -= 1
                posv -= 1
                posh -= 1
            elif caminhos[(alt, larg)][0] == 'B':
                seq1 += listav[posv]
                seq2 += '-'
                if len(caminhos[(alt, larg)]) > 1 and maisdeum == False:
                    maisdeum = True
                    caminhos[(alt, larg)].pop(0)
                alt += 1
                posv -= 1
            elif caminhos[(alt, larg)][0] == 'L':
                seq2 += listah[posh]
                seq1 += '-'
                if len(caminhos[(alt, larg)]) > 1 and maisdeum == False:
                    maisdeum = True
                    caminhos[(alt, larg)].pop(0)
                larg -= 1
                posh -= 1
        seq1, seq2 = seq1[::-1], seq2[::-1]
        alinhamentos.append((seq1, seq2))
    return alinhamentos

def MostraMatriz(matriz, vert, hori):
    tabela = Pt()
    tabela.header = False
    tabela.title = "Valores de Score Nº24"
    alt, larg = matriz.shape
    vert = vert[::-1]
    tabela.add_column(False, vert)

    for i in range(larg):
        tabela.add_column(False, matriz[:, i])

    hori = "X" + hori
    tabela.add_row(hori)
    tabela.align = "r"

    return tabela

linhas = []

with open('input.txt', 'r') as file:
    for linha in file:
        linhas.append(linha.strip().upper())

vert, hori = linhas[0], linhas[1]
vert, hori = AdicionaU(vert, hori)
gap, miss, match = int(linhas[2]), int(linhas[3]), int(linhas[4])
matriz, caminhos = GeraMatriz(vert, hori, gap, miss, match)
score = matriz[0][len(matriz[0])-1]
sequencias = BackTrace(caminhos, vert, hori)

with open('output.txt', 'w') as file:
    i = 0
    file.write(str(MostraMatriz(matriz, vert, hori))+'\n')
    for seq in sequencias:
        i += 1
        file.write("----------------------------------------------------------------\n")
        file.write(f"Alinhamento {i}\nScore = {score}|Match = {match}|Mismatch = {miss}|Gap = {gap}\n")
        file.write("----------------------------------------------------------------\n")
        file.write("Vertical: " + str(seq[0]) + '\n' + "Horizontal: " + str(seq[1]) + '\n')
