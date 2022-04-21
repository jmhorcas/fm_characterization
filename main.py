import os
import argparse
import time 

from famapy.metamodels.fm_metamodel.transformations import FeatureIDEReader
from fm_characterization.models.fm_characterization import FMCharacterization
from fm_characterization.models import interfaces


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Characterization of feature models.')
    parser.add_argument('feature_model', type=str, help='Feature model.')
    args = parser.parse_args()

    fm = FeatureIDEReader(args.feature_model).transform() 
    name = os.path.splitext(os.path.basename(args.feature_model))[0]

    start = time.perf_counter_ns()
    fm_characterization = FMCharacterization(fm, name)

    str_result = interfaces.get_string_output(fm_characterization)
    end = time.perf_counter_ns()
    print(str_result)
    interfaces.to_json(fm_characterization, 'metrics.json')

    print(f'Time: {(end-start) * 1e-6} ms')
    