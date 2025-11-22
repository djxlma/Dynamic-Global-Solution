import math
import random
import itertools
from decorators import performance, logger, memoize
from grafo import SkillGraph

@performance
@logger
def desafio1_max_value_path(graph: SkillGraph, target_skill='S6', max_time=350, max_complexity=30, num_scenarios=1000):
    """
    Calcula o caminho de maior valor esperado até a habilidade alvo (S6) usando 
    Programação Dinâmica (implícita via busca em grafo) e Simulação Monte Carlo.

    Otimiza a aquisição de habilidades considerando restrições de tempo e complexidade,
    e incerteza no valor das habilidades via Monte Carlo.

    Args:
        graph (SkillGraph): Instância do grafo de habilidades.
        target_skill (str): Habilidade objetivo (padrão 'S6').
        max_time (int): Restrição máxima de tempo em horas (padrão 350h).
        max_complexity (int): Restrição máxima de complexidade (padrão 30).
        num_scenarios (int): Número de cenários para simulação Monte Carlo (padrão 1000).

    Returns:
        dict: Dicionário com soluções determinística e estocástica, incluindo 
              o desvio-padrão da simulação Monte Carlo.
    """

    @memoize
    def monte_carlo_simulation(selected_skills_tuple):
        """
        Simulação Monte Carlo para incerteza nos valores das habilidades.
        Usa memoização para evitar recálculos desnecessários.
        Retorna o valor esperado e o desvio-padrão.
        """
        selected_skills = list(selected_skills_tuple)
        values = []
        for _ in range(num_scenarios):
            total_value = 0
            for skill_id in selected_skills:
                original_value = graph.get_skill_data(skill_id)['value']
                # Aplicar incerteza: V ~ Uniforme[V-10%, V+10%]
                perturbed_value = original_value * random.uniform(0.9, 1.1)
                total_value += perturbed_value
            values.append(total_value)

        # Cálculo do Valor Esperado
        expected_value = sum(values) / len(values)
        
        # Cálculo do Desvio Padrão (Requisito 2.1)
        std_dev = math.sqrt(sum((x - expected_value) ** 2 for x in values) / len(values))
        
        return expected_value, std_dev

    @logger
    def find_feasible_paths(current, path, visited, time_used, complexity_used, all_paths):
        """
        Busca em profundidade (DFS) para encontrar todos os caminhos viáveis 
        que terminam na habilidade alvo, respeitando as restrições.
        """
        # Se o caminho atual é um caminho completo para o alvo
        if current == target_skill:
            all_paths.append(path.copy())
            return

        visited.add(current)

        # Explorar vizinhos (próximas habilidades)
        # O grafo (self.graph) aponta de pré-requisito para a habilidade que o requer
        for neighbor in graph.graph.get(current, []):
            if neighbor not in visited:
                skill_data = graph.get_skill_data(neighbor)
                new_time = time_used + skill_data['time']
                new_complexity = complexity_used + skill_data['complexity']

                # Verificar restrições
                if new_time <= max_time and new_complexity <= max_complexity:
                    path.append(neighbor)
                    find_feasible_paths(neighbor, path, visited, new_time, new_complexity, all_paths)
                    path.pop()  # Backtrack

        visited.remove(current)

    # Encontrar todos os caminhos para S6 partindo de habilidades sem pré-requisitos
    all_paths_to_target = []

    # Pontos de partida: habilidades sem pré-requisitos
    starting_points = [skill_id for skill_id in graph.skills if not graph.skills[skill_id]['pre_reqs']]

    for start in starting_points:
        visited = set()
        path = [start]
        skill_data = graph.get_skill_data(start)
        time_used = skill_data['time']
        complexity_used = skill_data['complexity']

        if start != target_skill:
            find_feasible_paths(start, path, visited, time_used, complexity_used, all_paths_to_target)
        else:
            all_paths_to_target.append(path)

    # Calcular valores para cada caminho (solução determinística)
    path_values = []
    for path in all_paths_to_target:
        if target_skill in path:
            total_value = sum(graph.skills[skill_id]['value'] for skill_id in path)
            total_time = sum(graph.skills[skill_id]['time'] for skill_id in path)
            total_complexity = sum(graph.skills[skill_id]['complexity'] for skill_id in path)
            
            # Executar Monte Carlo para obter valor esperado e desvio-padrão
            expected_value, std_dev = monte_carlo_simulation(tuple(path))
            
            path_values.append((path, total_value, total_time, total_complexity, expected_value, std_dev))

    if not path_values:
        return None

    # Ordenar por valor esperado (solução estocástica)
    path_values.sort(key=lambda x: x[4], reverse=True) # x[4] é o expected_value

    # Melhor caminho estocástico
    best_stochastic_path, best_value, best_time, best_complexity, best_expected_value, best_std_dev = path_values[0]

    return {
        'stochastic_solution': {
            'path': best_stochastic_path,
            'value': best_value,
            'time': best_time,
            'complexity': best_complexity,
            'expected_value': best_expected_value,
            'std_deviation': best_std_dev
        },
        'all_feasible_paths': path_values
    }
