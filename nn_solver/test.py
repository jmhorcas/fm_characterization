import os
import argparse
import time 

import fm_generator


if __name__ == "__main__":
    fms = fm_generator.generate_all_feature_models(n_features=6, generate_constraints=True)
    #print([str(fm) for fm in fms])
    print(len(fms))
    