from collections import defaultdict 
import sys
import numpy as np
import timeit
import tracemalloc

#-------------------------------------------------------------------------------
#Data Structure Methods
#-------------------------------------------------------------------------------

#Takes a list of edges and converts it into an adjacency list.
def create_adjacency_list(edges):
    
    adj_list = defaultdict(list)
        
    for u, v, w in edges:
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))
    
    return adj_list
 
#Takes a list of edges and converts it into an adjacency matrix. 
def create_adjacency_matrix(edges):
    
    nodes = sorted(list(set([node for edge in edges for node in edge[:2]])))
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    size = len(nodes)
    
    #Initialize to a very large number to represent route does not exist to Dijkstra's Alg
    matrix = [[65535] * size for _ in range(size)] 
    
    for start_node, end_node, weight in edges:
        u, v = node_to_idx[start_node], node_to_idx[end_node]
        matrix[u][v] = weight
        matrix[v][u] = weight
    
    return matrix
    
def generate_graph(num_nodes, weight_range=(1, 10)):
    
    matrix = np.random.randint(weight_range[0], weight_range[1], size = (num_nodes, num_nodes))
    
    
    matrix = (matrix + matrix.T) // 2
    np.fill_diagonal(matrix, 0)
    
    py_matrix = matrix.tolist()
    
    return py_matrix

def matrix_to_list(matrix):
    adj_list = defaultdict(list)
    
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val != 0:
                adj_list[str(i + 1)].append([str(j + 1), val])
        
    return dict(adj_list)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Dijkstra's Algorithm Implementation
#-------------------------------------------------------------------------------

#For adjacency list, data supplied as a dictionary: Nodes are the Key, contents are the edges
def dijkstra_list(adj_list, src):
    
    #Initialization
    dist = {node: sys.maxsize for node in adj_list}
    visited = set()
    
    dist[src] = 0
    
    while len(visited) < len(adj_list):
        cur_node = None
        min_dist = sys.maxsize
        
        for node in adj_list:
            if node not in visited and dist[node] < min_dist:
                min_dist = dist[node]
                cur_node = node
        
        if cur_node is None:
            break
        
        visited.add(cur_node)
        
        for neighbor, weight in adj_list[cur_node]:
            new_path_dist = dist[cur_node] + weight
            if new_path_dist < dist[neighbor]:
                dist[neighbor] = new_path_dist
        
    return dist

