import geopandas as gpd
import numpy as np
from collections import defaultdict

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

# Load edges from shp
shp_path = r'D:\MGR\1_semestr\Geoinformatika\dijkstra\data\roads_data.shp'
Start_pts, End_pts, W = loadEdgesFromShp(shp_path)

# Merge lists and remove unique points
Pts_all = Start_pts + End_pts
Pts_all = np.unique(Pts_all, axis=0).tolist()
Pts_all.insert(0, [1000000, 1000000])

# Edges to graph
P_ids = pointsToIDs(Pts_all)
G = edgesToGraph(P_ids, Start_pts, End_pts, W) #result as 2: ({1: [1.3535754744, 1.35345461349, 70], 3: [0.450951656971, 0.44945385647, 70]}, [12.104227900197486, 50.23602740014445])
