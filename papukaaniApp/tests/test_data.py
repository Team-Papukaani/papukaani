from papukaaniApp.models import GeneralParser
jouko_parser = GeneralParser.objects.create(
         formatName="jouko",
         latitude="Latitude(N)",
         longitude="Longitude(E)",
         time='Time', date='Date',
         delimiter="\t")