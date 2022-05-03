import os
from typing import Optional

from flask import Flask, render_template, request

from famapy.metamodels.fm_metamodel.models import FeatureModel
from famapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader

from fm_characterization import FMCharacterization


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
        reference = request.form['inputReference']
        keywords = request.form['inputKeywords']
        domain = request.form['inputDomain']
        year = request.form['inputYear']
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
            
            characterization = FMCharacterization(fm)
            characterization.metadata.name=name
            characterization.metadata.description=description
            characterization.metadata.author=author
            characterization.metadata.year=year
            characterization.metadata.tags=keywords
            characterization.metadata.reference=reference
            characterization.metadata.domains=domain
            
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


        if os.path.exists(filename):
            os.remove(filename)
        
        return render_template('index.html', data=data)


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    app.run(host='0.0.0.0')