import time as time_module
import logging
import tracemalloc
from functools import wraps
from collections import defaultdict

# Configuração do sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('moh_system.log', encoding='utf-8')
    ]
)

# Lista global para armazenar resultados de desempenho
resultados_desempenho = []

def logger(func):
    """
    Decorator para logging de execução de funções.
    Registra entrada, saída e parâmetros de cada função.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f" INICIANDO: {func.__name__}")
        if args:
            # Limitar a exibição de argumentos longos para evitar poluição do log
            arg_repr = str(args)[:100] + ('...' if len(str(args)) > 100 else '')
            logging.info(f"   Parâmetros posicionais: {arg_repr}")
        if kwargs:
            kwarg_repr = str(kwargs)[:100] + ('...' if len(str(kwargs)) > 100 else '')
            logging.info(f"   Parâmetros nomeados: {kwarg_repr}")

        try:
            result = func(*args, **kwargs)
            logging.info(f" SUCESSO: {func.__name__} concluída")
            return result
        except Exception as e:
            logging.error(f" ERRO em {func.__name__}: {str(e)}")
            raise

    return wrapper

def performance(func):
    """
    Decorator para monitoramento de performance.
    Mede tempo de execução e consumo de memória.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Iniciar monitoramento de memória
        tracemalloc.start()
        start_time = time_module.time()

        try:
            result = func(*args, **kwargs)

            # Calcular métricas de performance
            end_time = time_module.time()
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            execution_time_ms = 1000 * (end_time - start_time)
            memory_usage_kb = peak_mem / 1024

            # Armazenar resultados
            resultados_desempenho.append({
                'funcao': func.__name__,
                'tempo_ms': execution_time_ms,
                'memoria_kb': memory_usage_kb,
                'timestamp': time_module.time()
            })

            # Log de performance
            logging.info(f" PERFORMANCE - {func.__name__}: "
                         f"{execution_time_ms:.2f} ms | "
                         f"{memory_usage_kb:.2f} KB")

            print(f" {func.__name__} -> "
                  f"Tempo: {execution_time_ms:.2f} ms | "
                  f"Memória: {memory_usage_kb:.2f} KB")

            return result

        except Exception as e:
            tracemalloc.stop()
            logging.error(f" ERRO de performance em {func.__name__}: {str(e)}")
            raise

    return wrapper

def memoize(func):
    """
    Decorator para memoização (cache) de resultados.
    Otimiza funções com chamadas repetitivas.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Criar chave única baseada nos argumentos
        # Converter argumentos mutáveis (listas, dicts) para imutáveis (tuples, sorted items)
        key_args = tuple(
            tuple(sorted(arg.items())) if isinstance(arg, dict) else 
            tuple(arg) if isinstance(arg, list) else 
            arg for arg in args
        )
        key_kwargs = tuple(sorted(kwargs.items()))
        key = (key_args, key_kwargs)

        if key not in cache:
            cache[key] = func(*args, **kwargs)
            logging.debug(f" CACHE MISS: {func.__name__} - Novo resultado armazenado")
        else:
            logging.debug(f" CACHE HIT: {func.__name__} - Resultado recuperado do cache")

        return cache[key]

    # Adicionar método para limpar cache se necessário
    wrapper.clear_cache = lambda: cache.clear()

    return wrapper

def get_performance_results():
    """Retorna a lista global de resultados de desempenho."""
    return resultados_desempenho

def clear_performance_results():
    """Limpa a lista global de resultados de desempenho."""
    global resultados_desempenho
    resultados_desempenho = []
