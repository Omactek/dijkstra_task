from algorithms import Graph, ShortestPath
import json

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

graph_data, city_nodes = load_graph_and_cities_from_json(json_path)

graph = Graph()
graph.populate_graph(graph_data)
graph.populate_cities(city_nodes)
algorithm = ShortestPath(graph)

start_node, end_node = 1000, 8000
mode = "advanced" #basic (euclidean distance), advanced (time)

mst = algorithm.kruskal()
print(mst)

shortest_distance, parents = algorithm.dijkstra(start_node, end_node, mode=mode)
shortest_path = algorithm.reconstruct_path(start_node, end_node, parents)
#print(f"Shortest Path Dijkstra: {shortest_path}")
print(f"Shortest Distance Dijkstra: {shortest_distance}")

algorithm.calculate_combinations("combinations.json", limit=10, mode=mode)

bell_dists, bell_parents = algorithm.bellman_ford(start_node, mode=mode)
shortest_dist_bell = bell_dists[end_node]
shortest_bell_path = algorithm.reconstruct_path(start_node, end_node, bell_parents)

#print(f"Shortest Path Bell: {shortest_bell_path}")
print(f"Shortest Distance Bell: {shortest_dist_bell}")