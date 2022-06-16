import os
from nn_solver import fm_generator
from fm_characterization import FMCharacterization


CSV_FILE = 'label.csv'
MAX_FEATURES_WITH_CONSTRAINTS = 10
MAX_FEATURES_WITHOUT_CONSTRAINTS = 4


def generate_feature_models(n_features: int, generate_constraints: bool):
    fms = fm_generator.generate_all_feature_models(n_features=n_features, generate_constraints=generate_constraints)
    print(f'#Features: {n_features}')
    print(f'#FMs: {len(fms)}')

    header = []
    labels = set()
    for fm in fms:
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
                with open(CSV_FILE, 'a+') as file:    
                    file.write(f'{header}\n')

    print(f'#Labels: {len(labels)}')
    with open(CSV_FILE, 'a+') as file:    
        for l in labels:
            file.write(f'{l}\n')
    print('----------')

if __name__ == "__main__":
    #for n_features in range(1, MAX_FEATURES_WITH_CONSTRAINTS + 1):
    #    generate_feature_models(n_features, generate_constraints=False)
    for n_features in range(1, MAX_FEATURES_WITHOUT_CONSTRAINTS + 1):
        generate_feature_models(n_features, generate_constraints=True)
    
    