# For exiting when poping an empty heap
import sys

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




    # For graphs stored like this
#     graph = {
#       'A': {'B': 4, 'C': 2},
#       'B': {'C': 3, 'D': 2, 'E': 3},
#       'C': {'B': 1, 'D': 4, 'E': 5},
#       'D': {'E': 1},
#       'E': {}
#     }