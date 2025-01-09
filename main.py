import tkinter as tk
from tkinter import ttk
from algorithms import Graph, ShortestPath
from interface import ShortestPathApp
import json

def load_graph_and_cities_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
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

json_path = "graph_data.json"
graph_data, city_nodes = load_graph_and_cities_from_json(json_path)

graph = Graph()
graph.populate_graph(graph_data)
graph.populate_cities(city_nodes)
algorithm = ShortestPath(graph)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShortestPathApp(root, algorithm)
    root.mainloop()
