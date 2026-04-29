from collections import defaultdict 

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
    
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Adjacency List Creation
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

#-------------------------------------------------------------------------------
print("Adjacency Lists:")
print()

for node, neighbors in list1.items():
    print(f" {node}: {neighbors}")

print()

for node, neighbors in list2.items():
    print(f" {node}: {neighbors}")
    
print()

for node, neighbors in list3.items():
    print(f" {node}: {neighbors}")

print()

for node, neighbors in list4.items():
    print(f" {node}: {neighbors}")
    
print()
print("Adjacency Matrices:")
print()

for row in matrix1:
    print(row)

print()

for row in matrix2:
    print(row)
    
print()

for row in matrix3:
    print(row)

print()

for row in matrix4:
    print(row)