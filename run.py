import os
from typing import Optional

from flask import Flask, render_template, request

from famapy.metamodels.fm_metamodel.models import FeatureModel
from famapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader
from fm_characterization.models.fm_characterization import FMCharacterization
from fm_characterization.models import interfaces

app = Flask(__name__,
            static_url_path='', 
            static_folder='web',
            template_folder='web')


def read_fm_file(filename: str) -> Optional[FeatureModel]:
    try:
        return UVLReader(filename).transform() 
    except:
        pass
    try:
        return FeatureIDEReader(filename).transform() 
    except:
        pass
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        data = {}

        name = request.form['inputName']
        description = request.form['inputDescription']
        description = description.replace(os.linesep, ' ')
        author = request.form['inputAuthor']
        # reference = request.form['inputReference']
        keywords = request.form['inputKeywords']
        domain = request.form['inputDomain']
        fm_file = request.files['inputFM']

        if not fm_file:
            # The file is required and this is controlled in the front-end.
            pass

        filename = fm_file.filename
        try:
            fm_file.save(filename)
            
            # Read the feature model
            fm = read_fm_file(filename)
            if fm is None:
                data['file_error'] = 'Feature model format not supported.'
                return render_template('index.html', data=data) 
            if not name:
                name = os.path.splitext(os.path.basename(filename))[0]
            
            characterization = FMCharacterization(fm, name)
            characterization.set_metadata(name=name, description=description, author=author, tags=keywords, domains=domain)
            #json_characterization = interfaces.to_json(fm_characterization, FM_FACT_JSON_FILE)
            json_characterization = interfaces.to_json(characterization)
            json_str_characterization = interfaces.to_json_str(characterization)
            str_characterization = interfaces.get_string_output(characterization)
            data['fm_facts'] = json_characterization
            data['fm_characterization_str'] = str_characterization
            data['fm_characterization_json_str'] = json_str_characterization
        except Exception as e:
            data = None
            print(e)

        if os.path.exists(filename):
            os.remove(filename)
        
        return render_template('index.html', data=data)


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    app.run(host='0.0.0.0')