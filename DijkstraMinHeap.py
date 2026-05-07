# For exiting when poping an empty heap
import sys
# For mesuring runtime
import time
# For creating random numbers
import numpy as np
# For keeping track of how much memory is being used
import tracemalloc

# In the priority queue the heap bubles up the new item by
def heapPush (heap, item):
    # Start by adding the item
    heap.append(item)

    # loop for bubling up the new insert
    i = len(heap) - 1
    while i > 0:
        # Find the index of the parent node // uses floor
        parent = (i - 1) // 2
        if heap[i] < heap [parent]:
            # swap the heap the the parent 
            heap[i], heap[parent] = heap[parent], heap[i]
            # Set i to the new parent so the process can check the next parent
            i = parent
        else:
            # This means that the node is in the correct position
            break

def heapPop(heap):
    if len(heap) == 0:
        print("Error: cannot pop empty heap")
        sys.exit(1)
    
    # The root node will be the smallest value
    smallest = heap[0]

    # Keep the last item in the heap stored and remove it from the list
    last = heap.pop()

    # Check if the heap still contains items
    if len(heap) != 0:
        heap[0] = last

        # i for indexing the heap
        i = 0

        while True:
            # Get the index of the left and right child
            leftIndex = (2 * i) + 1
            rightIndex = (2 * i) + 2

            # For changing and checking the index
            newIndex = i

            # Check if the indcies are in bounds and if the children are smaller than the parents
            # If the children are smaller than the parents swap the nodes (check left first)
            if leftIndex < len(heap) and heap[leftIndex] < heap[newIndex]:
                newIndex = leftIndex
            if rightIndex < len(heap) and heap[rightIndex] < heap[newIndex]:
                newIndex = rightIndex

            # If the new index equals the old index then children are larger than the parent
            # satisfying the heap property (or the heap has one node)
            if newIndex == i:
                break
            else:
                # Condition not satified continue to sift down the heap
                heap[i], heap[newIndex] = heap[newIndex], heap[i]
                i = newIndex

    return smallest

# Main dijkstra's algorithm
def dijkstra(graph, start):
    # Create a distances list with a length equal to the number of nodes in the graph
    distances = {node: float('inf') for node in graph}
    # The distance to the root/start node is zero
    distances[start] = 0

    # Instanciate an empty list for the priority queue
    priorityQueue = []
    # push the first node into the priority queue
    heapPush(priorityQueue, (0, start))


    previous = {node: None for node in graph}

    while len(priorityQueue) != 0:
        # get the values in the tuple of the priority queue
        currentDistance, currentNode = heapPop(priorityQueue)

        # If the distance is greater than an already known distance then it is
        # worse and we skip the rest of the checks
        if currentDistance > distances[currentNode]:
            continue

        # Because the graph is stored by stating the nodes neighbors
        # items will return the current nodes neighbors as tuples
        for adjacent, weight in graph[currentNode].items():

            # The distance to the adjacent node is the current distance
            # to get to the current node plus the distance to the new node
            newDistance = currentDistance + weight

            if newDistance < distances[adjacent]:
                distances[adjacent] = newDistance
                previous[adjacent] = currentNode
                heapPush(priorityQueue, (newDistance, adjacent))

    return distances, previous

# From Dijkstra.py. Copied this so we could both use the same fixed 
# seed to do the comparison on the 3rd dense algorithm
def generate_graph(num_nodes, weight_range=(1, 10), seed = 125):
    
    rng = np.random.default_rng(seed)
    
    matrix = rng.integers(weight_range[0], weight_range[1], size = (num_nodes, num_nodes))
    
    inf_mask = rng.random(size=(num_nodes, num_nodes)) < 0.05
    matrix[inf_mask] = sys.maxsize
    
    matrix = np.maximum(matrix, matrix.T)
    np.fill_diagonal(matrix, 0)
    
    py_matrix = matrix.tolist()
    
    return py_matrix

# Function to find the average runtime
def averageRuntime(graph, start):
    times = []
    for _ in range(5):
        startTime = time.perf_counter()
        dijkstra(graph, start)
        times.append(time.perf_counter() - startTime)
    # Get the average and convert it into milliseconds
    return sum(times) / len(times) * 1000

# This function is used to find out the peak amount of 
# memory used in this implementation of Dijkstra's Algorithm
def peakMemory(graph, start):
    tracemalloc.start()
    dijkstra(graph, start)
    currentMemory, peakMemory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peakMemory

