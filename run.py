import os
from zipfile import ZipFile
import shutil
import tempfile
from typing import Optional, Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median

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

def extract_zip(zip_path: str) -> Tuple[str, list]:
    extract_dir = tempfile.mkdtemp()
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        extracted_files = zip_ref.namelist()
    return extract_dir, extracted_files


def process_single_file(file_path: str) -> Optional[FMCharacterization]:
    fm = read_fm_file(file_path)
    if fm:
        return FMCharacterization(fm)
    return None

def process_files(extracted_files: list, extract_dir: str, zip_filename: str) -> Optional[Dict[str, Any]]:
    metrics_data = {}
    model_count = 0
    dataset_characterization = None

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_single_file, os.path.join(extract_dir, file)): file for file in extracted_files if file.endswith('.uvl')}
        
        for future in as_completed(futures):
            try:
                characterization = future.result()
                if characterization:
                    model_count += 1
                    if dataset_characterization is None:
                        dataset_characterization = characterization
                        # Initialize metrics data
                        for m in characterization.metrics.get_metrics():
                            metrics_data[m.property.name] = {'sizes': [], 'ratios': []}
                    
                    current_metrics = {m.property.name: m.size if m.size is not None else m.value for m in characterization.metrics.get_metrics()}
                    current_ratios = {m.property.name: m.ratio for m in characterization.metrics.get_metrics() if m.ratio is not None}
                    
                    # Store size metrics
                    for key, value in current_metrics.items():
                        metrics_data[key]['sizes'].append(value)
                    
                    # Store ratio metrics
                    for key, value in current_ratios.items():
                        metrics_data[key]['ratios'].append(value)
            except Exception as e:
                print(f"Error processing file {futures[future]}: {e}")

    if model_count > 0 and metrics_data:
        dataset_characterization_json = dataset_characterization.to_json()

        dataset_characterization_json['metadata'][0]['value'] = zip_filename

        for metric in dataset_characterization_json['metrics']:
            name = metric['name']
            if name in metrics_data:
                sizes = metrics_data[name]['sizes']
                ratios = metrics_data[name]['ratios']
                
                metric['size'] = mean(sizes) if sizes else None
                metric['ratio'] = mean(ratios) if ratios else None
                metric['stats'] = {
                    'mean': mean(sizes) if sizes else None,
                    'median': median(sizes) if sizes else None,
                    'min': min(sizes) if sizes else None,
                    'max': max(sizes) if sizes else None
                }
            
        
        return dataset_characterization_json


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
    data = {'active_tab': 'upload-single-tab'}
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
    
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    data = {
        'active_tab': 'upload-zip-tab',
        'models': EXAMPLE_MODELS
    }

    zip_file = request.files.get('inputZip')

    if not zip_file or not zip_file.filename.lower().endswith('.zip'):
        data['zip_file_error'] = 'Please upload a valid ZIP file.'
        return render_template('index.html', data=data)

    original_filename = os.path.splitext(zip_file.filename)[0]

    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip_file:
        zip_filename = tmp_zip_file.name
        zip_file.save(zip_filename)

    extract_dir = None

    try:
        extract_dir, extracted_files = extract_zip(zip_filename)

        first_characterization_json = process_files(extracted_files, extract_dir, original_filename)

        if first_characterization_json:
            data['fm_dataset_facts'] = first_characterization_json
            data['fm_dataset_characterization_json_str'] = first_characterization_json
            data['fm_dataset_characterization_str'] = str(first_characterization_json)
        else:
            data['zip_file_error'] = 'No valid UVL files found in the ZIP.'

    except Exception as e:
        data['zip_file_error'] = f'An error occurred while processing the ZIP file: {e}'
        print(e)

    finally:
        try:
            os.remove(zip_filename)
        except OSError as e:
            print(f"Error removing temporary zip file: {e}")

        if extract_dir and os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

    return render_template('index.html', data=data)

# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
