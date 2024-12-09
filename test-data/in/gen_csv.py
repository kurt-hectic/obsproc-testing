import csv

from datetime import datetime, timedelta

nr_stations = 1000
nr_obs = 1000

start_date = datetime(2024,1,1)

wsis = [ "0-20000-99-{}".format(i) for i in range(0,nr_stations) ]
obs = [ start_date + timedelta(hours=h) for h in range(0,nr_obs) ]

header = { "year": None ,"month": None ,"day": None ,"hour": None ,"minute": None, "longitude": 60.00 ,"latitude": 70.00 ,
"wigosIdentifierSeries":None,
"wigosIssuerOfIdentifier":None,
"wigosIssueNumber":None,
"wigosLocalIdentifierCharacter":None,
"temperature":11.22,"pressure":22.33 }
 

for wsi in wsis:

    with open("obs1m"+wsi+".csv", 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames = header.keys() )
        
        writer.writeheader()
        
        for o in obs:
        
            temp2 = wsi.split("-")
            
            temp = { "year": o.year, "month": o.month, "day": o.day, "hour": o.hour, "minute": o.minute, 
                    "wigosIdentifierSeries":temp2[0],
                    "wigosIssuerOfIdentifier":temp2[1],
                    "wigosIssueNumber":temp2[2],
                    "wigosLocalIdentifierCharacter":temp2[3]
            }
            
            row = header.copy()
            row.update(temp)
        
            writer.writerow(row)