# Turns an adjacency matrix into a dictionary to be used in this 
# programs Dijkstra's Algorithm
def matrixToDictionary (matrix):
    graph = {}
    # Gets each row and the contents in those rows
    for i, row in enumerate(matrix):
        # get the node number for that row
        node = str(i + 1)
        graph[node] = {}
        for j, length in enumerate(row):
            # Don't create the diagonal
            if i != j and length != sys.maxsize:
                graph[node][str(j + 1)] = length
    return graph

if __name__ == "__main__":

    # Below are the hard coded graphs. These graphs are undirected
    sparseGraph1 = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'D': 5},
        'C': {'A': 2, 'D': 1},
        'D': {'B': 5, 'C': 1, 'E': 3},
        'E': {'D': 3, 'F': 2},
        'F': {'E': 2}
    }

    sparseGraph2 = {
        '1': {'2': 3, '3': 6},
        '2': {'1': 3, '4': 2, '5': 5},
        '3': {'1': 6, '5': 4},
        '4': {'2': 2, '6': 7},
        '5': {'2': 5, '3': 4, '7': 1},
        '6': {'4': 7},
        '7': {'5': 1}
    }

    denseGraph1 = {
        'A': {'B': 2, 'C': 5, 'D': 1, 'E': 4},
        'B': {'A': 2, 'C': 3, 'D': 2, 'E': 6},
        'C': {'A': 5, 'B': 3, 'D': 3, 'E': 1},
        'D': {'A': 1, 'B': 2, 'C': 3, 'E': 2},
        'E': {'A': 4, 'B': 6, 'C': 1, 'D': 2}
    }

    denseGraph2 = {
        '1': {'2': 3, '3': 2, '4': 6, '5': 5, '6': 4},
        '2': {'1': 3, '3': 1, '4': 2, '5': 4, '6': 7},
        '3': {'1': 2, '2': 1, '4': 3, '5': 6, '6': 5},
        '4': {'1': 6, '2': 2, '3': 3, '5': 2, '6': 4},
        '5': {'1': 5, '2': 4, '3': 6, '4': 2, '6': 1},
        '6': {'1': 4, '2': 7, '3': 5, '4': 4, '5': 1}
    }

    # Create a matrix graph 
    # (the same as was done in the array implementation for comparison purposes)
    matrix = generate_graph(10)
    # Convert it so it can be used in this programs Dijkstra's Algorithm
    denseGraph3 = matrixToDictionary(matrix)


    # Run all the graphs and print the shortest lengths
    distances, previous = dijkstra(sparseGraph1, 'A')
    print("Sparse graph 1")
    print("Distances: ", distances, "\nPrevious: ", previous)

    distances, previous = dijkstra(sparseGraph2, '1')
    print("\nSparse graph 2")
    print("Distances: ", distances, "\nPrevious: ", previous)

    distances, previous = dijkstra(denseGraph1, 'A')
    print("\nDense graph 1")
    print("Distances: ", distances, "\nPrevious: ", previous)

    distances, previous = dijkstra(denseGraph2, '1')
    print("\nDense graph 2")
    print("Distances: ",  distances, "\nPrevious: ", previous)


    distances, previous = dijkstra(denseGraph3, '1')
    print("\nDense graph 3")
    print("Distances: ",  distances, "\nPrevious: ", previous)  

    # Run and print out the average runtimes
    print("\nAverage runtimes:")
    print(f"Sparse graph 1: {averageRuntime(sparseGraph1, 'A'):.6f} ms")
    print(f"Sparse graph 2: {averageRuntime(sparseGraph2, '1'):.6f} ms")
    print(f"Dense graph 1:  {averageRuntime(denseGraph1, 'A'):.6f} ms")
    print(f"Dense graph 2:  {averageRuntime(denseGraph2, '1'):.6f} ms")
    print(f"Dense graph 3:  {averageRuntime(denseGraph3, '1'):.6f} ms")

    # Run and pring out the amount of memory used
    print("\nPeak memory usage:")
    print(f"Sparse graph 1: {peakMemory(sparseGraph1, 'A')} bytes")
    print(f"Sparse graph 2: {peakMemory(sparseGraph2, '1')} bytes")
    print(f"Dense graph 1:  {peakMemory(denseGraph1, 'A')} bytes")
    print(f"Dense graph 2:  {peakMemory(denseGraph2, '1')} bytes")
    print(f"Dense graph 3:  {peakMemory(denseGraph3, '1')} bytes")