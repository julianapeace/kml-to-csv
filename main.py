from bs4 import BeautifulSoup
import csv
file = 'Newsletter 177.kml'
chars = [',', '.']

def main():
    def no_punc(text):
        return text.translate({ord(k): None for k in chars})

    def extract(obj):
        ret = []
        name_obj = no_punc(obj.find("name").text).split(" ")
        number = name_obj[0]
        district = name_obj[1]
        city = name_obj[2]

        address = obj.find('address').text
        description = obj.find('description').text
        desc = description.split("<br>")
        link = desc[0].split(' ')[3:]
        eng_link = desc[1].split(' ')[2:]
        maps = desc[2].split(' ')[2:]
        # skip address here
        jpy_price = desc[4].split(' ')[2:]
        usd_price = desc[5].split(' ')[2:]

        ret.append(number)
        if city != "City":
            ret.append(district)
            ret.append(city)
        else:
            ret.append("")
            ret.append("".join(district+" "+city))

        ret.append(address)
        ret.append(link[0])
        ret.append(eng_link[0])
        if "万円" not in jpy_price[0]:
            p = jpy_price[0]+"万円"
            ret.append(p)
        else:
            ret.append(jpy_price[0])
        ret.append(usd_price[0])
        if len(desc) >= 7: # range
            ret.append(" ".join(desc[6].split(' ')[2:]))
        if len(desc) >= 8: #instagram
            ret.append(desc[7].split(' ')[1:][0])
        return ret


    def generate_placemarks():
        ret = []
        with open(file, 'r') as f:
            s = BeautifulSoup(f, 'xml')
            placemark = s.find_all('Placemark')
            for place in placemark:
                ret.append(place)
        return ret
    
    
    placemarks = generate_placemarks()

    with open('out.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Number","District", "City", "Address", "Link", "Eng Link", "JPY Price", "USD Price", "Range", "Instagram"])
        for place in placemarks:
            writer.writerow(extract(place))

if __name__ == "__main__":
    main()