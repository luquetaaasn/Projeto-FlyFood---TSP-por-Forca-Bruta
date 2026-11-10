


def carregar_distancias(arquivo, quantidade_cidades):
    with open(arquivo, "r") as entrada:
        valores = entrada.read().split()

    quantidade_esperada = quantidade_cidades * (quantidade_cidades - 1) // 2

    if len(valores) != quantidade_esperada:
        raise ValueError("Use edgesbrasil58.tsp, contendo somente os pesos.")

    distancias = {}
    posicao = 0

    for cidade1 in range(1, quantidade_cidades):
        for cidade2 in range(cidade1 + 1, quantidade_cidades + 1):
            peso = int(valores[posicao])

            distancias[(cidade1, cidade2)] = peso
            distancias[(cidade2, cidade1)] = peso

            posicao += 1

    return distancias


def converter_flyfood(entrada):
    linhas = entrada.strip().splitlines()

    altura, largura = map(int, linhas[0].split())
    mapa = [linha.split() for linha in linhas[1:]]

    if len(mapa) != altura or any(
        len(linha) != largura for linha in mapa
    ):
        raise ValueError("As dimensoes do mapa estao incorretas.")

    coordenadas = {}

    for linha in range(altura):
        for coluna in range(largura):
            nome = mapa[linha][coluna]

            if nome != "0":
                if nome in coordenadas:
                    raise ValueError("Existem nomes de pontos repetidos.")

                coordenadas[nome] = (linha, coluna)

    if "R" not in coordenadas or len(coordenadas) < 2:
        raise ValueError("O mapa precisa de R e pelo menos uma entrega.")

    nomes = ["R"]

    for nome in coordenadas:
        if nome != "R":
            nomes.append(nome)

    distancias = {}

    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            linha1, coluna1 = coordenadas[nomes[i]]
            linha2, coluna2 = coordenadas[nomes[j]]

            custo = abs(linha1 - linha2) + abs(coluna1 - coluna2)

            distancias[(i + 1, j + 1)] = custo
            distancias[(j + 1, i + 1)] = custo

    return distancias, nomes


def salvar_tsplib(arquivo, distancias, quantidade_cidades):
    with open(arquivo, "w", encoding="utf-8") as saida:
        saida.write("NAME: flyfood\n")
        saida.write("TYPE: TSP\n")
        saida.write(f"DIMENSION: {quantidade_cidades}\n")
        saida.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
        saida.write("EDGE_WEIGHT_FORMAT: UPPER_ROW\n")
        saida.write("EDGE_WEIGHT_SECTION\n")

        for i in range(1, quantidade_cidades):
            pesos = []

            for j in range(i + 1, quantidade_cidades + 1):
                pesos.append(str(distancias[(i, j)]))

            saida.write(" ".join(pesos) + "\n")

        saida.write("EOF\n")


ENTRADA_FLYFOOD = """6 8
R 0 A 0 B 0 C 0
0 0 0 0 0 0 0 0
D 0 E 0 F 0 G 0
0 0 0 0 0 0 0 0
H 0 I 0 J 0 K 0
L 0 M 0 0 0 0 0"""
