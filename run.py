import os
from typing import Optional

from flask import Flask, render_template, request

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader

from fm_characterization import FMCharacterization
from fm_characterization import models_info


STATIC_DIR = 'web'
EXAMPLE_MODELS_DIR = 'fm_models'


app = Flask(__name__,
            static_url_path='',
            static_folder=STATIC_DIR,
            template_folder=STATIC_DIR)


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


# This sets the basepath from FLASK_BASE_PATH env variable
# basepath = os.environ.get("FLASK_BASE_PATH")

# if basepath == None:
#     basepath = ""
# else:
#     os.system("ln -sf /app/web /app/" + static_dir + "/" + basepath)
#     basepath = "/" + basepath

# Get example models
EXAMPLE_MODELS = {m[models_info.NAME]: m for m in models_info.MODELS}
# for root, dirs, files in os.walk(os.path.join(static_dir, EXAMPLE_MODELS_DIR)):
#     for file in files:
#         #filepath = os.path.join(root, file)
#         EXAMPLE_MODELS.append(file)
# EXAMPLE_MODELS.sort()


@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    data['models'] = EXAMPLE_MODELS

    if request.method == 'GET':
        return render_template('index.html', data=data)

    if request.method == 'POST':
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

            characterization = FMCharacterization(fm)
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


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
