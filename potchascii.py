#!/usr/bin/python3
# Potchascii
# version 0.3

import sys, time
from urllib import request, parse
from xml.dom import minidom
from yaml import load

def load_config():
    try:
        cfg = load(open('config.yml'))
    except:
        sys.exit('Error: That config file doesn\'t seem to be valid. Are you sure you haven\'t messed it up somehow?')
    return cfg


def load_weather(url):
    try:
        xml = request.urlopen(url).read()
    except:
        sys.exit('Error: The server returns some bullshit ... something wrong with your city perhaps?')

    try:
        xml = minidom.parseString(xml)
        xml_times = xml.getElementsByTagName('time')
    except:
        sys.exit('Error: Invalid data?!? Contact your system administrator or something. =P')

    return xml_times


def potchascii(city):
    url = 'http://www.yr.no/place/{0}/{1}/{2}/forecast_hour_by_hour.xml'.format(parse.quote(city['country']), parse.quote(city['region']), parse.quote(city['town']))

    tmr_date = time.localtime(time.time() + 24*3600)
    day = 0
    today = {'sun':False, 'rain':False, 'min_temp':0, 'max_temp':0}
    tomorrow = {'sun':False, 'rain':False, 'min_temp':0, 'max_temp':0}

    xml_times = load_weather(url)
    for moment in xml_times:
        if moment.attributes['from'].value[0:10] == time.strftime('%Y-%m-%d'):
            symbol = moment.getElementsByTagName('symbol')[0].attributes['name'].value
            temp = int(moment.getElementsByTagName('temperature')[0].attributes['value'].value)

            if day == 0:
                today['min_temp'] = temp
                today['max_temp'] = temp
                day = 1

            # TODO: add sunrise and sunset to the glasses check
            if int(cfg['day-start']) < int(moment.attributes['from'].value[11:13]) < int(cfg['day-end']):
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


    print('The temperatures today should be somewhere between ' + str(today['min_temp']) + '°C and ' + str(today['max_temp']) + '°C.' if today['min_temp'] != today['max_temp'] else 'Today is simply gonna be ' + str(today['max_temp']) + '°C. Weird right?')
    if today['sun'] and cfg['glasses']: print('And the sun\'s gonna shine SO hard!')
    if today['rain'] and cfg['umbrella']: print('Wouldn\'t go out without and umbrella tho!')
    print('Tomorrow you can expect temperatures between ' + str(tomorrow['min_temp']) + '°C and ' + str(tomorrow['max_temp']) + '°C' + (' with a pretty good chance of rain.' if tomorrow['rain'] and cfg['umbrella'] else '.') + (' You should take your sunglasses with you as well.' if tomorrow['sun'] and cfg['glasses'] else ''))

if __name__ == '__main__':
    cfg = load_config()

    if len(sys.argv) > 2:
        sys.exit('Only put in ONE place abbreviation from your favorites list ... just 1 ok?')
    elif len(sys.argv) == 2:
        code = sys.argv[1]
    else:
        code = cfg['default']

    for place in cfg['favorites']:
        if place['code'] == code:
            city = place
            break

    if not city:
        sys.exit('Error: Umm, I\'m not quite sure what place you want me to show.')

    potchascii(city)
