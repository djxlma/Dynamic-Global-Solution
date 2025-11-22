import math
import itertools
from decorators import performance, logger, memoize
from grafo import SkillGraph

@logger
def get_market_probabilities():
    """
    Define e documenta as probabilidades e ajustes de valor de mercado.
    (Requisito 2.5: Documentar probabilidades e simulações)
    """
    # Probabilidades de diferentes cenários de mercado
    scenarios = {
        'ai_boom': 0.3,      # Foco em IA e machine learning
        'cloud_focus': 0.4,   # Foco em cloud computing
        'balanced': 0.3       # Desenvolvimento balanceado
    }

    # Ajuste de valores por cenário (multplicadores)
    # Aumenta o valor percebido de habilidades relacionadas ao cenário
    value_adjustments = {
        'ai_boom': {
            'S4': 1.2,   # ML fundamentos
            'S6': 1.3,   # IA Generativa
            'H11': 1.1   # Big Data
        },
        'cloud_focus': {
            'S7': 1.2,   # Cloud
            'S9': 1.3,   # DevOps/CI-CD
            'S8': 1.1    # APIs
        },
        'balanced': {}    # Sem ajustes
    }
    
    # Matriz de Transição (Exemplo para documentação)
    transition_matrix = [
        ['Período', 'Prob ML↑', 'Prob Nuvem↑', 'Prob BI↑', 'Prob Azure↓'],
        ['Ano 1', '0.35', '0.25', '0.20', '0.10'],
        ['Ano 2', '0.40', '0.30', '0.15', '0.05']
    ]

    return scenarios, value_adjustments, transition_matrix

@performance
@logger
def desafio5_skill_recommendation(graph: SkillGraph, current_skills=[], horizon_years=5):
    """
    Implementa o Desafio 5 - Recomendar Próximas Habilidades.
    
    Usa Programação Dinâmica (DP) com look-ahead limitado para sugerir as 
    próximas habilidades que maximizam o valor esperado, considerando 
    incertezas de mercado.

    Args:
        graph (SkillGraph): Instância do grafo de habilidades.
        current_skills (list): Lista de habilidades já adquiridas.
        horizon_years (int): Horizonte de planejamento em anos.

    Returns:
        dict: Dicionário com recomendações e análise.
    """
    
    scenarios, value_adjustments, _ = get_market_probabilities()

    @memoize
    def finite_horizon_dp(current_state_tuple, time_horizon, max_depth=3):
        """
        Programação Dinâmica em horizonte finito com look-ahead limitado.
        Usa memoização para otimizar cálculos repetitivos.
        """
        current_state = list(current_state_tuple)

        def dp(state, time_left, depth=0):
            # Caso base: profundidade máxima atingida ou sem tempo
            if depth >= max_depth or time_left <= 0:
                return 0, []

            # Encontrar habilidades disponíveis (pré-requisitos satisfeitos)
            available_skills = []
            for skill_id in graph.skills:
                if (skill_id not in state and
                    all(p in state for p in graph.skills[skill_id]['pre_reqs'])):
                    skill_time = graph.skills[skill_id]['time']
                    if skill_time <= time_left:
                        available_skills.append(skill_id)

            if not available_skills:
                return 0, []

            best_value = -1
            best_path = []

            # Avaliar cada habilidade disponível
            for skill_id in available_skills:
                skill_data = graph.skills[skill_id]
                remaining_time = time_left - skill_data['time']

                # Calcular valor esperado considerando todos os cenários
                expected_value = 0
                for scenario, prob in scenarios.items():
                    # Aplicar ajuste de cenário se existir
                    adjustment = value_adjustments[scenario].get(skill_id, 1.0)
                    scenario_value = skill_data['value'] * adjustment

                    # Valor futuro recursivo
                    future_value, future_path = dp(state + [skill_id], remaining_time, depth + 1)
                    total_value = scenario_value + future_value
                    expected_value += prob * total_value

                # Atualizar melhor solução
                if expected_value > best_value:
                    best_value = expected_value
                    best_path = [skill_id] + future_path

            return best_value, best_path

        return dp(current_state, time_horizon)

    # Configurar parâmetros
    hours_per_week = 10
    weeks_per_year = 52
    total_hours = horizon_years * weeks_per_year * hours_per_week

    # Executar Programação Dinâmica com memoização
    expected_value, recommended_path = finite_horizon_dp(tuple(current_skills), total_hours)

    # Recomendar próximas 2-3 habilidades
    next_skills = recommended_path[:3]

    return {
        'current_skills': current_skills,
        'horizon_years': horizon_years,
        'total_hours': total_hours,
        'recommended_next_skills': next_skills,
        'full_recommended_path': recommended_path,
        'expected_value': expected_value
    }
