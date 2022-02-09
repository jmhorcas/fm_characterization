
from famapy.metamodels.fm_metamodel.models import FeatureModel
from famapy.metamodels.pysat_metamodel.transformations.fm_to_pysat import FmToPysat
from famapy.metamodels.bdd_metamodel.transformations.fm_to_bdd import FmToBDD
from famapy.metamodels.pysat_metamodel.operations.glucose3_products_number import Glucose3ProductsNumber
from famapy.metamodels.pysat_metamodel.operations.glucose3_core_features import Glucose3CoreFeatures
from famapy.metamodels.pysat_metamodel.operations.glucose3_dead_features import Glucose3DeadFeatures
from famapy.metamodels.pysat_metamodel.operations.glucose3_false_optional_features import Glucose3FalseOptionalFeatures
from famapy.metamodels.bdd_metamodel.operations.bdd_products_number import BDDProductsNumber
from famapy.metamodels.fm_metamodel.operations.fm_estimated_products_number import FMEstimatedProductsNumber


class FMAnalysis():

    def __init__(self, model: FeatureModel):
        self.fm = model
        self.sat_model = FmToPysat(model).transform()
        try:
            self.bdd_model = FmToBDD(model).transform()
        except Exception as e:
            print(f'Warning: the feature model is too large to build the BDD model.')
            self.bdd_model = None

    def nof_core_features(self) -> int:
        return len(Glucose3CoreFeatures().execute(self.sat_model).get_result())
    
    def nof_variant_features(self) -> int:
        return len(self.fm.get_features()) - self.nof_core_features() - self.nof_dead_features()

    def count_configurations(self) -> int:
        if self.bdd_model is not None:
            return BDDProductsNumber().execute(self.bdd_model).get_result()
        else:
            return FMEstimatedProductsNumber().execute(self.fm).get_result()

    def nof_dead_features(self) -> int:
        return len(Glucose3DeadFeatures().execute(self.sat_model).get_result())

    def nof_false_optional_features(self) -> int:
        return len(Glucose3FalseOptionalFeatures().execute(self.sat_model).get_result())
