from dijkstra import Graph, Dijkstra
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

dijkstra = Dijkstra(graph)
start_node, end_node = 126326, 66515

shortest_distance, parents = dijkstra.shortest_path(start_node, end_node)
shortest_path = dijkstra.reconstruct_path(start_node, end_node, parents)
print(f"Shortest Path: {shortest_path}")
print(f"Shortest Distance: {shortest_distance}")