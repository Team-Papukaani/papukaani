from itertools import count


class Gathering:
    '''
    Represets the gatherings in a Document table in LajiStore
    '''
    def __init__(self, dateBegin, geometry, higherGeography = 'x', areaDetail = 'x',
                 country = 'x', notes = '0', publicityRestrictions="MZ.publicityRestrictionsPrivate"):
        self.dateBegin = dateBegin
        self.geometry = geometry
        self.notes = notes # Temporarily? holds temperature in a string
        self.publicityRestrictions = publicityRestrictions
        self.higherGeography = higherGeography
        self.areaDetail = areaDetail
        self.country = country

    def to_lajistore_json(self):
        '''
        Returns the fields in a LajiStore-saveable format.
        :return: A dictionary
        '''
        return {"dateBegin":self.dateBegin,
                "wgs84Geometry":{ "type":"Point", "coordinates" : self.geometry},
                "higherGeography":self.higherGeography,
                "areaDetail":self.areaDetail,
                "country":self.country,
                "notes":self.notes,
                "publicityRestrictions":self.publicityRestrictions}


    def __key(self):
        return  self.dateBegin, "%.9f" % self.geometry[0], "%.9f" % self.geometry[1], "%.9f" % float(self.notes)

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
                     higherGeography=kwargs["higherGeography"],
                     areaDetail=kwargs["areaDetail"],
                     country=kwargs["country"],
                     notes=kwargs["notes"],
                     publicityRestrictions=kwargs["publicityRestrictions"])