#For adjacency matrix, data supplied as a 2D matrix, each row-column pair being an edge.    
def dijkstra_matrix(matrix, src):
    
    V = len(matrix)
    dist = [sys.maxsize] * V
    dist[src] = 0
    visited = [False] * V
    
    for _ in range(V):
        
        u = -1
        for i in range(V):
            if not visited[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        
        if dist[u] == sys.maxsize: break
        visited[u] = True
        
        for neighbor in range(V):
            if matrix[u][neighbor] > 0 and not visited[neighbor]:
                new_dist = dist[u] + matrix[u][neighbor]
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
   
    return dist


#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Graph Creation
#-------------------------------------------------------------------------------
edges1 = [('A', 'B', 4), ('A', 'C', 2), ('B', 'D', 5), ('C', 'D', 1), ('D', 'E', 3), ('E', 'F', 2)]
list1 = create_adjacency_list(edges1)
matrix1 = create_adjacency_matrix(edges1)

edges2 = [('1', '2', 3), ('1', '3', 6), ('2', '4', 2), ('3', '5', 4), ('4', '6', 7), ('5', '7', 1), ('2', '5', 5)]
list2 = create_adjacency_list(edges2)
matrix2 = create_adjacency_matrix(edges2)

edges3 = [('A', 'B', 2), ('A', 'C', 5), ('A', 'D', 1), ('A', 'E', 4), ('B', 'C', 3), ('B', 'D', 2), ('B', 'E', 6),
          ('C', 'D', 3), ('C', 'E', 1), ('D', 'E', 2)]            
list3 = create_adjacency_list(edges3)
matrix3 = create_adjacency_matrix(edges3)

edges4 = [('1', '2', 3), ('1', '3', 2), ('1', '4', 6), ('1', '5', 5), ('1', '6', 4), ('2', '3', 1), ('2', '4', 2),
          ('2', '5', 4), ('2', '6', 7), ('3', '4', 3), ('3', '5', 6), ('3', '6', 5), ('4', '5', 2), ('4', '6', 4),
          ('5', '6', 1)]            
list4 = create_adjacency_list(edges4)
matrix4 = create_adjacency_matrix(edges4)

matrix5 = generate_graph(100)
list5 = matrix_to_list(matrix5)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Algorithm Correctness Test
#-------------------------------------------------------------------------------

print("Results for Graph 1, all nodes, List version:")
print(dijkstra_list(list1, 'A'))
print(dijkstra_list(list1, 'B'))
print(dijkstra_list(list1, 'C'))
print(dijkstra_list(list1, 'D'))
print(dijkstra_list(list1, 'E'))
print(dijkstra_list(list1, 'F'))
print()

print("Results for Graph 1, all nodes, Matrix version:")
print(dijkstra_matrix(matrix1, 0))
print(dijkstra_matrix(matrix1, 1))
print(dijkstra_matrix(matrix1, 2))
print(dijkstra_matrix(matrix1, 3))
print(dijkstra_matrix(matrix1, 4))
print(dijkstra_matrix(matrix1, 5))
print()

print("Results for Graph 2, all nodes, List version:")
print(dijkstra_list(list2, '1'))
print(dijkstra_list(list2, '2'))
print(dijkstra_list(list2, '3'))
print(dijkstra_list(list2, '4'))
print(dijkstra_list(list2, '5'))
print(dijkstra_list(list2, '6'))
print(dijkstra_list(list2, '7'))
print()

print("Results for Graph 2, all nodes, Matrix version:")
print(dijkstra_matrix(matrix2, 0))
print(dijkstra_matrix(matrix2, 1))
print(dijkstra_matrix(matrix2, 2))
print(dijkstra_matrix(matrix2, 3))
print(dijkstra_matrix(matrix2, 4))
print(dijkstra_matrix(matrix2, 5))
print(dijkstra_matrix(matrix2, 6))
print()

print("Results for Graph 3, all nodes, List version:")
print(dijkstra_list(list3, 'A'))
print(dijkstra_list(list3, 'B'))
print(dijkstra_list(list3, 'C'))
print(dijkstra_list(list3, 'D'))
print(dijkstra_list(list3, 'E'))
print()

print("Results for Graph 3, all nodes, Matrix version:")
print(dijkstra_matrix(matrix3, 0))
print(dijkstra_matrix(matrix3, 1))
print(dijkstra_matrix(matrix3, 2))
print(dijkstra_matrix(matrix3, 3))
print(dijkstra_matrix(matrix3, 4))
print()

print("Results for Graph 4, all nodes, List version:")
print(dijkstra_list(list4, '1'))
print(dijkstra_list(list4, '2'))
print(dijkstra_list(list4, '3'))
print(dijkstra_list(list4, '4'))
print(dijkstra_list(list4, '5'))
print(dijkstra_list(list4, '6'))
print()

print("Results for Graph 4, all nodes, Matrix version:")
print(dijkstra_matrix(matrix4, 0))
print(dijkstra_matrix(matrix4, 1))
print(dijkstra_matrix(matrix4, 2))
print(dijkstra_matrix(matrix4, 3))
print(dijkstra_matrix(matrix4, 4))
print(dijkstra_matrix(matrix4, 5))
print()

print("Graph 5 is randomized and used solely for time and space analysis")
print()
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Execution Time Trial
#-------------------------------------------------------------------------------
time1 = 0
time2 = 0
time3 = 0
time4 = 0
time5 = 0
time6 = 0
time7 = 0
time8 = 0
time9 = 0
time10 = 0

for i in range(5):
    time1 += timeit.timeit("dijkstra_list(list1, 'A')", globals = globals(), number = 5000)

for i in range(5):    
    time2 += timeit.timeit("dijkstra_list(list2, '1')", globals = globals(), number = 5000)
    
for i in range(5):    
    time3 += timeit.timeit("dijkstra_list(list3, 'A')", globals = globals(), number = 5000)
    
for i in range(5):    
    time4 += timeit.timeit("dijkstra_list(list4, '1')", globals = globals(), number = 5000)
    
for i in range(5):    
    time5 += timeit.timeit("dijkstra_list(list5, '1')", globals = globals(), number = 5000)

for i in range(5):    
    time6 += timeit.timeit("dijkstra_matrix(matrix1, 0)", globals = globals(), number = 5000)

for i in range(5):    
    time7 += timeit.timeit("dijkstra_matrix(matrix2, 0)", globals = globals(), number = 5000)
    
for i in range(5):    
    time8 += timeit.timeit("dijkstra_matrix(matrix3, 0)", globals = globals(), number = 5000)
    
for i in range(5):    
    time9 += timeit.timeit("dijkstra_matrix(matrix4, 0)", globals = globals(), number = 5000)
    
for i in range(5):    
    time10 += timeit.timeit("dijkstra_matrix(matrix5, 0)", globals = globals(), number = 5000)
    
print(f"Time for List 1: {time1 * 1000} ms")
print(f"Time for List 2: {time2 * 1000} ms")
print(f"Time for List 3: {time3 * 1000} ms")
print(f"Time for List 4: {time4 * 1000} ms")
print(f"Time for List 5: {time5 * 1000} ms")
print(f"Time for Matrix 1: {time6 * 1000} ms")
print(f"Time for Matrix 2: {time7 * 1000} ms")
print(f"Time for Matrix 3: {time8 * 1000} ms")
print(f"Time for Matrix 4: {time9 * 1000} ms")
print(f"Time for Matrix 5: {time10 * 1000} ms")
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Memory Usage Trial
#-------------------------------------------------------------------------------

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_list(list1, 'A')
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"List 1 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_list(list2, '1')
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"List 2 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_list(list3, 'A')
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"List 3 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_list(list4, '1')
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"List 4 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_list(list5, '1')
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"List 5 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_matrix(matrix1, 0)
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"Matrix 1 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_matrix(matrix2, 0)
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"Matrix 2 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_matrix(matrix3, 0)
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"Matrix 3 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_matrix(matrix4, 0)
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"Matrix 4 Memory Usage: {peak} bytes")
tracemalloc.stop()

tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
temp = dijkstra_matrix(matrix5, 0)
snapshot = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()
print(f"Matrix 5 Memory Usage: {peak} bytes")
tracemalloc.stop()