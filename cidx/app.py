import flask
import logging

import data

app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

sliders = ['HDI', 'GDP', 'Gini', 'Population', 'Area']

@app.route('/', methods=['GET', 'POST'])
def index():
    form = flask.request.form.get

    if flask.request.method == 'GET':
        # table = pd.DataFrame(data=world_map).to_html()

        return flask.render_template(
            'index.html',
            sliders=sliders,
            world_map=data.render_globe(),
            country_table=data.country_list(
                hdi_cfg=form('hdi'),
                gdp_cfg=form('gdp'),
                gini_cfg=form('gini'),
                population_cfg=form('population'),
                area_cfg=form('area')
            )
        )

    return flask.request.form

app.run(port=3838, debug=True)