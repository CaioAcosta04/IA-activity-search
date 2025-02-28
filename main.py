import random
import time
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

def print_results(results, results_kn):
    def print_search_results(label, search_data):
        print(f"  {label}:")
        print(f"    - Tempo de execução: {search_data['time']:.6f} segundos")
        print(f"    - Tamanho do caminho: {search_data['length'] if search_data['length'] is not None else 'Nenhum caminho encontrado'}")
        print()
    
    print("\n========= RESULTADOS DOS GRAFOS =========\n")
    for res in results:
        print(f"Grafo com {res['vertices']} vértices e {res['arestas_por_vertice']} arestas por vértice")
        print(f"Ponto inicial: {res['start']}, Ponto final: {res['goal']}\n")
        
        print_search_results("Busca em Largura (BFS)", res['bfs'])
        print_search_results("Busca em Profundidade (DFS)", res['dfs'])
        print_search_results("Busca em Profundidade Limitada", res['depth_limited'])
        print("--------------------------------------------\n")
    
    print("========= RESULTADOS DO GRAFO COMPLETO (Kn) =========\n")
    print(f"Grafo completo com {results_kn['vertices']} vértices")
    print(f"Ponto inicial: {results_kn['start']}, Ponto final: {results_kn['goal']}\n")
    
    print_search_results("Busca em Largura (BFS)", results_kn['bfs'])
    print_search_results("Busca em Profundidade (DFS)", results_kn['dfs'])
    print_search_results("Busca em Profundidade Limitada", results_kn['depth_limited'])
    print("============================================\n")

# Função para gerar grafos com 'v' vértices e 'k' arestas mínimas por vértice.
def generate_graph(v, k):
    graph = {i: set() for i in range(v)}
    for i in range(v):
        while len(graph[i]) < k:
            j = random.randint(0, v - 1)
            if j != i:
                # Adiciona aresta de i para j (grafo não direcionado)
                graph[i].add(j)
                graph[j].add(i)
    return graph

# Busca em Largura (BFS)
def bfs(graph, start, goal):
    visited = {start}
    queue = deque([(start, [start])])
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

# Busca em Profundidade (DFS) de forma iterativa
def dfs_iterative(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        current, path = stack.pop()
        if current == goal:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in graph[current]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None

# Busca em Profundidade Limitada de forma iterativa
def depth_limited_search_iterative(graph, start, goal, limit):
    stack = [(start, [start], 0)]
    while stack:
        current, path, depth = stack.pop()
        if current == goal:
            return path
        if depth < limit:
            for neighbor in graph[current]:
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor], depth + 1))
    return None

# Parâmetros de teste
vertices_list = [500, 5000, 10000]
edges_options = [3, 5, 7]
start_vertex = 0

results = []

for v in vertices_list:
    for k in edges_options:
        print(f"Gerando grafo com {v} vértices e {k} arestas por vértice...")
        graph = generate_graph(v, k)
        goal_vertex = v - 1  # ponto final fixo
        print(f"Ponto inicial: {start_vertex}, Ponto final: {goal_vertex}")
        
        # Busca em Largura (BFS)
        start_time = time.time()
        path_bfs = bfs(graph, start_vertex, goal_vertex)
        bfs_time = time.time() - start_time
        
        # Busca em Profundidade (DFS) iterativa
        start_time = time.time()
        path_dfs = dfs_iterative(graph, start_vertex, goal_vertex)
        dfs_time = time.time() - start_time
        
        # Busca em Profundidade Limitada iterativa (definindo um limite, por exemplo, 50)
        limit = 50
        start_time = time.time()
        path_dls = depth_limited_search_iterative(graph, start_vertex, goal_vertex, limit)
        dls_time = time.time() - start_time
        
        results.append({
            'vertices': v,
            'arestas_por_vertice': k,
            'start': start_vertex,
            'goal': goal_vertex,
            'bfs': {
                'path': path_bfs,
                'time': bfs_time,
                'length': len(path_bfs) if path_bfs else None
            },
            'dfs': {
                'path': path_dfs,
                'time': dfs_time,
                'length': len(path_dfs) if path_dfs else None
            },
            'depth_limited': {
                'path': path_dls,
                'time': dls_time,
                'length': len(path_dls) if path_dls else None,
                'limit': limit
            }
        })
        print("Resultados armazenados.\n")

# Função para gerar grafo completo (Kn)
def generate_complete_graph(v):
    graph = {i: set(range(v)) - {i} for i in range(v)}
    return graph

print("Gerando grafo completo (Kn) com 10000 vértices...")
graph_kn = generate_complete_graph(10000)
goal_vertex_kn = 9999

# Aplicando as buscas no grafo completo
start_time = time.time()
path_bfs_kn = bfs(graph_kn, start_vertex, goal_vertex_kn)
bfs_time_kn = time.time() - start_time

start_time = time.time()
path_dfs_kn = dfs_iterative(graph_kn, start_vertex, goal_vertex_kn)
dfs_time_kn = time.time() - start_time

limit_kn = 50
start_time = time.time()
path_dls_kn = depth_limited_search_iterative(graph_kn, start_vertex, goal_vertex_kn, limit_kn)
dls_time_kn = time.time() - start_time

results_kn = {
    'vertices': 10000,
    'graph_type': 'complete',
    'start': start_vertex,
    'goal': goal_vertex_kn,
    'bfs': {
        'path': path_bfs_kn,
        'time': bfs_time_kn,
        'length': len(path_bfs_kn) if path_bfs_kn else None
    },
    'dfs': {
        'path': path_dfs_kn,
        'time': dfs_time_kn,
        'length': len(path_dfs_kn) if path_dfs_kn else None
    },
    'depth_limited': {
        'path': path_dls_kn,
        'time': dls_time_kn,
        'length': len(path_dls_kn) if path_dls_kn else None,
        'limit': limit_kn
    }
}

# Visualização do grafo e do caminho encontrado (exemplo)
sample_graph = generate_graph(500, 3)
sample_path = bfs(sample_graph, 0, 499)

# Chamando a função para exibir os resultados
print_results(results, results_kn)