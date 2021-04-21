# Gordian Software Python Developer Coding Challenge - Vansh Gupta

import xml.etree.ElementTree as ET
import json
import xml.dom.minidom

xmlparse2 = xml.dom.minidom.parse('seatmap2.xml')
prettyxml2 = xmlparse2.toprettyxml()
root2 = ET.fromstring(prettyxml2)

prices = {}
seat_prices = {}

for price in root2[3]:
    prices[price.get('OfferItemID')] = price[1][0][0].text

for row in root2.iter('{http://www.iata.org/IATA/EDIST/2017.2}Row'):
    row_num = row[0].text
    for seat in row.findall('{http://www.iata.org/IATA/EDIST/2017.2}Seat'):
        seat_id = row_num + seat.find('{http://www.iata.org/IATA/EDIST/2017.2}Column').text
        try:
            seat_prices[seat_id] = prices[seat.find('{http://www.iata.org/IATA/EDIST/2017.2}OfferItemRefs').text]
        except:
            seat_prices[seat_id] = "No Price Available"

xmlparse = xml.dom.minidom.parse('seatmap1.xml')
prettyxml = xmlparse.toprettyxml()
root = ET.fromstring(prettyxml)

data = {}
data ['Seats'] = []

for row in root.iter('{http://www.opentravel.org/OTA/2003/05/common/}RowInfo'):
    for seat in row.findall('{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo'):
        j = 0
        for i in range(len(seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features'))):
            if seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')[i].text == 'Center' or seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')[i].text == 'Aisle' or seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')[i].text == 'Window':
                j = i
        seat_type = seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')[j].text + " Seat"
        if seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')[j].text == 'Other_':
            seat_type = seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')[j].get('extension')
        held = 'false'
        if seat.find('{http://www.opentravel.org/OTA/2003/05/common/}Status') is not None:
            held = 'true'
        data ['Seats'].append({
                "Type": seat_type,
                "Seat id": seat[0].attrib['SeatNumber'],
                "Availability": seat[0].attrib['AvailableInd'],
                "Cabin Class": row.attrib['CabinType'] + " Class",
                "Held": held
            })
            

for seat in data ['Seats']:
    seat_id = seat["Seat id"]
    try:
        seat['Price'] = seat_prices[seat_id]
    except:
        seat['Price'] = "No Price Available"

json_formatted_str = json.dumps(data, indent=2)
# print(json_formatted_str)

# Creates new json file in directory
filePathNameWExt = './' + './' + '/' + 'FILENAME_parsed' + '.json'
with open(filePathNameWExt, 'w') as fp:
    json.dump(data, fp)