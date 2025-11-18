import csv
import networkx as nx
import geopy.distance

class Route:
    """Represents a single route. 

    A route is more or less a list of tuples (A, B), which form individual segments of the whole route. For instance, a route A -> B -> C has the following list: [(A, B), (B, C)]. Each segment is formed of the source and destination station IDs.

    Attributes
    ----------

    segments: the list of segments
    stations: a copy of the set of all stations in the network
    id: the identifier of the list
    depart: the initial station of the route
    is_finished: indicates whether the route is complete or whether some segments are missing

    """
    def __init__(self, stations, ident, depart):
        self.stations = stations
        self.segments = []
        self.id = ident
        self.depart = stations.get_parent(int(depart))
        self.is_finished = False

    def __str__(self):
        s = str(self.id) + ": " + str(self.depart)
        s_route = "".join([" -> " + str(a) for (_, a) in self.segments])
        return s + s_route

    def ajouter_arret(self, arrivee):
        """
        Adds an extra station at the (current) end of the route. This adds a new segment in the list of segments.
        """
        if len(self.segments) > 0:
            _, nouveau_depart = self.segments[-1]
            self.segments.append((nouveau_depart, self.stations.get_parent(int(arrivee))))
        else:
            self.segments.append((self.depart, self.stations.get_parent(int(arrivee))))

class Routes: 
    def __routes(trip_to_route, time_reader, stations):
        routes = {}
        for row in time_reader:
            trip_id = row['trip_id']
            route_id = int(trip_to_route[trip_id])
            if int(row['stop_sequence']) == 1:
                if not route_id in routes:
                    routes[route_id] = Route(stations, route_id, row['stop_id'])
                else:
                    routes[route_id].is_finished = True
            elif not routes[route_id].is_finished:
                routes[route_id].ajouter_arret(row['stop_id'])
        return routes

    def __get_trip_to_route(trips_reader):
        trip_to_route = {}
        for row in trips_reader:
            trip_to_route[row['trip_id']] = int(row['route_id'])
        return trip_to_route

    def __init__(self, trip_filepath, times_filepath, stations):
        with open(trip_filepath, encoding='utf-8-sig') as csvfile:
            trips_reader = csv.DictReader(csvfile)
            trip_to_route = Routes.__get_trip_to_route(trips_reader)

        with open(times_filepath, encoding='utf-8-sig') as csvfile:
            time_reader = csv.DictReader(csvfile)
            routes = Routes.__routes(trip_to_route, time_reader, stations)
            self.routes = routes

    def __str__(self):
        s = ""
        for route in self.routes.values():
            s += str(route)
        return s

    def get_nx_graph(self, stations):
        graph = nx.Graph()
        
        # Ajouter tous les arrêts comme nœuds
        for station_id in stations.stations.keys():
            graph.add_node(station_id)
        
        # Parcourir toutes les routes et leurs segments
        for route in self.routes.values():
            for (id_depart, id_arrivee) in route.segments:
                # Obtenir les coordonnées des deux arrêts
                coord_depart = stations.get_coords_of_station(id_depart)
                coord_arrivee = stations.get_coords_of_station(id_arrivee)
                
                # Calculer la distance entre les deux arrêts (en kilomètres)
                distance = geopy.distance.geodesic(coord_depart, coord_arrivee).kilometers
                
                # Ajouter l'arête avec la distance comme attribut
                graph.add_edge(id_depart, id_arrivee, distance=distance)
        
        return graph
