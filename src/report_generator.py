import os
from tabulate import tabulate
from decorators import logger

@logger
def generate_technical_report(d1, d2, d3, d4, d5, viz_data):
    """
    Gera o relatório técnico em formato Markdown com base nos resultados dos desafios.
    """
    report_content = []
    
    report_content.append("# Relatório Técnico - Motor de Orientação de Habilidades (MOH)")
    report_content.append("\n## I. Visão Geral e Estrutura")
    report_content.append("O Motor de Orientação de Habilidades (MOH) foi desenvolvido para aplicar Programação Dinâmica e heurísticas de otimização na aquisição de habilidades, considerando restrições de tempo, complexidade e incerteza de mercado.")
    report_content.append("\n### Estruturas de Dados")
    report_content.append("O projeto utiliza um **Grafo Direcionado Ponderado** (implementado na classe `SkillGraph` em `grafo.py`) onde os nós são as habilidades e as arestas representam os pré-requisitos. **Dicionários** são usados para armazenar os metadados das habilidades (Valor, Tempo, Complexidade). **Conjuntos** e **Listas** são empregados na detecção de ciclos e na busca de caminhos.")
    
    report_content.append("\n## II. Validação do Grafo")
    report_content.append("A validação do grafo (pré-requisito do Desafio 2) é realizada antes da execução dos desafios. Ela verifica a existência de ciclos e de pré-requisitos inexistentes, garantindo a coerência da estrutura de aquisição de habilidades.")
    
    report_content.append("\n## III. Resultados dos Desafios")
    
    # Desafio 1
    report_content.append("\n### Desafio 1 — Caminho de Valor Máximo")
    report_content.append("O objetivo foi encontrar a sequência de habilidades que maximiza o Valor Esperado sob restrições T ≤ 350h e C ≤ 30, utilizando Simulação Monte Carlo para modelar a incerteza.")
    
    if d1 and d1.get('stochastic_solution'):
        sol = d1['stochastic_solution']
        report_content.append("\n#### Solução Estocástica (Melhor Caminho)")
        report_content.append(f"- **Caminho:** `{' → '.join(sol['path'])}`")
        report_content.append(f"- **Valor Esperado (E[V]):** `{sol['expected_value']:.2f}`")
        report_content.append(f"- **Desvio Padrão (σ):** `{sol['std_deviation']:.2f}`")
        report_content.append(f"- **Tempo Total:** `{sol['time']}h`")
        report_content.append(f"- **Complexidade Total:** `{sol['complexity']}`")
        report_content.append("\n**Justificativa do Algoritmo:** O problema foi modelado como um problema de **Knapsack Multidimensional** (tempo e complexidade) resolvido por busca em grafo com poda (Programação Dinâmica implícita). A incerteza foi introduzida via **Simulação Monte Carlo** (1000 cenários) para calcular o Valor Esperado (E[V]) e o Desvio Padrão (σ).")
    else:
        report_content.append("\n*Não foi possível gerar a solução do Desafio 1.*")
        
    # Desafio 2
    report_content.append("\n### Desafio 2 — Verificação Crítica")
    report_content.append("Foram enumeradas as 120 permutações das 5 Habilidades Críticas (S3, S5, S7, S8, S9) para calcular o custo total (Tempo de Aquisição + Espera por pré-reqs).")
    
    if d2:
        report_content.append("\n#### Top 3 Melhores Ordens")
        table_data = viz_data['top3_table']['data']
        headers = viz_data['top3_table']['headers']
        report_content.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report_content.append(f"\n{viz_data['top3_table']['analysis']}")
        report_content.append(f"\n**Heurística Observada:** {d2['heuristic_justification']}")
        report_content.append("\n**Análise de Complexidade:** A busca exaustiva de permutações tem complexidade **O(n!)**, onde n=5, resultando em 120 operações. Para um número maior de habilidades críticas, essa abordagem se torna inviável.")
    else:
        report_content.append("\n*Não foi possível gerar a solução do Desafio 2.*")
        
    # Desafio 3
    report_content.append("\n### Desafio 3 — Pivô Mais Rápido")
    report_content.append("O objetivo foi alcançar adaptabilidade mínima S ≥ 15 usando habilidades básicas, comparando a seleção gulosa (V/T) com a solução ótima (busca exaustiva).")
    
    if d3:
        report_content.append("\n#### Comparação Guloso vs. Ótimo")
        table_data = [
            ["Solução Gulosa", ' → '.join(d3['greedy_solution']['skills']), f"{d3['greedy_solution']['time']}h", d3['greedy_solution']['adaptability']],
            ["Solução Ótima", ' → '.join(d3['optimal_solution']['skills']), f"{d3['optimal_solution']['time']}h", d3['optimal_solution']['adaptability']]
        ]
        headers = ["Abordagem", "Habilidades", "Tempo Total", "Adaptabilidade"]
        report_content.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        
        report_content.append("\n#### Contraprova do Guloso")
        ce = d3['counterexample']
        report_content.append(f"Um cenário artificial demonstra a falha do guloso. Objetivo: Adaptabilidade ≥ {ce['min_adaptability']}.")
        report_content.append(f"- **Guloso:** {ce['greedy_path']['explanation']} (Tempo: {ce['greedy_path']['time']}h)")
        report_content.append(f"- **Ótimo:** {ce['optimal_path']['explanation']} (Tempo: {ce['optimal_path']['time']}h)")
        report_content.append("\n**Discussão:** A heurística gulosa (V/T) é aceitável quando a diferença entre o ótimo e o guloso é pequena ou quando a complexidade da busca exaustiva **O(2^n)** é proibitiva.")
    else:
        report_content.append("\n*Não foi possível gerar a solução do Desafio 3.*")
        
    # Desafio 4
    report_content.append("\n### Desafio 4 — Trilhas Paralelas")
    report_content.append("As 12 habilidades foram ordenadas por Complexidade (C) usando implementações próprias de Merge Sort e Quick Sort, e comparadas com o sort nativo.")
    
    if d4:
        report_content.append("\n#### Ordenação Final (por Complexidade)")
        report_content.append(f"**Ordem:** `{' → '.join(d4['sorted_skills'])}`")
        report_content.append(f"\n**Sprint A (1-6):** `{' → '.join(d4['sorted_skills'][:6])}`")
        report_content.append(f"**Sprint B (7-12):** `{' → '.join(d4['sorted_skills'][6:])}`")
        
        report_content.append("\n#### Benchmark de Performance")
        table_data = [
            ["Merge Sort", f"{d4['merge_sort']['time']:.6f}s", "O(n log n)"],
            ["Quick Sort", f"{d4['quick_sort']['time']:.6f}s", "O(n log n) (médio), O(n²) (pior)"],
            ["Native Sort (Timsort)", f"{d4['native_sort']['time']:.6f}s", "O(n log n)"]
        ]
        headers = ["Algoritmo", "Tempo Medido (N=1000)", "Complexidade (Big-O)"]
        report_content.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report_content.append(f"\n**Justificativa da Escolha:** {d4['algorithm_choice']['reason']}")
    else:
        report_content.append("\n*Não foi possível gerar a solução do Desafio 4.*")
        
    # Desafio 5
    report_content.append("\n### Desafio 5 — Recomendar Próximas Habilidades")
    report_content.append("Sugestão das próximas 2-3 habilidades maximizando o valor esperado em um horizonte de 5 anos, considerando transições de mercado.")
    
    if d5:
        report_content.append("\n#### Recomendação")
        report_content.append(f"- **Habilidades Atuais:** {d5['current_skills'] if d5['current_skills'] else 'Nenhuma'}")
        report_content.append(f"- **Horizonte:** {d5['horizon_years']} anos ({d5['total_hours']}h de estudo)")
        report_content.append(f"- **Próximas 3 Habilidades:** `{' → '.join(d5['recommended_next_skills'])}`")
        report_content.append(f"- **Valor Esperado Total:** `{d5['expected_value']:.2f}`")
        
        report_content.append("\n#### Probabilidades de Mercado (Simulação)")
        table_data = viz_data['probabilities_table']['data']
        headers = viz_data['probabilities_table']['headers']
        report_content.append(tabulate(table_data, headers=headers, tablefmt="pipe"))
        report_content.append(f"\n**Sugestão Técnica:** Utilizou-se **Programação Dinâmica em Horizonte Finito** com um look-ahead limitado (profundidade 3) para ponderar o valor das habilidades sob diferentes cenários de mercado (AI Boom, Cloud Focus, Balanced), maximizando o Valor Esperado.")
    else:
        report_content.append("\n*Não foi possível gerar a solução do Desafio 5.*")
        
    # Salvar o relatório
    # Salvar no diretório raiz do projeto (um nível acima de src/)
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "relatorio_tecnico_avancado.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(report_content))
        
    # logger.info(f"Relatório técnico gerado em: {report_path}")
    return report_path
