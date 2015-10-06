class Gathering():

    def __init__(self, time, geometry, temperature, facts):
        self.time = time
        self.geometry = geometry
        self.temperature = temperature
        self.facts = facts

    def to_lajistore_json(self):
        return {"timeStart":self.time, "wgs84Geometry":{ "type":"Point", "coordinates" : self.geometry}, "temperatureCelsius":self.temperature, "facts":self.facts}


def from_lajistore_json(**kwargs):
    return Gathering(kwargs["timeStart"], kwargs["wgs84Geometry"]["coordinates"], kwargs["temperatureCelsius"], kwargs["facts"])



