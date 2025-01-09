# Shortest Path Finder

This repository implements a **tool for finding the shortest path in a graph** using **Dijkstra's algorithm**. It calculates the shortest or fastest routes within a road network represented as a graph.
It also implements other graph computional algorithms: **Bellman-Ford Algorithm** that andles graphs with negative weights and calculates shortest paths and Kruskal's Algorithm** that finds a Minimum Spanning Tree for the graph.

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
  
   - 
