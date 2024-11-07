import os
import sys
import json
import logging
from typing import Optional

from flask import Flask, render_template, request, g, redirect, url_for

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader

from fm_characterization import FMCharacterization
from fm_characterization import models_info
import config

STATIC_DIR = 'web'
EXAMPLE_MODELS_DIR = 'fm_models'


app = Flask(__name__,
            static_url_path='',
            static_folder=STATIC_DIR,
            template_folder=STATIC_DIR)
app.config.from_object(config)

# Add version to the global context before each request
@app.before_request
def add_version_to_g():
    g.version = app.config['VERSION']


# Automatically add the version parameter in each generated URL
@app.url_defaults
def add_version_to_url(endpoint, values):
    if 'v' not in values:
        values['v'] = g.version


# Redirect automatically to the URL with the version parameter if not present
@app.before_request
def enforce_version_in_url():
    if 'v' not in request.args:
        return redirect(url_for(request.endpoint, **request.view_args, v=g.version))


def read_fm_file(filename: str) -> Optional[FeatureModel]:
    try:
        if filename.endswith(".uvl"):
            return UVLReader(filename).transform()
        elif filename.endswith(".xml") or filename.endswith(".fide"):
            return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    try:
        return UVLReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    try:
        return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    return None


# Get example models
EXAMPLE_MODELS = {m[models_info.NAME]: m for m in models_info.MODELS}


@app.route('/', methods=['GET', 'POST'])
def index():
    version = request.args.get('v')
    if version != g.version:
        return "Incorrect version", 404
    
    data = {}
    data['uploadFM'] = True
    data['models'] = EXAMPLE_MODELS

    if request.method == 'GET':
        return render_template('index.html', data=data)

    if request.method == 'POST':
        light_fact_label = 'lightFactLabel' in request.form
        logging.warning(f'light_fact_label: {light_fact_label}')
        fm_file = request.files['inputFM']
        fm_name = request.form['inputExample']
        name = None
        description = None
        author = None
        year = None
        keywords = None
        reference = None
        domain = None

        if not fm_file and not fm_name:
            # The file is required and this is controlled in the front-end.
            data['file_error'] = 'Please upload a feature model or select one from the examples.'
            return render_template('index.html', data=data)

        if fm_file:
            filename = fm_file.filename
            fm_file.save(filename)
        elif fm_name in EXAMPLE_MODELS.keys():
            filename = os.path.join(STATIC_DIR, EXAMPLE_MODELS_DIR, EXAMPLE_MODELS[fm_name][models_info.FILENAME])
            name = EXAMPLE_MODELS[fm_name][models_info.NAME]
            description = EXAMPLE_MODELS[fm_name][models_info.DESCRIPTION]
            author = EXAMPLE_MODELS[fm_name][models_info.AUTHOR]
            reference = EXAMPLE_MODELS[fm_name][models_info.REFERENCE]
            keywords = EXAMPLE_MODELS[fm_name][models_info.KEYWORDS]
            keywords = ', '.join(keywords)
            domain = EXAMPLE_MODELS[fm_name][models_info.DOMAIN]
            year = EXAMPLE_MODELS[fm_name][models_info.YEAR]
            data['fm_example'] = os.path.join(EXAMPLE_MODELS_DIR, EXAMPLE_MODELS[fm_name][models_info.FILENAME])
        else:
            data['file_error'] = 'Please upload a feature model or select one from the examples.'
            return render_template('index.html', data=data)

        if request.form['inputName']:
            name = request.form['inputName']
        if request.form['inputDescription']:
            description = request.form['inputDescription']
            description = description.replace(os.linesep, ' ')
        if request.form['inputAuthor']:
            author = request.form['inputAuthor']
        if request.form['inputReference']:
            reference = request.form['inputReference']
        if request.form['inputKeywords']:
            keywords = request.form['inputKeywords']
        if request.form['inputDomain']:
            domain = request.form['inputDomain']
        if request.form['inputYear']:
            year = request.form['inputYear']

        try:
            # Read the feature model
            fm = read_fm_file(filename)
            if fm is None:
                data['file_error'] = 'Feature model format not supported.'
                return render_template('index.html', data=data)
            if not name:
                name = os.path.splitext(os.path.basename(filename))[0]

            characterization = FMCharacterization(fm, light_fact_label)
            characterization.metadata.name = name
            characterization.metadata.description = description
            characterization.metadata.author = author
            characterization.metadata.year = year
            characterization.metadata.tags = keywords
            characterization.metadata.reference = reference
            characterization.metadata.domains = domain

            #json_characterization = interfaces.to_json(fm_characterization, FM_FACT_JSON_FILE)
            json_characterization = characterization.to_json()
            json_str_characterization = characterization.to_json_str()
            str_characterization = str(characterization)
            data['fm_facts'] = json_characterization
            data['fm_characterization_json_str'] = json_str_characterization
            data['fm_characterization_str'] = str_characterization
        except Exception as e:
            data = None
            print(e)
            raise e

        if os.path.exists(filename) and filename == fm_file.filename:
            os.remove(filename)

        return render_template('index.html', data=data)


@app.route('/uploadJSON', methods=['GET', 'POST'])
def uploadJSON():
    version = request.args.get('v')
    if version != g.version:
        return "Incorrect version", 404
    
    data = {}
    data['uploadJSON'] = True
    data['models'] = EXAMPLE_MODELS

    if request.method == 'GET':
        return render_template('index.html', data=data)

    if request.method == 'POST':
        json_file = request.files['inputJSON']
        if not json_file:
            # The file is required and this is controlled in the front-end.
            data['file_error'] = 'Please upload a JSON file.'
            return render_template('index.html', data=data)
        
        filename = json_file.filename
        json_file.save(filename)
        try:
            # Read the json
            json_characterization = json.load(open(filename))
            if json_characterization is None:
                data['file_error'] = 'JSON format not supported.'
                return render_template('index.html', data=data)
            data['fm_facts'] = json_characterization
        except Exception as e:
            data = None
            print(e)
            raise e

        if os.path.exists(filename) and filename == json_file.filename:
            os.remove(filename)

        return render_template('index.html', data=data)


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    #logging.basicConfig(filename='app.log', level=logging.INFO)

    app.run(host='0.0.0.0', debug=True)
