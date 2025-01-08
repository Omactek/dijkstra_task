import heapq
import numpy as np
from itertools import combinations
import json

class Graph:
    def __init__(self):
        self.neighbours = {}
        self.coords = {}
        self.cities = {}

    def populate_graph(self, graph_data): #expects {1: ({2: 8, 3: 4}, [95, 322])}
        for node, (neighbours, coords) in graph_data.items():
            self.neighbours[node] = neighbours
            self.coords[node] = coords

    def get_neighbours(self, node):
        return self.neighbours.get(node)
    
    def populate_cities(self, city_nodes):
        for city_id, name in city_nodes.items():
            self.cities[city_id] = name

    def get_city(self, city_id):
        return self.cities[city_id]
    
class ShortestPath:
    def __init__(self, graph):
        self.graph = graph

    def calc_weight(self, weights, mode="basic"):
        if mode=="basic": #basic planar distance
            return weights[1]
        elif mode=="advanced": #takes into account roads and speed
            return weights[0]/weights[2]
        else:
            raise ValueError(f"Invalid mode: {mode}. Mode should be either 'basic' or 'advanced'.")

    def dijkstra(self, start, end, mode="basic"):
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

            for neighbour, weights in self.graph.get_neighbours(cur_node).items():
                weight = self.calc_weight(weights, mode)
                new_dist = cur_distance + weight
                if dists[neighbour] > new_dist:
                    dists[neighbour] = new_dist
                    parents[neighbour] = cur_node
                    heapq.heappush(pq, (new_dist, neighbour))

        return dists[end], parents
    
    def bellman_ford(self, start, mode="basic"):
        num_nodes = len(self.graph.neighbours)
        parents = [-1] * (num_nodes + 1)
        dists = [np.inf] * (num_nodes + 1)

        dists[start] = 0 #init weight of starting node

        for _ in range(num_nodes - 1): #number of relaxations
            for cur_node in range(1, num_nodes + 1):
                for neighbour, weights in self.graph.get_neighbours(cur_node).items():
                    weight = self.calc_weight(weights, mode)
                    if dists[cur_node] + weight < dists[neighbour]:
                        dists[neighbour] = dists[cur_node] + weight
                        parents[neighbour] = cur_node

        #check for negative cycle
        for cur_node in range(num_nodes + 1):
            for neighbour, weights in self.graph.get_neighbours(cur_node).items():
                weight = self.calc_weight(weights, mode)
                if dists[cur_node] + weight < dists[neighbour]:
                    raise ValueError("Negative weight cycle in graph")
                
    def kruskal(self, mode="basic"):
        edges = [] #weight, node, neighbour

        for node, neighbours in self.graph.neighbours.items():
            for neighbour, weights in neighbours.items():
                weight = self.calc_weight(weights, mode)
                if (weight, node, neighbour) not in edges:
                    edges.append((weight, node, neighbour))

        edges.sort(key=lambda x: x[0]) #sort by weight

        nodes = list(self.graph.neighbours.keys())
        disj_set = DisjointSet(nodes)

        min_span_tree = []

        for weight, node, neighbour in edges:
            root_node = disj_set.find(node)
            root_neigh = disj_set.find(neighbour)
            if root_node != root_neigh:
                min_span_tree.append(((weight, node, neighbour)))
                disj_set.union(root_node, root_neigh)

        return min_span_tree

    @staticmethod
    def reconstruct_path(start, end, parents):
        path = []
        cur_node = end

        while cur_node != start and cur_node != -1:
            path.append(cur_node)
            cur_node = parents[cur_node]

        path.append(start)
        if cur_node != start:
            print("Incorrect path")
        
        return path[::-1]
    
    def calculate_combinations(self, filename, limit=None):
        city_nodes = self.graph.cities

        if limit:   #only takes first x cities
            filtered_city_nodes = dict(list(city_nodes.items())[:limit])    
        else:
            filtered_city_nodes = city_nodes

        city_combinations = list(combinations(filtered_city_nodes.keys(), 2))
        shortest_paths = {}

        for start_id, end_id in city_combinations:
            distance, parents = self.dijkstra(start_id, end_id)
            path = self.reconstruct_path(start_id, end_id, parents)
            start_name = self.graph.get_city(start_id)
            end_name = self.graph.get_city(end_id)

            shortest_paths[f"({start_name}, {end_name})"] = {
                "distance": distance,
                "path": path
            }

        with open(filename, "w") as f:
            json.dump(shortest_paths, f, indent=4)
        
class DisjointSet:
    def __init__(self, nodes):
        self.parents = {node: node for node in nodes}
        self.ranks = {node: 0 for node in nodes}

    def find(self, node):
        if self.parents[node] != node:
            self.parents[node] = self.find(self.parents[node])
        return self.parents[node]
    
    def union(self, root1, root2):
        if self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        elif self.ranks[root1] < self.ranks[root2]:
            self.parents[root1] = root2
        else:
            self.parents[root2] = root1
            self.ranks[root1] += 1