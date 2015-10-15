class Gathering:
    '''
    Represets the gatherings in a Document table in LajiStore
    '''

    def __init__(self, time, geometry, temperature, facts):
        self.time = time
        self.geometry = geometry
        self.temperature = temperature
        self.facts = facts

    def to_lajistore_json(self):
        '''
        Returns the fields in a LajiStore-saveable format.
        :return: A dictionary
        '''
        return {"timeStart": self.time, "wgs84Geometry": {"type": "Point", "coordinates": self.geometry},
                "temperatureCelsius": self.temperature, "facts": self.facts}


def from_lajistore_json(**kwargs):
    '''
    Creates a Gathering object from LajiStore-format json
    :param kwargs: The data from LajiStore
    :return: a Gathering object
    '''
    return Gathering(kwargs["timeStart"], kwargs["wgs84Geometry"]["coordinates"], kwargs["temperatureCelsius"],
                     kwargs["facts"])
