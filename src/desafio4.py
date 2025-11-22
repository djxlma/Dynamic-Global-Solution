import time
import random
from decorators import performance, logger
from grafo import SkillGraph

# Tamanho da lista para o benchmark (usar um tamanho maior para resultados mais significativos)
BENCHMARK_SIZE = 1000

def merge_sort(arr, key_func):
    """Implementação do Merge Sort."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)

    return merge(left, right, key_func)

def merge(left, right, key_func):
    """Função auxiliar para o Merge Sort."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr, key_func):
    """Implementação do Quick Sort."""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    pivot_key = key_func(pivot)
    
    left = [x for x in arr if key_func(x) < pivot_key]
    middle = [x for x in arr if key_func(x) == pivot_key]
    right = [x for x in arr if key_func(x) > pivot_key]
    
    return quick_sort(left, key_func) + middle + quick_sort(right, key_func)

@performance
@logger
def desafio4_parallel_tracks(graph: SkillGraph):
    """
    Implementa o Desafio 4 - Trilhas Paralelas.
    
    Ordena as habilidades por Complexidade (C) usando Merge Sort e Quick Sort.
    Requisito 2.4: Compara os tempos medidos com o `sorted()` nativo do Python.

    Args:
        graph (SkillGraph): Instância do grafo de habilidades.

    Returns:
        dict: Dicionário com os resultados de performance e a análise.
    """
    
    all_skills = graph.get_all_skills()
    
    # Função chave para ordenar por complexidade
    key_func = lambda skill_id: graph.get_skill_data(skill_id)['complexity']
    
    # --- Benchmark de Performance (Requisito 2.4) ---
    
    # Criar uma lista de habilidades maior para um benchmark significativo
    # Usaremos uma lista de dicionários para simular dados mais complexos
    benchmark_list = []
    for i in range(BENCHMARK_SIZE):
        skill_id = f"S_{i}"
        complexity = random.randint(1, 100)
        benchmark_list.append({'id': skill_id, 'complexity': complexity})
        
    # Função chave para o benchmark
    benchmark_key_func = lambda item: item['complexity']
    
    # 1. Merge Sort
    start_time = time.time()
    merge_sorted = merge_sort(benchmark_list, benchmark_key_func)
    t_merge = time.time() - start_time
    
    # 2. Quick Sort
    start_time = time.time()
    quick_sorted = quick_sort(benchmark_list, benchmark_key_func)
    t_quick = time.time() - start_time
    
    # 3. Native Sort (Requisito 2.4)
    start_time = time.time()
    native_sorted = sorted(benchmark_list, key=benchmark_key_func)
    t_native = time.time() - start_time
    
    # --- Análise e Resultados ---
    
    # Ordenar as habilidades originais (12) para exibição
    final_sorted_skills = merge_sort(all_skills, key_func)
    
    # Determinar o algoritmo mais rápido
    times = {
        'merge_sort': t_merge,
        'quick_sort': t_quick,
        'native_sort': t_native
    }
    
    fastest_algo = min(times, key=times.get)
    
    # Justificativa da escolha
    algorithm_choice = {
        'chosen': fastest_algo,
        'reason': (
            f"O algoritmo nativo do Python (`sorted()`) foi o mais rápido ({t_native:.6f}s) "
            f"para uma lista de {BENCHMARK_SIZE} elementos, devido à sua implementação otimizada "
            f"(Timsort, que é uma combinação de Merge Sort e Insertion Sort). "
            f"Entre as implementações manuais, o {fastest_algo} foi o mais rápido. "
            "A complexidade teórica O(n log n) é a mesma para Merge Sort e Quick Sort (caso médio), "
            "mas o Quick Sort pode degradar para O(n²) no pior caso, enquanto o Merge Sort é estável em O(n log n)."
        ),
        'complexities': {
            'merge_sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n log n)'},
            'quick_sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n²)'},
            'native_sort': {'best': 'O(n)', 'average': 'O(n log n)', 'worst': 'O(n log n)'} # Timsort
        }
    }

    return {
        'sorted_skills': final_sorted_skills,
        'merge_sort': {'time': t_merge, 'correct': merge_sorted == native_sorted},
        'quick_sort': {'time': t_quick, 'correct': quick_sorted == native_sorted},
        'native_sort': {'time': t_native, 'correct': True},
        'algorithm_choice': algorithm_choice,
        'benchmark_size': BENCHMARK_SIZE
    }
