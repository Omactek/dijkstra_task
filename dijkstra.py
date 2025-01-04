import heapq
import numpy as np

class Graph:
    def __init__(self):
        self.neighbours = {}
        self.coords = {}

    def populate_graph(self, graph_data): #expects {1: ({2: 8, 3: 4}, [95, 322])}
        for node, (neighbours, coords) in graph_data.items():
            self.neighbours[node] = neighbours
            self.coords[node] = coords

    def get_neighbours(self, node):
        return self.neighbours.get(node)
    
class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, end):
        num_nodes = len(self.graph.neighbours)
        parents = [-1] * (num_nodes + 1)
        dists = [np.inf] * (num_nodes + 1)

        dists[start] = 0 #init weight of starting node

        pq = []
        heapq.heapify(pq)
        heapq.heappush(pq, (dists[start], start)) #queue, (weight, node)

        while pq:
            cur_distance, cur_node = heapq.heappop(pq)

            if cur_distance > dists[cur_node]:
                continue

            for neighbour, weight in self.graph.get_neighbours(cur_node).items():
                new_dist = cur_distance + weight
                if dists[neighbour] > new_dist:
                    dists[neighbour] = new_dist
                    parents[neighbour] = cur_node
                    heapq.heappush(pq, (new_dist, neighbour))

        return dists[end], parents

    @staticmethod
    def reconstruct_path(start, end, parents):
        path = []
        cur_node = end

        while cur_node != start_node and cur_node != -1:
            path.append(cur_node)
            cur_node = parents[cur_node]

        path.append(start)
        if cur_node != start:
            print("Incorrect path")
        
        return path[::-1]
        
graph_data = {
    1: ({2: 8, 3: 4, 5: 2}, [95, 322]),
    2: ({1: 8, 3: 5, 4: 2, 7: 6, 8: 7}, [272, 331]),
    3: ({1: 4, 2: 5, 6: 3, 7: 4}, [173, 298]),
    4: ({2: 2, 9: 3}, [361, 299]),
    5: ({1: 2, 6: 5}, [82, 242]),
    6: ({3: 3, 5: 5, 7: 5, 8: 7, 9: 10}, [163, 211]),
    7: ({2: 6, 3: 4, 6: 5, 8: 3}, [244, 234]),
    8: ({2: 7, 6: 7, 7: 3, 9: 1}, [333, 225]),
    9: ({4: 3, 6: 10, 8: 1}, [412, 196])
}

graph = Graph()
graph.populate_graph(graph_data)
dijkstra = Dijkstra(graph)
start_node, end_node = 1, 9

shortest_distance, parents = dijkstra.shortest_path(start_node, end_node)
shortest_path = dijkstra.reconstruct_path(start_node, end_node, parents)
print(f"Shortest Path: {shortest_path}")
print(f"Shortest Distance: {shortest_distance}")
print(f"Parents: {parents}")