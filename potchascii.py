#!/usr/bin/python3
# Potchascii
# version 0.2

import sys, time
from urllib import request, parse
from xml.dom import minidom


def load_file(url):
    try:
        xml = request.urlopen(url).read()
    except:
        sys.exit('Error: Server vrací nějakou blbost ... možná chybné město? (Musí být v Česku.)')

    try:
        xml = minidom.parseString(xml)
        xml_times = xml.getElementsByTagName('time')
    except:
        sys.exit('Error: Chybná data?!? Obraťte se na správce systému. =P')

    return xml_times


def potchascii(city):
    url = 'http://www.yr.no/place/Czech_Republic/{0}/{0}/forecast_hour_by_hour.xml'.format(parse.quote(city))
    # FIXME: Některá města mají před sebou svůj kraj, takže tento formát u nich nevyhovuje. Databázička?

    tmr_date = time.localtime(time.time() + 24*3600)
    day = 0 # pomocná proměnná na rozpoznávání nového dne - kratší a jednodušší, než kontrolovat časomíru
    today = {'sun':False, 'rain':False, 'min_temp':0, 'max_temp':0}
    tomorrow = {'sun':False, 'rain':False, 'min_temp':0, 'max_temp':0}

    xml_times = load_file(url)
    for moment in xml_times:
        if moment.attributes['from'].value[0:10] == time.strftime('%Y-%m-%d'):
            symbol = moment.getElementsByTagName('symbol')[0].attributes['name'].value
            temp = int(moment.getElementsByTagName('temperature')[0].attributes['value'].value)

            if day == 0:
                today['min_temp'] = temp
                today['max_temp'] = temp
                day = 1

            # TODO: předělat brýle podle východu/západu slunce
            # TODO: config na časy a možná na defaultní město?
            if 7 < int(moment.attributes['from'].value[11:13]) < 21:
                if temp < today['min_temp']: today['min_temp'] = temp
                if temp > today['max_temp']: today['max_temp'] = temp
                if symbol in ['Clear sky', 'Fair']: today['sun'] = True
                if symbol in ['Light rain showers', 'Rain showers', 'Light rain', 'Rain', 'Heavy rain', 'Light sleet showers', 'Sleet showers', 'Light sleet', 'Sleet', 'Heavy sleet']: today['rain'] = True

        elif moment.attributes['from'].value[0:10] == '-'.join([str(tmr_date.tm_year), str(tmr_date.tm_mon), str(tmr_date.tm_mday)]):
            symbol = moment.getElementsByTagName('symbol')[0].attributes['name'].value
            temp = int(moment.getElementsByTagName('temperature')[0].attributes['value'].value)

            if day < 2:
                tomorrow['min_temp'] = temp
                tomorrow['max_temp'] = temp
                day = 2

            if 6 < int(moment.attributes['from'].value[11:13]) < 21:
                if temp < tomorrow['min_temp']: tomorrow['min_temp'] = temp
                if temp > tomorrow['max_temp']: tomorrow['max_temp'] = temp
                if symbol in ['Clear sky', 'Fair']: tomorrow['sun'] = True
                if symbol in ['Light rain showers', 'Rain showers', 'Light rain', 'Rain', 'Heavy rain', 'Light sleet showers', 'Sleet showers', 'Light sleet', 'Sleet', 'Heavy sleet']: tomorrow['rain'] = True

    print('Teploty se dnes budou pohybovat mezi ' + str(today['min_temp']) + '°C a ' + str(today['max_temp']) + '°C.')
    if today['sun']: print('Bude to taky pěkně šajnit!')
    if today['rain']: print('Bez deštníku bych ven ale nechodil!')
    print('Zítra očekávej teploty mezi ' + str(tomorrow['min_temp']) + '°C a ' + str(tomorrow['max_temp']) + '°C' + (' s tím, že asi bude pršet.' if tomorrow['rain'] else '.') + (' Vzal bych si navíc sluneční brýle.' if tomorrow['sun'] else ''))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit('Zadejte jedno město! ... 1 (víceslovný název do uvozovek)')
    elif len(sys.argv) == 2:
        city = sys.argv[1]
    else:
        city = 'Liberec'

    potchascii(city)
