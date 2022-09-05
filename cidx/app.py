import json
import flask
import random
import logging
import pandas as pd

app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

sliders = ['HDI', 'GDP', 'Gini', 'Population', 'Area']

@app.route('/favicon.ico')
def fav():
    return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
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
        # table = pd.DataFrame(data=world_map).to_html()

        return flask.render_template('index.html', sliders=sliders, world_map=world_map)

    return flask.request.form

app.run(port=3838, debug=True)