import csv;
import geopy.distance
import plotly.express as px
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from stations import *
from routes import *

def nx_graph_to_map(graph, stations):
    stations_dicts = [ stations.stations[station_id].to_dictionary() for station_id in graph.nodes ]
    df = pd.DataFrame(data = stations_dicts)
    fig = px.scatter_map(df, lat='lat', lon='long', hover_data=['name', 'id', 'lat', 'long'])
    fig.update_layout(mapbox_style="open-street-map")
    for fromm, to in graph.edges:
        (lat_from, long_from) = stations.get_coords_of_station(fromm)
        name_from = stations.get_name_of_station(fromm)
        (lat_to, long_to) = stations.get_coords_of_station(to)
        name_to = stations.get_name_of_station(to)
        edge = [{'lat': lat_from, 'long': long_from, 'name': name_from}, {'lat': lat_to, 'long': long_to, 'name': name_to}]
        line = px.line_map(data_frame=edge, lat='lat', lon='long')
        fig.add_trace(line.data[0])
    fig.show()

stations = Stations('../fichiers/stops.txt')
routes = Routes('../fichiers/trips.txt', '../fichiers/stop_times.txt', stations)

graph = routes.get_nx_graph(stations)

# Visualisation du graphe (lent et ne fonctionne pas sur ma machine)
#nx_graph_to_map(graph, stations)

# Question 5 : Trouver le nombre de composantes connexes, et pour chaque composante, trouver le nombre de noeuds. Trouver la plus grande composante.
# Dans le CR, pas besoin d'afficher le nombre de noeuds de chaque composantes (il y en a beaucoup) : indiquez juste comment vous avez trouvé le résultat.

# Trouver toutes les composantes connexes
composantes = list(nx.connected_components(graph))

# Nombre total de composantes connexes
nb_composantes = len(composantes)
print(f"Nombre de composantes connexes : {nb_composantes}")

# Pour chaque composante, trouver le nombre de nœuds
tailles_composantes = []
for i, composante in enumerate(composantes):
    taille = len(composante)
    tailles_composantes.append((i, taille))
    #print(f"Composante {i} : {taille} nœuds")

# Trouver la plus grande composante connexe
plus_grande_composante = max(composantes, key=len)
taille_plus_grande = len(plus_grande_composante)
print(f"Taille de la plus grande composante connexe : {taille_plus_grande} nœuds")

# Stocker la plus grande composante dans la variable 'component' pour la suite
component = plus_grande_composante

# À partir de maintenant, on ne travaille que sur la plus grande composante connexe (`nommée `component`). Gardez la ligne suivante qui vous permet de calculer ce sous-graphe (nommé `subgraph`).
subgraph = graph.subgraph(component)

# Question 6 : Trouver l'arrêt avec le plus de voisins.
# Le degré d'un nœud correspond au nombre de ses voisins
arrêt_plus_voisins = max(subgraph.nodes(), key=lambda node: subgraph.degree(node))
nb_voisins = subgraph.degree(arrêt_plus_voisins)
nom_arrêt = stations.get_name_of_station(arrêt_plus_voisins)

print(f"Arrêt le mieux desservi : {nom_arrêt} (ID: {arrêt_plus_voisins})")
print(f"Nombre de voisins : {nb_voisins}")
print(f"Localisation : {stations.get_coords_of_station(arrêt_plus_voisins)}")

# Question 7 : plus court chemin de Nancy (arrêt Vélodrome, ID 16043) vers Maron (arrêt Maron Charles de Gaulle, ID 16135).
chemin = nx.shortest_path(subgraph, source=16043, target=16135, weight='distance')
noms_arrêts = [(stations.get_name_of_station(node), node) for node in chemin]
longueur = nx.shortest_path_length(subgraph, source=16043, target=16135, weight='distance')
print(f"Chemin le plus court : {noms_arrêts}")
print(f"Longueur du chemin : {longueur} km")

# Question 9 : Cherchez, dans la documentation, une fonction qui distances
distances = dict(nx.all_pairs_dijkstra_path_length(subgraph, weight='distance'))

# Question 10 : Implémenter l'algorithme qui trouve l'arrêt qui minimise la distance par rapport aux autres.
def Trouver_Arret_Plus_Proche(distances):
    arret_optimal = None
    somme_minimale = float('inf')
    liste_arrêts = list(distances.keys())

    for arret in liste_arrêts:
        somme_distances = 0
        for autre_arret in liste_arrêts:
            if autre_arret != arret:
                somme_distances += distances[arret][autre_arret]
        if somme_distances < somme_minimale:
            somme_minimale = somme_distances
            arret_optimal = arret
    return arret_optimal

arret_optimal = Trouver_Arret_Plus_Proche(distances)
nom_arret_optimal = stations.get_name_of_station(arret_optimal)
print(f"Arrêt qui minimise la distance par rapport aux autres : {nom_arret_optimal}")
print(f"Coordonnées de l'arrêt optimal : {stations.get_coords_of_station(arret_optimal)}")