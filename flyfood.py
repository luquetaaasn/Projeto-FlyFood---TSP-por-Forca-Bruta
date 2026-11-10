import itertools
from datetime import datetime

entrada = """6 8
R 0 A 0 B 0 C 0
0 0 0 0 0 0 0 0
D 0 E 0 F 0 G 0
0 0 0 0 0 0 0 0
H 0 I 0 J 0 K 0
L 0 M 0 0 0 0 0"""

linhas = entrada.splitlines()

linhas_colunas = linhas[0].split()

linhas_mapa = int(linhas_colunas[0])
colunas_mapa = int(linhas_colunas[1])

mapa = []

for linha in linhas[1:]:
    mapa.append(linha.split())


coordenadas = {}

for linha in range(linhas_mapa):
    for coluna in range(colunas_mapa):

        elemento = mapa[linha][coluna]

        if elemento != "0":
            coordenadas[elemento] = (linha, coluna)


def distancia(ponto1, ponto2):

    linha1 = ponto1[0]
    coluna1 = ponto1[1]

    linha2 = ponto2[0]
    coluna2 = ponto2[1]

    return abs(linha1 - linha2) + abs(coluna1 - coluna2)

def calcular_custo(rota):

    custo = 0
    atual = "R"

    for cidade in rota:

        custo += distancia(
            coordenadas[atual],
            coordenadas[cidade]
        )

        atual = cidade

    custo += distancia(
        coordenadas[atual],
        coordenadas["R"]
    )

    return custo


cidades = []

for cidade in coordenadas:

    if cidade != "R":
        cidades.append(cidade)


menor_custo = float("inf")
melhor_rota = None

inicio = datetime.now()


for rota in itertools.permutations(cidades):

    custo = calcular_custo(rota)

    if custo < menor_custo:

        menor_custo = custo
        melhor_rota = rota


fim = datetime.now()

tempo = fim - inicio

print("Melhor rota:", " ".join(melhor_rota))
print("Menor custo:", menor_custo)
print("Tempo de busca:", tempo)