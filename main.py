import os
import argparse

from famapy.metamodels.fm_metamodel.transformations.featureide_reader import FeatureIDEReader
from famapy.metamodels.fm_metamodel.transformations.uvl_reader import UVLReader

from fm_characterization.models.fm_characterization import FMCharacterization
from fm_characterization.models import interfaces


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Characterization of feature models.')
    parser.add_argument('feature_model', type=str, help='Feature model.')
    args = parser.parse_args()


    fm = FeatureIDEReader(args.feature_model).transform() 
    #fm = UVLReader(args.feature_model).transform() 
    fm_characterization = FMCharacterization(fm)

    # print(f'METRICS')
    # for property, value in fm_characterization.metrics.items():
    #     print(f'  {property.value}: {value}')
    
    # print(f'ANALYSIS')
    # for property, value in fm_characterization.analysis.items():
    #     print(f'  {property.value}: {value}')

    print(os.path.splitext(os.path.basename(args.feature_model))[0])
    string = interfaces.get_string_output(fm_characterization)
    print(string)

    #print(fm)