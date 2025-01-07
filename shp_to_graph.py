import geopandas as gpd
import numpy as np
from collections import defaultdict
import json

def loadEdgesFromShp(shp_path):
    shp = gpd.read_file(shp_path)

    Start_pts = []
    End_pts = []
    Weights = []
    for idx, row in shp.iterrows():
        line = row.geometry
        Start_pts.append((line.coords[0][0], line.coords[0][1]))
        End_pts.append((line.coords[-1][0], line.coords[-1][1]))

        lenght = row.get('lenght', 0)
        len_straight = row.get('vzd_fl', 0)
        maxspeed = row.get('maxspeed', 0)

        Weights.append([float(lenght), float(len_straight), int(maxspeed)])

    return Start_pts, End_pts, Weights

def pointsToIDs(P):
    P_ids = {}
    for i in range(len(P)):
        P_ids[(P[i][0], P[i][1])] = i
    return P_ids

def edgesToGraph(P_ids, Start_pts, End_pts, Weights):
    G = defaultdict(dict)

    for point, point_id in P_ids.items():
        G[point_id] = ({}, list(point))

    for i in range(len(Start_pts)):
        start_id = P_ids[Start_pts[i]]
        end_id = P_ids[End_pts[i]]

        G[start_id][0][end_id] = Weights[i]
        G[end_id][0][start_id] = Weights[i]

    return G # as {point_id: ({neighbour_point_id: [DISTANCE, STRAIGHT_DISTANCE, MAXSPEED], ..more neighbours}, [coordinates of point_id])

def find_city_nodes(city_shp_path, P_ids):
    city_data = gpd.read_file(city_shp_path)

    city_nodes = {}

    for idx, row in city_data.iterrows():
        city_coords = (row.geometry.x, row.geometry.y)
        city_name = row.get('name', 'Unknown')
        
        # Checks if the city coordinates match any node in the graph
        if city_coords in P_ids:
            node_id = P_ids[city_coords]
            city_nodes[node_id] = city_name

    return city_nodes


def save_to_json(graph, city_nodes, filename):
    json_graph = {
        node_id: {
            "coords": coords,
            "neighbors": {neighbor_id: weights for neighbor_id, weights in neighbors.items()}
        }
        for node_id, (neighbors, coords) in graph.items()
    }
    
    #combine graph and city nodes
    json_data = {
        "graph": json_graph,
        "city_nodes": city_nodes
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

# Load edges from shp
shp_path = r'data\roads_data.shp'
cities_shp_path = r'data\towns.shp'

Start_pts, End_pts, Weights = loadEdgesFromShp(shp_path)

# Merge lists and remove unique points
Pts_all = Start_pts + End_pts
Pts_all = np.unique(Pts_all, axis=0).tolist()
Pts_all.insert(0, [1000000, 1000000])

# Edges to graph
P_ids = pointsToIDs(Pts_all)
Graph = edgesToGraph(P_ids, Start_pts, End_pts, Weights) #result as 2: ({1: [1.3535754744, 1.35345461349, 70], 3: [0.450951656971, 0.44945385647, 70]}, [12.104227900197486, 50.23602740014445])
city_nodes = find_city_nodes(cities_shp_path, P_ids)

save_to_json(Graph, city_nodes, "graph_data.json")
print(city_nodes)