import csv
from statistics import mean, pstdev
from algoritmo_genetico import executar_ag


def comparar_configuracoes(problemas, arquivo):
    configuracoes = [
        ("base", {}),
        ("populacao_200", {"tamanho": 200}),
        ("rodadas_20000", {"rodadas": 20000}),
        ("cruzamento_70", {"taxa_cruzamento": 0.7}),
        ("mutacao_60", {"taxa_mutacao": 0.6}),
        ("pais_roleta", {"selecao_pais": "roleta"}),
        (
            "sobreviventes_torneio",
            {"selecao_sobreviventes": "torneio"}
        )
    ]

    registros = []

    for problema, distancias, quantidade in problemas:
        for nome, alteracoes in configuracoes:
            parametros = {
                "tamanho": 100,
                "rodadas": 10000,
                "taxa_cruzamento": 0.9,
                "taxa_mutacao": 0.3,
                "selecao_pais": "torneio",
                "selecao_sobreviventes": "melhores"
            }

            parametros.update(alteracoes)

            custos = []
            tempos = []

            for semente in (11, 22, 33):
                resultado = executar_ag(
                    distancias,
                    quantidade,
                    semente=semente,
                    **parametros
                )

                custos.append(resultado["custo"])
                tempos.append(resultado["tempo"])

                registro = {
                    "problema": problema,
                    "configuracao": nome,
                    "semente": semente
                }

                registro.update(parametros)

                registro["custo"] = resultado["custo"]
                registro["tempo"] = resultado["tempo"]
                registro["avaliacoes"] = resultado["avaliacoes"]
                registro["rota"] = " ".join(
                    map(str, resultado["rota"])
                )

                registros.append(registro)

            print(
                problema,
                nome,
                "| melhor:", min(custos),
                "| media:", round(mean(custos), 2),
                "| desvio:", round(pstdev(custos), 2),
                "| tempo medio:", round(mean(tempos), 4),
                flush=True
            )

    if registros:
        with open(
            arquivo, "w", newline="", encoding="utf-8-sig"
        ) as saida:
            escritor = csv.DictWriter(
                saida,
                fieldnames=list(registros[0]),
                delimiter=";"
            )

            escritor.writeheader()
            escritor.writerows(registros)

    return registros
