#! /usr/bin/python3
# Potchascii
# version 0.1

import sys, time
from urllib import request
from xml.dom import minidom

def potchascii(city):
    url = 'http://www.yr.no/place/Czech_Republic/{0}/{0}/forecast_hour_by_hour.xml'.format(city)

    try:
        xml = request.urlopen(url).read()
    except:
        sys.exit('Error: Server vrací nějakou blbost ... možná chybné město?')

    try:
        xml = minidom.parseString(xml)
        xml_times = xml.getElementsByTagName('time')
    except:
        sys.exit('Error: Chybná data?!?')

    tomorrow = time.localtime(time.time() + 24*3600)

    day = 0
    for moment in xml_times:
        if moment.attributes['from'].value[0:10] == time.strftime('%Y-%m-%d'):
            if day == 0:
                print('dnes (' + time.strftime('%d. %m.') + "):")
                day = 1
            print(moment.getElementsByTagName('temperature')[0].attributes['value'].value + '°C ' + moment.getElementsByTagName('symbol')[0].attributes['name'].value)
        elif moment.attributes['from'].value[0:10] == '-'.join([str(tomorrow.tm_year), str(tomorrow.tm_mon), str(tomorrow.tm_mday)]):
            if day == 1:
                print('zítra (' + str(tomorrow.tm_mday) + '. ' + str(tomorrow.tm_mon) + '.):')
                day = 2
            print(moment.getElementsByTagName('temperature')[0].attributes['value'].value + '°C ' + moment.getElementsByTagName('symbol')[0].attributes['name'].value)

# TODO: nejdřív načítat data do tabulky, pak je zpracovat a zobrazit až výsledky

if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("Zadejte jedno město! ... 1")
    elif len(sys.argv) == 2:
        city = sys.argv[1]
    else:
        city = 'Liberec'

    potchascii(city)