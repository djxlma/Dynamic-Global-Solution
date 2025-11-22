import itertools
from decorators import performance, logger
from grafo import SkillGraph

@performance
@logger
def desafio3_fast_pivot(graph: SkillGraph, min_adaptability=15):
    """
    Implementa o Desafio 3 - Pivô Mais Rápido.
    
    Encontra o conjunto de habilidades básicas que atinge a adaptabilidade mínima
    com o menor tempo total, comparando a abordagem gulosa (razão Valor/Tempo)
    com a solução ótima (busca exaustiva).

    Requisito 2.3: Inclui a demonstração de um contraexemplo onde o guloso não é ótimo.

    Args:
        graph (SkillGraph): Instância do grafo de habilidades.
        min_adaptability (int): Nível mínimo de adaptabilidade a ser atingido.

    Returns:
        dict: Dicionário com as soluções gulosa e ótima, e a análise do contraexemplo.
    """
    
    basic_skills = graph.get_skills_by_usage('Base')
    
    @logger
    def greedy_selection(skills_list):
        """
        Abordagem gulosa: seleciona habilidades com maior razão Valor/Tempo (V/T)
        até atingir a adaptabilidade mínima.
        """
        # 1. Calcular razão V/T e ordenar em ordem decrescente
        skills_with_ratio = []
        for skill_id in skills_list:
            data = graph.get_skill_data(skill_id)
            ratio = data['value'] / data['time']
            skills_with_ratio.append((ratio, skill_id, data))
            
        skills_with_ratio.sort(key=lambda x: x[0], reverse=True)
        
        # 2. Seleção gulosa
        selected = []
        total_adaptability = 0
        total_time = 0
        
        for ratio, skill_id, skill_data in skills_with_ratio:
            if total_adaptability < min_adaptability:
                selected.append(skill_id)
                total_adaptability += skill_data['value']
                total_time += skill_data['time']
            else:
                break
        
        return selected, total_adaptability, total_time

    @performance
    def optimal_exhaustive_search(skills_list):
        """
        Busca exaustiva para encontrar a solução ótima: 
        menor tempo para atingir a adaptabilidade mínima.
        """
        best_solution = None
        best_time = float('inf')
        n = len(skills_list)

        # Gerar todos os subconjuntos possíveis (2^n)
        for i in range(1, 2**n):
            subset = []
            total_adapt = 0
            total_time = 0

            # Construir subconjunto baseado na máscara de bits
            for j in range(n):
                if i & (1 << j):
                    skill_id = skills_list[j]
                    subset.append(skill_id)
                    total_adapt += graph.skills[skill_id]['value']
                    total_time += graph.skills[skill_id]['time']

            # Verificar se atinge adaptabilidade mínima com menor tempo
            if total_adapt >= min_adaptability and total_time < best_time:
                best_solution = subset
                best_time = total_time

        if best_solution is None:
            return [], 0, 0

        return best_solution, sum(graph.skills[s]['value'] for s in best_solution), best_time

    # --- Execução das abordagens ---
    greedy_solution, greedy_adapt, greedy_time = greedy_selection(basic_skills)
    optimal_solution, optimal_adapt, optimal_time = optimal_exhaustive_search(basic_skills)

    # --- Contraexemplo Formal (Requisito 2.3) ---
    
    # Criar um cenário artificial para demonstrar a falha do guloso
    # Habilidades Artificiais:
    # H_A: Valor=8, Tempo=10 (V/T=0.8)
    # H_B: Valor=5, Tempo=5 (V/T=1.0)
    # H_C: Valor=4, Tempo=4 (V/T=1.0)
    # Adaptabilidade Mínima: 12
    
    # Guloso (ordem B, C, A):
    # 1. Seleciona B (V=5, T=5). Adapt=5.
    # 2. Seleciona C (V=4, T=4). Adapt=9.
    # 3. Seleciona A (V=8, T=10). Adapt=17. Tempo Total=19.
    
    # Ótimo (combinação A, C):
    # Combinação A + C: Valor=12. Tempo Total=14.
    
    counterexample_analysis = {
        'min_adaptability': 12,
        'skills': [
            {'id': 'H_A', 'value': 8, 'time': 10, 'ratio': 0.8},
            {'id': 'H_B', 'value': 5, 'time': 5, 'ratio': 1.0},
            {'id': 'H_C', 'value': 4, 'time': 4, 'ratio': 1.0}
        ],
        'greedy_path': {
            'order': ['H_B', 'H_C', 'H_A'],
            'adaptability': 17,
            'time': 19,
            'explanation': "O guloso prioriza H_B e H_C (maior V/T), mas precisa de H_A para atingir o mínimo, resultando em um tempo total de 19h."
        },
        'optimal_path': {
            'order': ['H_A', 'H_C'],
            'adaptability': 12,
            'time': 14,
            'explanation': "A solução ótima (H_A + H_C) atinge o mínimo de adaptabilidade (12) com o menor tempo total (14h), provando que a heurística gulosa falha neste caso."
        }
    }

    return {
        'basic_skills': basic_skills,
        'min_adaptability': min_adaptability,
        'greedy_solution': {
            'skills': greedy_solution,
            'adaptability': greedy_adapt,
            'time': greedy_time,
            'efficiency': greedy_adapt/greedy_time if greedy_time > 0 else 0
        },
        'optimal_solution': {
            'skills': optimal_solution,
            'adaptability': optimal_adapt,
            'time': optimal_time,
            'efficiency': optimal_adapt/optimal_time if optimal_time > 0 else 0
        },
        'counterexample': counterexample_analysis
    }
