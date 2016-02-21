from itertools import count


class Gathering:
    '''
    Represets the gatherings in a Document table in LajiStore
    '''
    def __init__(self, dateBegin, geometry, temperature = 0, higherGeography = 'x', country = 'x', publicityRestrictions="MZ.publicityRestrictionsPrivate"):
        self.dateBegin = dateBegin
        self.geometry = geometry
        self.temperature = temperature
        self.publicityRestrictions = publicityRestrictions
        self.higherGeography = higherGeography
        self.country = country

    def to_lajistore_json(self):
        '''
        Returns the fields in a LajiStore-saveable format.
        :return: A dictionary
        '''
        return {"dateBegin":self.dateBegin,
                "wgs84Geometry":{ "type":"Point", "coordinates" : self.geometry},
                "temperature":self.temperature,
                "higherGeography":self.higherGeography,
                "country":self.country,
                "publicityRestrictions":self.publicityRestrictions}


    def __key(self):
        return  self.dateBegin, "%.9f" % self.geometry[0], "%.9f" % self.geometry[1], "%.9f" % self.temperature

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.__dict__)

def from_lajistore_json(**kwargs):
    '''
    Creates a Gathering object from LajiStore-format json
    :param kwargs: The data from LajiStore
    :return: a Gathering object
    '''
    return Gathering(dateBegin = kwargs["dateBegin"],
                     geometry= kwargs["wgs84Geometry"]["coordinates"],
                     temperature = kwargs["temperature"],
                     higherGeography=kwargs["higherGeography"],
                     country=kwargs["country"],
                     publicityRestrictions=kwargs["publicityRestrictions"])