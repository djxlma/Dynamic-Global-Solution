import itertools
import math
from decorators import performance, logger, memoize
from grafo import SkillGraph

@performance
@logger
def desafio2_critical_skills_analysis(graph: SkillGraph):
    # 1. Validação do Grafo (Requisito do Desafio 2)
    validation_errors = graph.validate_graph()
    if validation_errors:
        logger.error("Validação do Grafo falhou antes de calcular custos.")
        for error in validation_errors:
            logger.error(f"  -> {error}")
        # Exigência técnica: Se houver ciclo, reportar e interromper com mensagem de erro tratada.
        if any("Ciclo detectado" in error for error in validation_errors):
            raise ValueError("Ciclo detectado no grafo de habilidades. Interrompendo Desafio 2.")
        # Para outros erros (pré-requisitos inexistentes), o código pode continuar, mas o erro deve ser reportado.
    
    critical_skills = graph.get_skills_by_usage('Crítica')
    """
    Implementa o Desafio 2 - Verificação Crítica.
    
    Enumera todas as permutações das 5 Habilidades Críticas (S3, S5, S7, S8, S9)
    e calcula o custo total (tempo acumulado) para cada ordem.
    
    Requisito 2.2: Compara as 3 melhores ordens, calcula média e desvio-padrão
    do custo, e justifica a heurística observada.

    Args:
        graph (SkillGraph): Instância do grafo de habilidades.

    Returns:
        dict: Dicionário com a melhor ordem, as 3 melhores ordens e a análise.
    """
    
    critical_skills = graph.get_skills_by_usage('Crítica')
    
    # Filtrar apenas as 5 habilidades críticas mencionadas no notebook original
    # S3, S5, S7, S8, S9
    target_skills = [s for s in critical_skills if s in ['S3', 'S5', 'S7', 'S8', 'S9']]
    
    if len(target_skills) != 5:
        logger.error(f"Esperado 5 habilidades críticas, encontrado: {target_skills}")
        return None

    @memoize
    def calculate_cost(order_tuple):
        """
        Calcula o custo total (tempo acumulado) para uma dada ordem de aquisição.
        Usa memoização para evitar recálculos.
        """
        current_time = 0
        total_cost = 0
        
        for skill_id in order_tuple:
            skill_data = graph.get_skill_data(skill_id)
            acquisition_time = skill_data['time']
            
            # O custo é o tempo acumulado até a aquisição da habilidade
            current_time += acquisition_time
            total_cost += current_time
            
        return total_cost

    # Gerar todas as permutações (5! = 120)
    all_permutations = list(itertools.permutations(target_skills))
    
    results = []
    for order in all_permutations:
        cost = calculate_cost(order)
        results.append({
            'order': list(order),
            'cost': cost
        })

    # Ordenar por custo (menor custo é o melhor)
    results.sort(key=lambda x: x['cost'])
    
    # 3 Melhores Ordens (Requisito 2.2)
    top_3_results = results[:3]
    
    # Análise estatística (Requisito 2.2)
    all_costs = [r['cost'] for r in results]
    mean_cost = sum(all_costs) / len(all_costs)
    std_dev_cost = math.sqrt(sum((c - mean_cost) ** 2 for c in all_costs) / len(all_costs))
    
    # Justificativa da Heurística (Requisito 2.2)
    # A heurística observada é que as habilidades com menor tempo de aquisição
    # devem vir primeiro para minimizar o tempo acumulado (custo).
    # Vamos verificar a ordem das 3 melhores e a ordem dos tempos.
    
    skill_times = {s: graph.get_skill_data(s)['time'] for s in target_skills}
    sorted_by_time = sorted(target_skills, key=lambda s: skill_times[s])
    
    best_order_str = ' → '.join(top_3_results[0]['order'])
    sorted_by_time_str = ' → '.join(sorted_by_time)
    
    if best_order_str == sorted_by_time_str:
        heuristic_justification = (
            "A melhor ordem segue a heurística gulosa de priorizar habilidades com o menor tempo de aquisição. "
            "Isso ocorre porque o custo total é a soma dos tempos acumulados, e colocar o menor tempo no início "
            "minimiza o impacto desse tempo nas somas subsequentes. "
            f"Ordem ideal (por tempo): {sorted_by_time_str}. "
            f"Melhor ordem encontrada: {best_order_str}."
        )
    else:
        heuristic_justification = (
            "A melhor ordem encontrada não segue estritamente a heurística gulosa de menor tempo de aquisição, "
            "indicando que a estrutura de pré-requisitos (embora não usada diretamente no cálculo de custo aqui) "
            "ou a ordem de tempo de aquisição não é o único fator. "
            "No entanto, a tendência geral é que habilidades com menor tempo de aquisição apareçam no início da sequência."
        )


    return {
        'best_order': top_3_results[0]['order'],
        'best_cost': top_3_results[0]['cost'],
        'top_3_results': top_3_results,
        'all_costs': all_costs,
        'mean_cost': mean_cost,
        'std_dev_cost': std_dev_cost,
        'heuristic_justification': heuristic_justification
    }
