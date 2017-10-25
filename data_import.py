import csv
import datetime
from decimal import *
from ratsightings.models import RatSighting

getcontext().prec = 10

def import_data():
    RatSighting.objects.all().delete()

    with open('data/data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        for row in reader:
            try:
                key = int(row[0])
                dateCreated = row[1]
                dateCreated = datetime.datetime.strptime(dateCreated, "%m/%d/%Y %H:%M:%S %p")
                locationType = row[7]
                zipCode = int(row[8])
                address = row[9]
                city = row[16]
                borough = row[23]
                latitude = Decimal(row[49])
                longitude = Decimal(row[50])
            except:
                #print("Failed " + ",".join(row))
                continue

            if (key is None) or (dateCreated is None) or (zipCode is None) or (latitude is None) or (longitude is None) or len(locationType) == 0 or len(address) == 0 or len(city) == 0 or len(borough) == 0:
                #print("Failed " + row[0])
                continue

            try:
                q = RatSighting(id=key, owner_id=1, date_created=dateCreated, location_type=locationType, zip_code=zipCode, address=address, city=city, borough=borough, latitude=latitude, longitude=longitude)
                q.save()
            except:
                pass