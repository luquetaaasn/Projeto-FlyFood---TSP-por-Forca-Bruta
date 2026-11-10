from pathlib import Path
from algoritmo_genetico import executar_ag
from problemas import (
    carregar_distancias,
    converter_flyfood,
    salvar_tsplib,
    ENTRADA_FLYFOOD,
)
from experimentos import comparar_configuracoes


if __name__ == "__main__":
    arquivo = Path(__file__).with_name("edgesbrasil58.tsp")

    distancias = carregar_distancias(arquivo, 58)

    resultado = executar_ag(
        distancias,
        quantidade_cidades=58,
        tamanho=100,
        rodadas=20000,
        taxa_cruzamento=0.9,
        taxa_mutacao=0.3,
        selecao_pais="torneio",
        selecao_sobreviventes="melhores",
        semente=42
    )

    rota = resultado["rota"]
    rota_fechada = rota + [rota[0]]

    print("Melhor custo inicial:", resultado["historico"][0])
    print("Melhor rota encontrada:", rota_fechada)
    print("Custo final:", resultado["custo"])
    print("Tempo:", round(resultado["tempo"], 4), "segundos")
    print("Rotas avaliadas:", resultado["avaliacoes"])

    diferenca = 100 * (resultado["custo"] - 25395) / 25395

    print("Diferenca para 25395:", round(diferenca, 2), "%")

    distancias_flyfood, nomes = converter_flyfood(ENTRADA_FLYFOOD)
    
    arquivo_flyfood = Path(__file__).with_name("flyfood.tsp")

    salvar_tsplib(
        arquivo_flyfood,
        distancias_flyfood,
        len(nomes)
    )

    print("\nArquivo de distancias criado:", arquivo_flyfood)

    resultado_flyfood = executar_ag(
        distancias_flyfood,
        quantidade_cidades=len(nomes),
        tamanho=100,
        rodadas=20000,
        taxa_cruzamento=0.9,
        taxa_mutacao=0.3,
        selecao_pais="torneio",
        selecao_sobreviventes="melhores",
        semente=42
    )

    rota_flyfood = resultado_flyfood["rota"]

    posicao_restaurante = rota_flyfood.index(1)

    rota_flyfood = (
        rota_flyfood[posicao_restaurante:]
        + rota_flyfood[:posicao_restaurante]
    )

    rota_nomes = [nomes[cidade - 1] for cidade in rota_flyfood]
    rota_nomes.append(rota_nomes[0])

    print("\nResultado do AG no FlyFood:")
    print("Rota:", " -> ".join(rota_nomes))
    print("Custo inicial:", resultado_flyfood["historico"][0])
    print("Custo final:", resultado_flyfood["custo"])
    print(
        "Tempo:",
        round(resultado_flyfood["tempo"], 4),
        "segundos"
    )
    print("Rotas avaliadas:", resultado_flyfood["avaliacoes"])

    custo_flyfood_anterior = 26
    tempo_flyfood_anterior = "5h09min10,64s"

    print("\nComparacao com o FlyFood da 1a VA:")
    print("Custo da forca bruta anterior:", custo_flyfood_anterior)
    print("Tempo registrado na 1a VA:", tempo_flyfood_anterior)
    print("Custo do AG atual:", resultado_flyfood["custo"])
    print(
        "Tempo do AG atual:",
        round(resultado_flyfood["tempo"], 4),
        "segundos"
    )
    print(
        "Diferenca de custo:",
        resultado_flyfood["custo"] - custo_flyfood_anterior
    )

    rodar_ajustes = False

    if rodar_ajustes:
        problemas = [
            ("FlyFood", distancias_flyfood, len(nomes)),
            ("Brasil58", distancias, 58)
        ]

        arquivo_experimentos = Path(__file__).with_name(
            "experimentos.csv"
        )

        comparar_configuracoes(
            problemas,
            arquivo_experimentos
        )

        print("\nExperimentos salvos em:", arquivo_experimentos)
