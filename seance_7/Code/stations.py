import csv

class Station():
    """Represents a single station. A station has a name, an identifier, a latitude and a longitude. """

    def __init__(self, name, ident: int, lat: float, long: float):
        self.name = name
        self.id = ident
        self.lat = lat
        self.long = long

    def to_dictionary(self):
        d = {}
        d['name'] = self.name
        d['id'] = self.id
        d['lat'] = self.lat
        d['long'] = self.long
        return d

class Stations():
    """Represents a set of stations.

    This is merely a wrapper over a dictionary from station IDs to `Station`s.

    Attributes
    ----------

    stations: dictionary from int (station ID) to Station.
    parents: a dictionary that contains the identifier of the parent station for all station IDs.
    """
    def __init__(self, filename):
        def station_from_row(row):
            return Station(row['stop_name'], int(row['stop_id']), float(row['stop_lat']), float(row['stop_lon']))

        def get_stations_parents(reader):
            parent_of = {}
            for row in reader:
                if row['parent_station'] == '':
                    parent_of[int(row['stop_id'])] = int(row['stop_id'])
                else:
                    parent_of[int(row['stop_id'])] = int(row['parent_station'])
            return parent_of

        def check_parent_nested(parents_list):
            for (k, v) in parents_list.items():
                if parents_list[v] != v:
                    print("Parent of "+k+" is "+v+" but parent of "+v+" is "+parents_list[v])
                    return False
            return True

        with open(filename, encoding='utf-8-sig') as csvfile:
            stations_reader = list(csv.DictReader(csvfile))
            self.parents = get_stations_parents(stations_reader)
            self.stations = {}
            if check_parent_nested(self.parents):
                for row in stations_reader:
                    station_id = int(row['stop_id'])
                    if self.__is_parent(station_id):
                        if not station_id in self.stations:
                            self.stations[station_id] = station_from_row(row)

    def __str__(self):
        return "\n".join([station.name + " (" + str(station.lat) + ", " + str(station.long) + ")" for station in self.stations.values()])

    def __is_parent(self, station):
        """Returns True is `station` is a parent station, False otherwise

        Parameters
        ----------

        station: the station identifier to test
        """
        return self.parents[station] == station

    def get_name_of_station(self, station_id):
        """Returns the name of a given station ID

        Parameters
        ----------

        station_id: the station identifier
        """
        return self.stations[self.parents[int(station_id)]].name

    def get_coords_of_station(self, station_id):
        """Returns the coordinates of a given station ID. 

        Coordinates are tuples composed of a latitude and a longitude.

        Parameters
        ----------

        station_id: the station identifier
        """
        parent = self.parents[station_id]
        return (self.stations[parent].lat, self.stations[parent].long)

    def get_all_coords(self):
        """Returns the coordinates all station IDs.

        The returned value is a dictionnary, indexed by station IDs. Coordinates are tuples composed of a latitude and a longitude.

        Parameters
        ----------

        station_id: the station identifier
        """
        coords = {}
        for station in self.stations:
            coords[station] = self.get_coords_of_station(station)

    def get_parent(self, station_id):
        """Returns the identifier of the parent station of the given station ID

        Parameters
        ----------

        station_id: the station identifier to get the parent ID of.
        """
        return self.parents[int(station_id)]
