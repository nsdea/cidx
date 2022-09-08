import json
import random

from countryinfo import CountryInfo

def country_list(
        hdi_cfg: int=0,
        gdp_cfg: int=0,
        gini_cfg: int=0,
        population_cfg: int=0,
        area_cfg: int=0
    ):
    countries = []
    
    for name, details in CountryInfo().all().items():
        countries.append(get_country(name, details))

    json.dump(countries, open('data/processed.json', 'w'))
    return countries

def get_country(name, details):
    try:
        gdp = json.load(open('data/gdp.json'))[details['ISO']['alpha3']]
    except KeyError:
        gdp = '?'

    try:
        population = CountryInfo(name).population()
    except KeyError:
        population = '?'

    try:
        area = details['area']
    except KeyError:
        area = '?'

    return {
        'Name': name.title(),
        'GDP': gdp,
        'Area': area or '0',
        'Population': population
    }

def render_globe():
    countries = json.load(open('data/countries.json'))
    world_map = '['

    for c in countries:
        world_map += \
            '\n    {"id": "ID", "name": "NAME", "value": VALUE, polygonTemplate: {fill: colors.getIndex(CONTINENT)}},' \
            .replace('ID', c['id']) \
            .replace('NAME', c['name']) \
            .replace('VALUE', str(random.randint(1, 10))) \
            .replace('CONTINENT', str(c['continent']))

    world_map = str(world_map)[:-3] + "}}\n]"
    return world_map

def _():
    country = CountryInfo('Singapore')
    country.info()
