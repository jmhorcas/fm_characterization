from fm_characterization import FMProperties, FMPropertyMeasure
from .fm_utils import get_ratio, get_nof_configuration_as_str, get_percentage_str

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.pysat_metamodel.transformations.fm_to_pysat import FmToPysat
from flamapy.metamodels.bdd_metamodel.transformations.fm_to_bdd import FmToBDD
from flamapy.metamodels.pysat_metamodel import operations as sat_operations
from flamapy.metamodels.bdd_metamodel import operations as bdd_operations
from flamapy.metamodels.fm_metamodel import operations as fm_operations


class FMAnalysis():

    def __init__(self, model: FeatureModel):
        self.fm = model
        self.sat_model = FmToPysat(model).transform()
        try:
            self.bdd_model = FmToBDD(model).transform()
        except Exception as e:
            print(f'Warning: the feature model is too large to build the BDD model. (Exception: {e})')
            self.bdd_model = None

        # For performance purposes
        self._features = self.fm.get_features()
        self._common_features = sat_operations.PySATCoreFeatures().execute(self.sat_model).get_result()
        self._dead_features = sat_operations.PySATDeadFeatures().execute(self.sat_model).get_result()
        self._variant_features = [f.name for f in self._features 
                                  if f.name not in self._common_features and
                                  f.name not in self._dead_features]
        
        if self.bdd_model is not None:
            self._configurations = bdd_operations.BDDConfigurationsNumber().execute(self.bdd_model).get_result()
            self._approximation = False
        else:
            self._configurations = fm_operations.FMEstimatedConfigurationsNumber().execute(self.fm).get_result()
            self._approximation = True


    def get_analysis(self) -> list[FMPropertyMeasure]:
        result = []
        result.append(self.fm_valid())
        result.append(self.fm_core_features())
        result.append(self.fm_dead_features())
        result.append(self.fm_variant_features())
        result.append(self.fm_false_optional_features())
        result.append(self.fm_configurations_number())
        result.append(self.fm_total_variability())
        result.append(self.fm_partial_variability())
        return result

    def fm_valid(self) -> FMPropertyMeasure:
        _valid = sat_operations.PySATSatisfiable().execute(self.sat_model).get_result()
        _result = 'Yes' if _valid else 'No'
        return FMPropertyMeasure(FMProperties.VALID.value, _result)

    def fm_core_features(self) -> FMPropertyMeasure:
        _core_features = self._common_features
        return FMPropertyMeasure(FMProperties.CORE_FEATURES.value, 
                        _core_features, 
                        len(_core_features),
                        get_ratio(_core_features, self._features))

    def fm_dead_features(self) -> FMPropertyMeasure:
        _dead_features = self._dead_features
        return FMPropertyMeasure(FMProperties.DEAD_FEATURES.value, 
                        _dead_features, 
                        len(_dead_features),
                        get_ratio(_dead_features, self._features))

    def fm_variant_features(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.VARIANT_FEATURES.value, 
                        self._variant_features, 
                        len(self._variant_features),
                        get_ratio(self._variant_features, self._features))

    def fm_false_optional_features(self) -> FMPropertyMeasure:
        _false_optional_features = sat_operations.PySATFalseOptionalFeatures().execute(self.sat_model).get_result()
        return FMPropertyMeasure(FMProperties.FALSE_OPTIONAL_FEATURES.value, 
                        _false_optional_features, 
                        len(_false_optional_features),
                        get_ratio(_false_optional_features, self.fm.get_features()))

    def fm_configurations_number(self) -> FMPropertyMeasure:
        _configurations = get_nof_configuration_as_str(self._configurations, self._approximation, len(self.fm.get_constraints()))
        return FMPropertyMeasure(FMProperties.CONFIGURATIONS.value, _configurations)
    
    def fm_total_variability(self) -> FMPropertyMeasure:
        _total_variability = self._configurations / (2 ** len(self._features) - 1)
        _total_variability = get_percentage_str(_total_variability, 2) + "%"
        return FMPropertyMeasure(FMProperties.TOTAL_VARIABILITY.value, _total_variability)
    
    def fm_partial_variability(self) -> FMPropertyMeasure:
        _partial_variability = self._configurations / (2 ** len(self._variant_features) - 1)
        _partial_variability = get_percentage_str(_partial_variability, 2) + "%"
        return FMPropertyMeasure(FMProperties.PARTIAL_VARIABILITY.value, _partial_variability)