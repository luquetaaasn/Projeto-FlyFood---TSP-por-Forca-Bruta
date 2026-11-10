#  Algoritmo Genético - Problema do Caixeiro Viajante (TSP)

Este repositório contém a implementação de um **Algoritmo Genético** construído em Python para resolver o clássico **Problema do Caixeiro Viajante (TSP - Traveling Salesperson Problem)**. 

O projeto foi projetado para encontrar rotas otimizadas passando por um conjunto de pontos, minimizando a distância total percorrida. Ele utiliza instâncias conhecidas ou customizadas de TSP, com destaque para a base de dados de **58 cidades do Brasil** (`brasil58`) e o problema **FlyFood**.

##  Estrutura do Projeto

Abaixo está a descrição dos principais arquivos e módulos presentes neste repositório:

* **`algoritmo_genetico.py`**: O núcleo do projeto. Contém as lógicas de evolução, incluindo criação da população inicial, cálculo de *fitness* (aptidão), seleção, cruzamento (crossover) e mutação.
* **`problemas.py`**: Definição e modelagem estrutural dos problemas que serão resolvidos pelo algoritmo.
* **`brasil58.py`**: Script principal adaptado para rodar a instância específica das 58 localidades no Brasil.
* **`experimentos.py`**: Script para rodar testes automatizados variando parâmetros do algoritmo genético (como tamanho da população, taxa de mutação, número de gerações, etc.).
* **`experimentos.csv`**: Tabela com o histórico e os resultados gerados pelas execuções do script de experimentos.
* **`edgesbrasil58.tsp` / `flyfood.tsp`**: Arquivos de dados de entrada que contêm as matrizes de distâncias ou coordenadas dos pontos a serem visitados.

##  Como Executar

### Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado na sua máquina. Você pode verificar sua versão do Python com o comando:
```bash
python --version
```

*(Opcional: Caso utilize bibliotecas externas, adicione aqui o comando de instalação, ex: `pip install -r requirements.txt`)*

### Rodando o Algoritmo

Para executar a solução para o problema das 58 cidades do Brasil, rode no seu terminal:

```bash
python brasil58.py
```

Para rodar a bateria de experimentos e gerar novos dados de saída:

```bash
python experimentos.py
```

##  Parâmetros do Algoritmo Genético

No código fonte, você poderá customizar algumas variáveis importantes para o comportamento da evolução, como:
* **Tamanho da População**
* **Taxa de Crossover (Cruzamento)**
* **Taxa de Mutação**
* **Critério de Parada (Número máximo de gerações)**

##  Resultados e Experimentos

O módulo de experimentos tem como objetivo avaliar o comportamento do algoritmo sob diferentes condições. Os resultados finais (tempo de execução, melhor distância encontrada, etc.) são salvos automaticamente no arquivo `experimentos.csv` para posterior análise comparativa.

---
**Autores:** [Adeildo José, Arthur Ricardo, Daniel Hardman e Lucas Augusto]  
Sinta-se à vontade para abrir *issues* ou enviar *pull requests* com melhorias!