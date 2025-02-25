import random

def generate_graph(v, k):
    edges = []
    for i in range(v):
        for _ in range(k):
            target = random.randint(0, v - 1)
            if target != i:
                edges.append((i, target))
    return edges

def generate_graphs():
    vertices_options = [500, 5000, 10000]
    edges_per_vertex_options = [3, 5, 7]
    graphs = {}
    
    for v in vertices_options:
        for k in edges_per_vertex_options:
            graphs[(v, k)] = generate_graph(v, k)
            print(f"Graph with {v} vertices and {k} edges per vertex generated.")
    
    return graphs

if __name__ == "__main__":
    graphs = generate_graphs()
