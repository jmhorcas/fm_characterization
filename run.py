import os
import shutil
import tempfile
import json
from zipfile import ZipFile
from typing import Tuple

from flask import Flask, render_template, request

from fm_characterization import FMCharacterization, models_info
from fm_characterization.process_files import process_files, read_fm_file, calculate_percentiles, classify_value

STATIC_DIR = 'web'
EXAMPLE_MODELS_DIR = 'fm_models'

app = Flask(__name__,
            static_url_path='',
            static_folder=STATIC_DIR,
            template_folder=STATIC_DIR)


def extract_zip(zip_path: str) -> Tuple[str, list]:
    extract_dir = tempfile.mkdtemp()
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        extracted_files = zip_ref.namelist()
    return extract_dir, extracted_files

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
        zip_file = request.files.get('inputZipThreshold')
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
            
            if zip_file and zip_file.filename.endswith('.zip'):
                extract_dir = None
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip_file:
                        zip_file.save(tmp_zip_file.name)
                        extract_dir, extracted_files = extract_zip(tmp_zip_file.name)
                        
                        uvl_files = [f for f in extracted_files if f.endswith('.uvl')]
                        if not uvl_files:
                            data['zip_threshold_error'] = 'No valid UVL files found in the Threshold ZIP.'
                            shutil.rmtree(extract_dir)
                            return render_template('index.html', data=data)
                        
                        metrics_data, analysis_data, dataset_characterization_json = process_files(uvl_files, extract_dir, zip_file.filename)
                        if dataset_characterization_json:
                            thresholds = {}
                            for metric in dataset_characterization_json['metrics']:
                                name = metric['name']
                                if name in metrics_data:
                                    values = metrics_data[name]['values']
                                if values:
                                    thresholds[name] = calculate_percentiles(values)
                            for analysis in dataset_characterization_json['analysis']:
                                name = analysis['name']
                                if name in analysis_data:
                                    values = analysis_data[name]['values']
                                    clean_values = []
                                    for v in values:
                                        if isinstance(v, str) and '≤' in v:
                                            clean_values.append(float(v.replace('≤', '').strip()))
                                        elif isinstance(v, (int, float)):
                                            clean_values.append(v)
                                    if clean_values:
                                        thresholds[name] = calculate_percentiles(clean_values)
                        shutil.rmtree(extract_dir)
                finally:
                    if extract_dir and os.path.exists(extract_dir):
                        shutil.rmtree(extract_dir)
                    if os.path.exists(tmp_zip_file.name):
                        os.remove(tmp_zip_file.name)

            #json_characterization = interfaces.to_json(fm_characterization, FM_FACT_JSON_FILE)
            json_characterization = characterization.to_json()
            if zip_file and zip_file.filename.endswith('.zip'):
                for metric in json_characterization['metrics']:
                    name = metric['name']
                    if name in thresholds:
                        percentil_33 = thresholds[name]['percentil_33']
                        percentil_66 = thresholds[name]['percentil_66']
                        value = None
                        if metric['size'] is not None:
                            value = metric['size']
                        elif metric['value'] is not None:
                            value = metric['value']
                        if value is not None:
                            metric['threshold'] = classify_value(value, percentil_33, percentil_66)
                for analysis in json_characterization['analysis']:
                    name = analysis['name']
                    if name in thresholds:
                        percentil_33 = thresholds[name]['percentil_33']
                        percentil_66 = thresholds[name]['percentil_66']
                        value = None
                        if analysis['size'] is not None:
                            value = analysis['size']
                        elif analysis['value'] is not None:
                            value = analysis['value']
                        if value is not None:
                            if isinstance(value, str) and '≤' in value:
                                value = float(value.replace('≤', '').strip())
                            analysis['threshold'] = classify_value(value, percentil_33, percentil_66)

                
            json_str_characterization = characterization.to_json_str()
            str_characterization = str(characterization)
            data['fm_facts'] = json_characterization
            data['fm_characterization_json_str'] = json_str_characterization
            data['fm_characterization_str'] = str_characterization
        except Exception as e:
            data = None
            print(e)
            raise e
        finally:
            if os.path.exists(filename) and filename == fm_file.filename:
                os.remove(filename)
        
        if os.path.exists(filename) and filename == fm_file.filename:
            os.remove(filename)

        return render_template('index.html', data=data)

@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    data = {'active_tab': 'upload-zip-tab', 'models': EXAMPLE_MODELS}

    zip_file = request.files.get('inputZip')
    if not zip_file or not zip_file.filename.lower().endswith('.zip'):
        data['zip_file_error'] = 'Please upload a valid ZIP file.'
        return render_template('index.html', data=data)

    zip_name = os.path.splitext(zip_file.filename)[0]

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip_file:
            zip_file.save(tmp_zip_file.name)
            extract_dir, extracted_files = extract_zip(tmp_zip_file.name)

        _, _, dataset_characterization_json = process_files(extracted_files, extract_dir, zip_name)
        if dataset_characterization_json:
            dataset_characterization_json_str = json.dumps(dataset_characterization_json, ensure_ascii=False)

            data.update({
                'fm_dataset_facts': dataset_characterization_json,
                'fm_dataset_characterization_json_str': dataset_characterization_json_str,
                'fm_dataset_characterization_str': dataset_characterization_json_str
            })
        else:
            data['zip_file_error'] = 'No valid UVL files found in the ZIP.'

    except Exception as e:
        data['zip_file_error'] = f'An error occurred while processing the ZIP file: {e}'
        print(e)

    finally:
        cleanup_files([tmp_zip_file.name, extract_dir])

    return render_template('index.html', data=data)


def cleanup_files(paths):
    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
        except OSError as e:
            print(f"Error removing temporary file or directory: {e}")
            
# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
