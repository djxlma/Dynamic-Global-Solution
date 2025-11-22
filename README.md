# MOH - Motor de Orientação de Habilidades (Dynamic Programming)

## Resumo do Projeto

O **Motor de Orientação de Habilidades (MOH)** é um sistema projetado para guiar profissionais na aquisição de sequências de habilidades, visando maximizar o valor de carreira e a adaptabilidade em um mercado em constante mudança. O projeto implementa algoritmos avançados de otimização e análise estocástica para lidar com incertezas e restrições complexas.

## Integrantes

Djalma Moreira de Andrade Filho - RM: 555530

Felipe Paes de Barros Muller Carioba - RM: 558447

Jose Antonio Kretzer Rodriguez - RM: 555523

## Tecnologias Utilizadas

*   **Linguagem:** Python 3.x
*   **Bibliotecas Principais:**
    *   `numpy`: Para operações numéricas e estatísticas.
    *   `matplotlib`: Para geração de gráficos e visualizações.
    *   `tabulate`: Para formatação de tabelas no relatório.
    *   Módulos nativos (`itertools`, `math`, `random`, `logging`, `tracemalloc`).
*   **Estrutura:** Código modularizado em pacotes (`src/`) para melhor organização e manutenibilidade.

## Funcionalidades Principais

O MOH resolve 5 desafios de otimização e análise:

1.  **Caminho de Valor Máximo (Desafio 1):** Encontra a sequência de habilidades que maximiza o Valor Esperado, utilizando Programação Dinâmica (implícita via busca em grafo) e Simulação Monte Carlo para modelar a incerteza.
2.  **Verificação Crítica (Desafio 2):** Analisa a ordem de aquisição de 5 habilidades críticas, utilizando busca exaustiva para encontrar a sequência de menor custo (tempo acumulado).
3.  **Pivô Mais Rápido (Desafio 3):** Compara a eficiência da seleção gulosa (razão Valor/Tempo) com a solução ótima (busca exaustiva) para atingir um nível mínimo de adaptabilidade no menor tempo.
4.  **Trilhas Paralelas (Desafio 4):** Implementa e compara algoritmos de ordenação (Merge Sort e Quick Sort) com o sort nativo do Python, medindo o desempenho em tempo.
5.  **Recomendação de Habilidades (Desafio 5):** Sugere as próximas habilidades a serem adquiridas usando Programação Dinâmica com look-ahead, considerando transições de mercado e probabilidades de cenário.

## Instruções de Uso

1.  **Estrutura de Arquivos:** Certifique-se de que a pasta `src/` e o notebook `Dynamic_globalSolution_Atualizado.ipynb` estejam no mesmo diretório.
2.  **Instalação de Dependências:** Instale as bibliotecas necessárias:
    ```bash
    pip install matplotlib numpy tabulate
    ```
3.  **Execução:**
    *   Abra o notebook `Dynamic_globalSolution_Atualizado.ipynb` em um ambiente Jupyter ou Google Colab.
    *   Execute as células sequencialmente. A primeira célula configura o ambiente e a segunda (`run_all_challenges()`) executa todos os desafios, gera os gráficos, tabelas e o relatório técnico.
4.  **Resultados:** Os resultados detalhados e as evidências experimentais (gráficos e tabelas) serão gerados na pasta raiz do projeto.
    *   `relatorio_tecnico_avancado.md`: Relatório completo (texto estruturado).
    *   `performance_tempo.png`, `benchmark_sort.png`: Gráficos.
    *   `tabela_*.md`: Tabelas de evidências.
