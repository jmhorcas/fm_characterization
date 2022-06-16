import os
from fm_characterization import FMCharacterization
from fm_characterization import models_info
from famapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader


CSV_FILE = 'real_labels.csv'
REAL_MODELS_PATH = 'nn_solver/real_models'


def generate_labels_vectors():
    labels = set()
    header = []
    MODELS = [m[models_info.FILENAME] for m in models_info.MODELS]

    for m in MODELS:
        print(f'Feature model: {m}')
        filename = os.path.join(REAL_MODELS_PATH, m)
        
        if filename.endswith(".uvl"):
            fm = UVLReader(filename).transform()
        elif filename.endswith(".xml") or filename.endswith(".fide"):
            fm = FeatureIDEReader(filename).transform()

        characterization = FMCharacterization(fm)
        metrics_vector = [str(measure.size) if measure.size is not None else str(measure.value) for measure in characterization.metrics.get_metrics()]
        analysis_vector = [str(measure.size) if measure.size is not None else str(measure.value) for measure in characterization.analysis.get_analysis()]
        vector = ', '.join(metrics_vector + analysis_vector)
        labels.add(vector)

        if not header:
            header = [measure.property.name for measure in characterization.metrics.get_metrics()]
            header += [measure.property.name for measure in characterization.analysis.get_analysis()]
            header = ', '.join(header)
            if not os.path.exists(CSV_FILE):
                with open(CSV_FILE, 'a+', encoding='utf-8') as file:    
                    file.write(f'{header}\n')

    with open(CSV_FILE, 'a+', encoding='utf-8') as file:    
        for l in labels:
            file.write(f'{l}\n')
    print('----------')

if __name__ == "__main__":
    generate_labels_vectors()
    