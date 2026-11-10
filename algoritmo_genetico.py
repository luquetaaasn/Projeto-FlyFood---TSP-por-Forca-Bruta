import random
from time import perf_counter
from deap import tools


def criar_populacao(tamanho, quantidade_cidades):
    populacao = []

    for i in range(tamanho):
        rota = list(range(1, quantidade_cidades + 1))
        random.shuffle(rota)
        populacao.append(rota)

    return populacao


def calcular_custo(rota, distancias):
    custo = 0

    for i in range(len(rota) - 1):
        cidade1 = rota[i]
        cidade2 = rota[i + 1]

        custo += distancias[(cidade1, cidade2)]
    custo += distancias[(rota[-1], rota[0])]

    return custo


def calcular_aptidao(populacao, distancias):
    aptidoes = []

    for rota in populacao:
        custo = calcular_custo(rota, distancias)
        aptidoes.append(custo)

    return aptidoes


def cruzamento_ox(pai1, pai2):
    filho1 = []
    filho2 = []

    for cidade in pai1:
        filho1.append(cidade - 1)

    for cidade in pai2:
        filho2.append(cidade - 1)

    tools.cxOrdered(filho1, filho2)

    for i in range(len(filho1)):
        filho1[i] +=1
        filho2 [i] += 1

    return filho1, filho2


def mutacao_inversao(rota):
    nova_rota = rota.copy()

    inicio, fim = sorted(random.sample(range(len(rota)), 2))

    trecho = nova_rota[inicio:fim + 1]
    trecho.reverse()

    nova_rota[inicio:fim + 1] = trecho

    return nova_rota


def selecionar_pai(populacao, custos, metodo):
    if metodo == "torneio":
        a, b = random.sample(range(len(populacao)), 2)

        vencedor = a if custos[a] <= custos [b] else b

    elif metodo == "roleta":
        pesos = [1 / (1 + custo) for custo in custos]

        vencedor = random.choices(
            range(len(populacao)),
            weights=pesos,
            k=1
        )[0]

    else:
        raise ValueError("Seleção de pais inválida.")

    return populacao[vencedor].copy()


def selecionar_sobreviventes(
        populacao, custos, filhos, custos_filhos, metodo
):
    tamanho = len(populacao)

    candidatos = populacao + filhos
    valores = custos + custos_filhos

    if metodo == "melhores":
        classificados = sorted(zip(valores, candidatos))
        sobreviventes = classificados [:tamanho]

        novas_rotas = [rota for custo, rota in sobreviventes]
        novos_custos = [custo for custo, rota in sobreviventes]

        return novas_rotas, novos_custos

    if metodo != "torneio":
        raise ValueError("Seleção de sobreviventes inválida.")

    posicao = valores.index(min(valores))

    elite = candidatos.pop(posicao)
    custo_elite = valores.pop(posicao)

    while len(candidatos) > tamanho - 1:
        a, b = random.sample(range(len(candidatos)), 2)

        perdedor = a if valores[a] >= valores[b] else b

        candidatos.pop(perdedor)
        valores.pop(perdedor)

    return [elite] + candidatos, [custo_elite] + valores


def executar_ag(
        distancias,
        quantidade_cidades,
        tamanho=100,
        rodadas=10000,
        taxa_cruzamento=0.9,
        taxa_mutacao=0.3,
        selecao_pais="torneio",
        selecao_sobreviventes="melhores",
        semente=42
):
    if tamanho < 2 or quantidade_cidades < 2 or rodadas < 0:
        raise ValueError(
            "Populacao e cidades devem ser >= 2; rodadas deve ser >= 0."
        )

    if not 0 <= taxa_cruzamento <= 1:
        raise ValueError("A taxa de cruzamento deve ficar entre 0 e 1.")

    if not 0 <= taxa_mutacao <= 1:
        raise ValueError("A taxa de mutacao deve ficar entre 0 e 1.")

    if selecao_pais not in ("torneio", "roleta"):
        raise ValueError("Selecao de pais invalida.")

    if selecao_sobreviventes not in ("melhores", "torneio"):
        raise ValueError("Selecao de sobreviventes invalida.")

    random.seed(semente)
    inicio = perf_counter()

    populacao = criar_populacao(tamanho, quantidade_cidades)
    custos = calcular_aptidao(populacao, distancias)

    historico = [min(custos)]

    for geracao in range(rodadas):
        pai1 = selecionar_pai(populacao, custos, selecao_pais)
        pai2 = selecionar_pai(populacao, custos, selecao_pais)   

        if random.random() < taxa_cruzamento:
            filho1, filho2 = cruzamento_ox(pai1, pai2)
        else:
            filho1 = pai1.copy()
            filho2 = pai2.copy()

        if random.random() < taxa_mutacao:
            filho1 = mutacao_inversao(filho1)

        if random.random() < taxa_mutacao:
            filho2 = mutacao_inversao(filho2)

        filhos = [filho1, filho2]
        custos_filhos = calcular_aptidao(filhos, distancias)

        populacao, custos = selecionar_sobreviventes(
            populacao,
            custos,
            filhos,
            custos_filhos,
            selecao_sobreviventes
        )

        historico.append(min(custos))

    posicao = custos.index(min(custos))

    return {
        "rota": populacao[posicao].copy(),
        "custo": custos[posicao],
        "tempo": perf_counter() - inicio,
        "avaliacoes": tamanho + 2 * rodadas,
        "historico": historico
    }
