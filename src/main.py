'''
Este é o script principal que orquestra a execução de todos os desafios do MOH.
'''

import os
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

from grafo import SkillGraph
from decorators import get_performance_results, clear_performance_results, logger, performance
from desafio1 import desafio1_max_value_path
from desafio2 import desafio2_critical_skills_analysis
from desafio3 import desafio3_fast_pivot
from desafio4 import desafio4_parallel_tracks
from desafio5 import desafio5_skill_recommendation, get_market_probabilities
from report_generator import generate_technical_report

# Inicializar o grafo
graph = SkillGraph()

# Importar o gerador de relatório
from report_generator import generate_technical_report

def get_visualization_data(results_d2, results_d3, results_d4):
    """
    Coleta os dados brutos necessários para gerar gráficos e tabelas no notebook.
    Não gera arquivos, apenas retorna os dicionários de dados.
    """
    viz_data = {}

    # 1. Dados para o Gráfico de Performance (Tempo vs. Função)
    performance_data = get_performance_results()
    if performance_data:
        viz_data['performance_chart'] = {
            'functions': [d['funcao'] for d in performance_data],
            'times': [d['tempo_ms'] for d in performance_data],
            'title': 'Performance do Sistema MOH - Tempo de Execução por Função'
        }

    # 2. Dados para o Gráfico de Benchmark (Desafio 4)
    if results_d4:
        viz_data['benchmark_chart'] = {
            'labels': ['Merge Sort', 'Quick Sort', 'Native Sort'],
            'times': [results_d4['merge_sort']['time'], results_d4['quick_sort']['time'], results_d4['native_sort']['time']],
            'title': f'Benchmark de Algoritmos de Ordenação (N={results_d4["benchmark_size"]})'
        }

    # 3. Dados para a Tabela das 3 Melhores Permutações (Desafio 2)
    if results_d2:
        table_data = []
        for i, res in enumerate(results_d2['top_3_results']):
            table_data.append([
                i + 1,
                ' → '.join(res['order']),
                f"{res['cost']}h"
            ])
        viz_data['top3_table'] = {
            'headers': ['Posição', 'Ordem', 'Custo Total'],
            'data': table_data,
            'analysis': f"**Análise:** O custo médio de todas as 120 permutações é de {results_d2['mean_cost']:.2f}h, com um desvio-padrão de {results_d2['std_dev_cost']:.2f}h. A melhor ordem ({' → '.join(results_d2['best_order'])}) minimiza o tempo acumulado."
        }

    # 4. Dados para a Tabela do Contraexemplo (Desafio 3)
    if results_d3:
        ce = results_d3['counterexample']
        table_data = []
        for skill in ce['skills']:
            table_data.append([
                skill['id'],
                skill['value'],
                skill['time'],
                skill['ratio']
            ])
        viz_data['counterexample_table'] = {
            'headers': ['Habilidade', 'Valor', 'Tempo (h)', 'Razão V/T'],
            'data': table_data,
            'analysis': ce
        }

    # 5. Dados para a Tabela de Probabilidades (Desafio 5)
    _, _, transition_matrix = get_market_probabilities()
    viz_data['probabilities_table'] = {
        'headers': transition_matrix[0],
        'data': transition_matrix[1:],
        'description': "As probabilidades abaixo são utilizadas no algoritmo de Programação Dinâmica com look-ahead (Desafio 5) para simular a incerteza do mercado e ajustar o valor esperado das habilidades ao longo do tempo."
    }

    return viz_data

@logger
def run_all_challenges():
    """Executa todos os desafios e retorna os resultados e dados para visualização."""
    
    # Limpar resultados de performance
    clear_performance_results()
    
    # 1. Validar o grafo
    validation_errors = graph.validate_graph()
    if validation_errors:
        print("ERRO: O grafo é inválido. Corrija os seguintes problemas:")
        for error in validation_errors:
            print(f"- {error}")
        return None
    
    # 2. Executar Desafios
    results_d1 = desafio1_max_value_path(graph)
    results_d2 = desafio2_critical_skills_analysis(graph)
    results_d3 = desafio3_fast_pivot(graph)
    results_d4 = desafio4_parallel_tracks(graph)
    results_d5_init = desafio5_skill_recommendation(graph, current_skills=[])
    
    # 3. Coletar Dados para Visualização
    visualization_data = get_visualization_data(results_d2, results_d3, results_d4)
    
    # 5. Gerar Relatório Técnico (Requisito do PDF)
    report_path = generate_technical_report(results_d1, results_d2, results_d3, results_d4, results_d5_init, visualization_data)
    
    # 4. Retornar todos os resultados para o notebook
    return {
        'd1': results_d1,
        'd2': results_d2,
        'd3': results_d3,
        'd4': results_d4,
        'd5': results_d5_init,
        'viz': visualization_data,
        'report_path': report_path
    }

if __name__ == "__main__":
    # Este bloco serve para testes e não é executado no notebook
    run_all_challenges()
