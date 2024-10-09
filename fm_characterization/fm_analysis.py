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
        self.bdd_model = None
        self.sat_model = FmToPysat(model).transform()
        self.sat_model.original_model = self.fm
        try:
            self.bdd_model = FmToBDD(model).transform()
        except Exception as e:
            print(f'Warning: the feature model is too large to build the BDD model. (Exception: {e})')

        # For performance purposes
        self._features = self.fm.get_features()
        
        if self.bdd_model is not None:
            self._configurations = bdd_operations.BDDConfigurationsNumber().execute(self.bdd_model).get_result()
            self._approximation = False
            self._fip = bdd_operations.BDDFeatureInclusionProbability().execute(self.bdd_model).get_result()
            self._core_features = [feat for feat, prob, in self._fip.items() if prob >= 1.0]
            self._dead_features = [feat for feat, prob, in self._fip.items() if prob <= 0.0]
            self._variant_features = [feat for feat, prob, in self._fip.items() if 0.0 < prob < 1.0]
        else:
            self._configurations = fm_operations.FMEstimatedConfigurationsNumber().execute(self.fm).get_result()
            self._approximation = True
            self._core_features = sat_operations.PySATCoreFeatures().execute(self.sat_model).get_result()
            self._dead_features = sat_operations.PySATDeadFeatures().execute(self.sat_model).get_result()
            self._variant_features = [f.name for f in self._features 
                                      if f.name not in self._core_features and
                                      f.name not in self._dead_features]


    def get_analysis(self) -> list[FMPropertyMeasure]:
        result = []
        result.append(self.fm_valid())
        result.append(self.fm_core_features())
        result.append(self.fm_dead_features())
        result.append(self.fm_variant_features())
        result.append(self.fm_unique_features())
        result.append(self.fm_pure_optional_features())
        result.append(self.fm_false_optional_features())
        result.append(self.fm_configurations_number())
        result.append(self.fm_total_variability())
        result.append(self.fm_partial_variability())
        result.append(self.fm_homogeneity())
        return result

    def fm_valid(self) -> FMPropertyMeasure:
        if self.bdd_model is not None:
            _valid = self._configurations > 0
        else:
            _valid = sat_operations.PySATSatisfiable().execute(self.sat_model).get_result()
        _result = 'Yes' if _valid else 'No'
        return FMPropertyMeasure(FMProperties.VALID.value, _result)

    def fm_core_features(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.CORE_FEATURES.value,
                                 self._core_features, 
                                 len(self._core_features),
                                 get_ratio(self._core_features, self._features))

    def fm_dead_features(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.DEAD_FEATURES.value, 
                                 self._dead_features, 
                                 len(self._dead_features),
                                 get_ratio(self._dead_features, self._features))

    def fm_variant_features(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.VARIANT_FEATURES.value, 
                        self._variant_features, 
                        len(self._variant_features),
                        get_ratio(self._variant_features, self._features))
    
    def fm_unique_features(self) -> FMPropertyMeasure:
        if self.bdd_model is not None:
            _unique_features = bdd_operations.BDDUniqueFeatures().execute(self.bdd_model).get_result()
            _size = len(_unique_features)
            _ratio = get_ratio(_unique_features, self._features)
        else:
            _unique_features = '?'
            _size = None
            _ratio = None
        return FMPropertyMeasure(FMProperties.UNIQUE_FEATURES.value, 
                                 _unique_features, 
                                 _size,
                                 _ratio)
    
    def fm_pure_optional_features(self) -> FMPropertyMeasure:
        if self.bdd_model is not None:
            _pure_optional_features = [feat for feat, prob, in self._fip.items() if prob == 0.5]
            _size = len(_pure_optional_features)
            _ratio = get_ratio(_pure_optional_features, self._features)
        else:
            _pure_optional_features = '?'
            _size = None
            _ratio = None
        return FMPropertyMeasure(FMProperties.PURE_OPTIONAL_FEATURES.value, 
                                 _pure_optional_features, 
                                 _size,
                                 _ratio)

    def fm_false_optional_features(self) -> FMPropertyMeasure:
        if self.bdd_model is not None:
            _false_optional_features = [feat for feat in self._core_features 
                                        if not self.fm.get_feature_by_name(feat).is_root() and 
                                        not self.fm.get_feature_by_name(feat).is_mandatory()]
        else:
            _false_optional_features = sat_operations.PySATFalseOptionalFeatures().execute(self.sat_model).get_result()
        return FMPropertyMeasure(FMProperties.FALSE_OPTIONAL_FEATURES.value, 
                                 _false_optional_features, 
                                 len(_false_optional_features),
                                 get_ratio(_false_optional_features, self._features))

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
    
    def fm_homogeneity(self) -> FMPropertyMeasure:
        if self.bdd_model is not None:
            _homogeneity = bdd_operations.BDDHomogeneity().execute(self.bdd_model).get_result()
            _homogeneity = get_percentage_str(_homogeneity, 2) + "%"
        else:
            _homogeneity = '?'
        return FMPropertyMeasure(FMProperties.HOMOGENEITY.value, _homogeneity)
