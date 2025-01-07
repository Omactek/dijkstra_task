from algorithms import Graph, ShortestPath
import json
from itertools import combinations

json_path = "graph_data.json"

def load_graph_and_cities_from_json(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    graph = {
        int(node_id): (
            {int(neighbor_id): weights for neighbor_id, weights in node_data["neighbors"].items()},
            node_data["coords"]
        )
        for node_id, node_data in data["graph"].items()
    }

    city_nodes = {int(node_id): city_name for node_id, city_name in data["city_nodes"].items()}

    return graph, city_nodes

def generate_city_combinations(cities):
    return list(combinations(cities, 2))

def cities_combinations_shortest_paths(graph, algorithm, city_nodes, filename):
    filtered_city_nodes = dict(list(city_nodes.items())[:4])
    city_combinations = generate_city_combinations(filtered_city_nodes.keys())

    shortest_paths = {}

    for start_id, end_id in city_combinations:
        distance, parents = algorithm.dijkstra(start_id, end_id)
        path = algorithm.reconstruct_path(start_id, end_id, parents)
        start_name = graph.get_city(start_id)
        end_name = graph.get_city(end_id)

        shortest_paths[f"({start_name}, {end_name})"] = {
            "distance": distance,
            "path": path
        }

    with open(filename, "w") as f:
        json.dump(shortest_paths, f, indent=4)

graph_data, city_nodes = load_graph_and_cities_from_json(json_path)

graph = Graph()
graph.populate_graph(graph_data)
graph.populate_cities(city_nodes)

algorithm = ShortestPath(graph)
start_node, end_node = 100000, 5345

shortest_paths_json = cities_combinations_shortest_paths(graph, algorithm, city_nodes, "combinations.json")

shortest_distance, parents = algorithm.dijkstra(start_node, end_node)
shortest_path = algorithm.reconstruct_path(start_node, end_node, parents)
print(f"Shortest Path: {shortest_path}")
print(f"Shortest Distance: {shortest_distance}")

city_combinations = generate_city_combinations(city_nodes)

bell_dist, bell_parents = algorithm.bellman_ford(start_node)
shortest_bell = algorithm.reconstruct_path(start_node, end_node, bell_parents)

print(f"Shortest Path: {bell_dist}")
print(f"Shortest Distance: {shortest_bell}")
