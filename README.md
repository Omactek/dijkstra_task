# Shortest Path Finder

This repository implements a **tool for finding the shortest path in a graph** using **Dijkstra's algorithm**. It calculates the shortest or fastest routes within a road network represented as a graph.
It also implements other graph computional algorithms: **Bellman-Ford Algorithm** that andles graphs with negative weights and calculates shortest paths and **Kruskal's Algorithm** that finds a Minimum Spanning Tree for the graph.

## Features

1. **Graph Representation**
   - Converts GIS data (road networks and cities) into a graph.
   - Each graph node represents a point with coordinates.
   - Edges between nodes have weights based on distance and speed limits.

2. **Algorithms**
   - **Dijkstra's Algorithm** for finding the shortest path.
   - **Bellman-Ford Algorithm** for handling graphs with negative weights.
   - **Kruskal's Algorithm** for finding a Minimum Spanning Tree.

3. **Evaluation Metrics**
   - **Shortest Euclidean Distance**: Based on spatial proximity.
   - **Shortest Travel Time**: Accounts for road types and speed limits.

4. **Interactive GUI**
   - Built with **Tkinter** for user-friendly selection of cities and visualization of results.

  ## Scripts

### `main.py`
Main entry point. Loads the graph data, initializes the GUI (interface.py), and connects the interface with algorithms.

### `interface.py`
Defines the graphical user interface (GUI) for cities selection. Displays results for Dijkstra and Bellman-Ford algorithms.

### `shp_to_graph.py`
Converts GIS `.shp` files named roads.shp and towns.shp into a graph representation stored in **`graph_data.json`**, the data in json format are prepared in the repository. They represent the road network in Liberec region, Czechia. These data, downloaded from the OpenStreetMap include an attribute of the road segment (edge in the graph) lenght, its straight lenght and the maximum speed of the road. These attributes are later used as a weight components in the graph computational algorithms.

### `algorithms.py`
Contains the following classes and their functionalities:
#### `Graph`
   - **Attributes**:
     - `neighbours`: Dictionary mapping nodes to their neighbors and edge weights.
     - `coords`: Dictionary of node coordinates.
     - `cities`: Mapping of node IDs to city names.
   - **Methods**:
     - `populate_graph(graph_data)`: Initializes the graph with neighbors and coordinates.
     - `populate_cities(city_nodes)`: Maps city names to node IDs.
     - `get_neighbours(node)`: Retrieves neighbors for a given node.

#### `ShortestPath`
   - **Attributes**:
     - `graph`: An instance of the `Graph` class.
   - **Methods**:
     - `calc_weight(weights, mode)`: Calculates edge weight based on mode (basic or advanced). Basic mode counts with a simple distance (km), advanced mode takes in count the lenght and maxspeed, so it returns time in hours needed to go throught the edge.
     - `dijkstra(start, end, mode)`: Implements Dijkstra's algorithm to find the shortest path (in basic mode the shortest in lenght, im advanced mode the fastest).
     - `bellman_ford(start, mode)`: Implements Bellman-Ford algorithm for negative weights.
     - `kruskal(mode)`: Implements Kruskal's algorithm for Minimum Spanning Tree.
     - `reconstruct_path(start, end, parents)`: Reconstructs the path from parent nodes.
     - `calculate_combinations(filename, limit, mode)`: Calculates paths for each 2 cities combinations and saves results in a json format.
