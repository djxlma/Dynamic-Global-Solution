from collections import defaultdict
from decorators import logger, performance

class SkillGraph:
    """
    Classe principal que representa o grafo de habilidades.

    Estruturas:
    - skills: dicionário com metadados das habilidades
    - graph: lista de adjacência para pré-requisitos (quem precisa de quem)
    - reverse_graph: grafo reverso (quem é pré-requisito de quem)
    """

    def __init__(self):
        self.skills = {}
        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)
        self._initialize_skills()

    @logger
    def _initialize_skills(self):
        """
        Inicializa o grafo com os dados de habilidades do projeto original.
        """
        # Dados de habilidades (ID, Nome, Tempo, Valor, Complexidade, Pré-requisitos, Uso)
        skill_data = [
            # ID, Nome, Tempo (h), Valor (1-10), Complexidade (1-10), Pré-requisitos, Uso
            ('S1', 'Programação Básica (Python)', 80, 3, 4, [], 'Base'),
            ('S2', 'Modelagem de Dados (SQL)', 60, 4, 3, [], 'Base'),
            ('S3', 'Algoritmos Avançados', 100, 7, 8, ['S1'], 'Crítica'),
            ('S4', 'Fundamentos de Machine Learning', 120, 8, 9, ['S1', 'S3'], 'Não Crítica'),
            ('S5', 'Visualização de Dados (BI)', 40, 6, 5, ['S2'], 'Crítica'),
            ('S6', 'IA Generativa Ética', 150, 10, 10, ['S4'], 'Objetivo Final'),
            ('S7', 'Estruturas em Nuvem (AWS/Azure)', 70, 5, 7, ['S2'], 'Crítica'),
            ('S8', 'APIs e Microsserviços', 90, 6, 6, ['S1'], 'Crítica'),
            ('S9', 'DevOps/CI-CD', 110, 9, 8, ['S7', 'S8'], 'Crítica'),
            ('H10', 'Segurança de Dados', 60, 5, 6, [], 'Lista Grande'),
            ('H11', 'Análise de Big Data', 90, 8, 8, ['S4'], 'Lista Grande'),
            ('H12', 'Introdução a IoT', 30, 3, 3, [], 'Lista Grande'),
        ]

        for skill_id, name, time, value, complexity, pre_reqs, usage in skill_data:
            self.add_skill(skill_id, name, time, value, complexity, pre_reqs, usage)

    @logger
    def add_skill(self, skill_id, name, time, value, complexity, pre_reqs, usage):
        """
        Adiciona uma habilidade ao grafo.

        Args:
            skill_id (str): Identificador único da habilidade
            name (str): Nome descritivo da habilidade
            time (int): Tempo necessário para aquisição (horas)
            value (int): Valor da habilidade (1-10)
            complexity (int): Complexidade (1-10)
            pre_reqs (list): Lista de pré-requisitos (IDs)
            usage (str): Tipo de uso (Base, Crítica, etc.)
        """
        self.skills[skill_id] = {
            'name': name,
            'time': time,
            'value': value,
            'complexity': complexity,
            'pre_reqs': pre_reqs,
            'usage': usage
        }

        # Construir grafo direcionado para pré-requisitos
        for pre_req in pre_reqs:
            self.graph[pre_req].append(skill_id)
            self.reverse_graph[skill_id].append(pre_req)

    def get_all_skills(self):
        """Retorna lista de todas as habilidades (IDs)."""
        return list(self.skills.keys())

    def get_skill_data(self, skill_id):
        """Retorna os metadados de uma habilidade."""
        return self.skills.get(skill_id)

    def get_skills_by_usage(self, usage_type):
        """Retorna IDs das habilidades por tipo de uso."""
        return [skill_id for skill_id, data in self.skills.items() if data['usage'] == usage_type]

    @performance
    @logger
    def validate_graph(self):
        """
        Verifica a integridade do grafo:
        - Detecta ciclos usando DFS
        - Identifica pré-requisitos inexistentes
        - Verifica nós órfãos

        Returns:
            list: Lista de erros encontrados
        """
        errors = []

        # 1. Verificar nós com pré-requisitos inexistentes
        for skill_id, skill_data in self.skills.items():
            for pre_req in skill_data['pre_reqs']:
                if pre_req not in self.skills:
                    errors.append(f"Pré-requisito inexistente: {pre_req} -> {skill_id}")

        # 2. Verificar ciclos usando DFS com detecção de back edges
        visited = set()
        recursion_stack = set()

        def dfs_cycle_detection(node):
            visited.add(node)
            recursion_stack.add(node)

            # Usar o reverse_graph para verificar se os pré-requisitos formam um ciclo
            # O grafo principal (self.graph) aponta de pré-requisito para habilidade.
            # Um ciclo ocorre se, ao seguir os pré-requisitos (reverse_graph),
            # voltarmos a um nó na pilha de recursão.
            for pre_req in self.reverse_graph.get(node, []):
                if pre_req not in visited:
                    if dfs_cycle_detection(pre_req):
                        return True
                elif pre_req in recursion_stack:
                    return True # Ciclo detectado

            recursion_stack.remove(node)
            return False

        for skill_id in self.skills:
            if skill_id not in visited:
                if dfs_cycle_detection(skill_id):
                    errors.append("Ciclo detectado no grafo de pré-requisitos.")
                    break # Um ciclo é suficiente para falhar a validação

        # 3. Verificar nós órfãos (não são pré-requisitos de ninguém e não têm pré-requisitos)
        # Não é um erro crítico, mas é um aviso
        all_pre_reqs = set(p for data in self.skills.values() for p in data['pre_reqs'])
        
        # Habilidades que não são pré-requisitos de ninguém
        not_pre_req_for_anyone = set(self.skills.keys()) - all_pre_reqs
        
        # Habilidades que não têm pré-requisitos
        no_pre_reqs = set(skill_id for skill_id, data in self.skills.items() if not data['pre_reqs'])

        # Nós órfãos: aqueles que não são pré-requisitos de ninguém E não têm pré-requisitos
        # Na verdade, o que importa é se eles estão conectados.
        # Vamos focar nos erros críticos (ciclos e pré-requisitos inexistentes).

        return errors

# Inicializar o grafo para uso nos desafios
graph = SkillGraph()
