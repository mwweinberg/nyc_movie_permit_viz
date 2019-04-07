#python3

import csv
from mapbox import Geocoder
import time

#to open the input csv
film_file = open('Film_Permits_Nohead_no_T1.csv')
film_reader = csv.reader(film_file)

#to open the output csv
output_file = open('output.csv', 'w')
output_writer = csv.writer(output_file)

#for the mapbox api
geocoder = Geocoder(access_token=[YOUR ACCESS TOKEN IN QUOTE MARKS HERE])

#to keep track of things so that you can stay below the free mapbox limit (look in your dashboard to see where you are)
counter = 0


for row in film_reader:



        print(row[6])
        print(row[13])
        #grabs the first zipcode because life is short
        zip_split = list(row[13].split(', '))
        first_zip = zip_split[0]

        borough = row[7]

        #splits up the addresses
        addresses = list(row[6].split(',  '))
        #works through the addresses
        #here is where you are going to want to do the lookup
        for address in addresses:
            address_no_between = address.replace('between', ' ')
            address_fully_stripped = address_no_between.replace('and', ' ')
            print(address_fully_stripped)
            #adds the address to the end of the row
            row.append(address_fully_stripped)

            #this is what you are going to send to the geocoder
            geocoder_entry = borough + ' New York City ' + first_zip + ' ' + address_fully_stripped
            print("GC entry = " + geocoder_entry)

            #looks up the address and pulls the lat and long
            response = geocoder.forward(geocoder_entry)
            counter += 1
            collection = response.json()
            lat = collection['features'][0]['center'][1]
            #writes it to the csv
            #row.append(lat)
            long = collection['features'][0]['center'][0]
            #row.append(long)

            #if the geolookup worked the long will be a neative number
            if int(long) < 0:
                row.append(lat)
                row.append(long)
                output_writer.writerow(row)
            #if it didn't work the lookup will return a value in Africa
            #this re-runs the lookup with just the first street in the address
            else:
                short_address = address_fully_stripped.split('  ', 1)[0]
                short_geocoder_entry = borough + ' New York City ' + first_zip + ' ' + short_address
                print("Short GC entry = " + short_geocoder_entry)
                response = geocoder.forward(short_geocoder_entry)
                counter += 1
                collection = response.json()
                lat = collection['features'][0]['center'][1]
                long = collection['features'][0]['center'][0]
                row.append(lat)
                row.append(long)
                output_writer.writerow(row)



            #print(row[13])
            #writes the newly expanded row
            #the if statement gets rid of the bad matches
            #if int(long) < 0:
                #output_writer.writerow(row)


            #removes the address. If you skip this then the second or third address ends up getting tacked on to the end of the row
            row.remove(address_fully_stripped)
            row.remove(lat)
            row.remove(long)
            print("Counter = " + str(counter))
        print('')
        time.sleep(0.1)
