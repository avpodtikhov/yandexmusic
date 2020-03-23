import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities
from tqdm import tqdm
from threading import Thread
from queue import Queue
from time import time

# G - graph, que_out - для многопоточности (функция ничего не возвращает, но добавляет в очередь que_out кортеж (index, pos))
def fruchterman_reingold(G, que_out, index):
    print('->Thread #', index, 'launched')
    t_start = time()
    pos = {}
    W = 1.
    L = 1.
    # Initialize random positions
    iterations = 50
    for v in G.nodes:
        pos[v] = np.array([W * np.random.rand(), L * np.random.rand()])
    
    temp = W / 10
    dt = temp / (iterations + 1)
    
    area = W * L
    N = G.number_of_nodes()
    k = np.sqrt(area / N)
    # print(k, N, area, temp, dt , W ,L)
    f_r = lambda x: k * k / x
    for i in tqdm(range(iterations)):
        disp = {}
        for v in G.nodes:
            disp[v] = 0. 
            for u in G.nodes:
                if u != v:
                    delta = pos[v] - pos[u]
                    dist = np.linalg.norm(delta)
                    if dist == 0:
                        dist = 0.01    
                    disp[v] = (delta / dist) * f_r(dist) + disp[v]
        f_a = lambda x: x * x / k
        for e in G.edges:
            v, u = e
            delta = pos[v] - pos[u]
            dist = np.linalg.norm(delta)
            if dist == 0:
                dist = 0.01                   
            disp[v] = disp[v] - (delta / dist) * f_a(dist)
            disp[u] = disp[u] + (delta / dist) * f_a(dist)
        for v in G.nodes:
            dist = np.linalg.norm(disp[v])
            if dist == 0:
                dist = 0.01   
            pos[v] = pos[v] + (disp[v] / dist) * min(dist, temp)
            # pos[v][0] = min(W / 2, max(-W/2., pos[v][0]))
            # pos[v][1] = min(L/2, max(-L/2., pos[v][1]))
        temp -= dt
    que_out.put((index, pos))
    print('->Thread #', index, 'finished in time', time() - t_start)

# Модернизированный алгоритм
def create_layout(G, tresh=100):
    classes = sorted(list(greedy_modularity_communities(G)), key=len)
    # print(list(map( lambda x : len(x) , classes)))
    new_classes = []
    new_classes.append(set())
    for i in range(len(classes)):
        if len(classes[i]) > tresh:
            new_classes.append(classes[i])
        else:
            new_classes[-1] = new_classes[-1] | classes[i]
    # print(list(map( lambda x : len(x) , new_classes)))
    que_out = Queue()
    threads = []
    for i in range(len(new_classes)):
        G_new = G.subgraph(new_classes[i])
        t = Thread(target=fruchterman_reingold, args=(G_new, que_out, i))
        t.start()
        threads.append(t)

    for i in range(len(threads)):
        threads[i].join()
    layouts = [0] * len(threads)
    for i in range(len(threads)):
        i, pos = que_out.get()
        layouts[i] = pos
    G1 = nx.complete_graph(len(new_classes))
    t = Thread(target=fruchterman_reingold, args=(G1, que_out, 0))
    t.start()
    t.join()
    new_pos = que_out.get()[1]
    full = {}
    for j, i in enumerate(new_pos):
        x, y = new_pos[i]
        G_n = G.subgraph(new_classes[j])
        pos = layouts[j]
        for key in pos:
            full[key] = [pos[key][0] + x * 10, pos[key][1] + y * 10]
    return full

# Стандартный алгоритм
def fruchterman_reingold_layout(G):
    que_out = Queue()
    t = Thread(target=fruchterman_reingold, args=(G, que_out, 0))
    t.start()
    t.join()
    new_pos = que_out.get()[1]
    return new_pos

G = nx.read_graphml('graph1.graphml').to_undirected()
G0 = max(nx.connected_components(G), key=len)
G = G.subgraph(G0)
full = create_layout(G, 100)
nx.draw(G, full, node_size=1)
plt.show()