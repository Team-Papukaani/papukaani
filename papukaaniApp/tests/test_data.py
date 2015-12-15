from papukaaniApp.models import GeneralParser


def create_jouko_parser():
    return GeneralParser.objects.create(
             formatName="jouko",
             latitude="Latitude(N)",
             longitude="Longitude(E)",
             time='Time', date='Date',
             delimiter="\t")