class Gathering:
    '''
    Represets the gatherings in a Document table in LajiStore
    '''
    def __init__(self, time, geometry, temperature = 0, publicity="private", facts=None):
        self.time = time
        self.geometry = geometry
        self.temperature = temperature
        self.facts = facts
        self.publicity = publicity

        if not facts:
            self.facts = []

    def to_lajistore_json(self):
        '''
        Returns the fields in a LajiStore-saveable format.
        :return: A dictionary
        '''
        return {"timeStart":self.time, "wgs84Geometry":{ "type":"Point", "coordinates" : self.geometry}, "temperatureCelsius":self.temperature, "publicity":self.publicity,  "facts":self.facts}


    def __key(self):
        return  (self.time, "%.9f" % self.geometry[0], "%.9f" % self.geometry[1], "%.9f" % self.temperature)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

def from_lajistore_json(**kwargs):
    '''
    Creates a Gathering object from LajiStore-format json
    :param kwargs: The data from LajiStore
    :return: a Gathering object
    '''
    return Gathering( time = kwargs["timeStart"], geometry= kwargs["wgs84Geometry"]["coordinates"], temperature=kwargs["temperatureCelsius"],publicity=kwargs["publicity"], facts=kwargs["facts"])

