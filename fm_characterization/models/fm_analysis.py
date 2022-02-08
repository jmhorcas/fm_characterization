
from famapy.metamodels.fm_metamodel.models import FeatureModel

# from famapy.metamodels.fm_metamodel.operations import (
#     get_core_features, 
#     count_configurations
# )

from famapy.metamodels.pysat_metamodel.operations.glucose3_products_number import Glucose3ProductsNumber
from famapy.metamodels.pysat_metamodel.operations.glucose3_valid import Glucose3Valid
from famapy.metamodels.pysat_metamodel.operations.glucose3_core_features import Glucose3CoreFeatures
from famapy.metamodels.pysat_metamodel.operations.glucose3_dead_features import Glucose3DeadFeatures
from famapy.metamodels.pysat_metamodel.operations.glucose3_false_optional_features import Glucose3FalseOptionalFeatures


class FMAnalysis():

    def __init__(self, model: FeatureModel):
        self.fm = model

    def nof_core_features(self) -> int:
        return len(Glucose3CoreFeatures().execute(self.fm).get_result())
        #return len(get_core_features(self.feature_model))

    def count_configurations(self) -> int:
        return Glucose3ProductsNumber().execute(self.fm).get_result()
        #return count_configurations(self.feature_model)

    def nof_dead_features(self) -> int:
        return len(Glucose3DeadFeatures().execute(self.fm).get_result())

    def nof_false_optional_features(self) -> int:
        return Glucose3FalseOptionalFeatures().execute(self.fm).get_result()
