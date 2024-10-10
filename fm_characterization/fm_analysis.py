from typing import Optional, Any

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
            self._pd = bdd_operations.BDDProductDistribution().execute(self.bdd_model).get_result()
            self._descriptive_statistics = descriptive_statistics(self._pd)
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
            self._fip = None
            self._descriptive_statistics = None

    def get_analysis(self) -> list[FMPropertyMeasure]:
        result = []
        result.append(self.fm_valid())
        result.append(self.fm_core_features())
        result.append(self.fm_false_optional_features())
        result.append(self.fm_dead_features())
        result.append(self.fm_variant_features())
        if self.bdd_model is not None:
            result.append(self.fm_unique_features())
        if self._fip is not None:
            result.append(self.fm_pure_optional_features())
        result.append(self.fm_configurations_number())
        result.append(self.fm_total_variability())
        result.append(self.fm_partial_variability())
        if self.bdd_model is not None:
            result.append(self.fm_homogeneity())
        if self._descriptive_statistics is not None:
            result.append(self.fm_product_distribution())
            result.append(self.fm_mean_pd())
            result.append(self.fm_std_pd())
            result.append(self.fm_median_pd())
            result.append(self.fm_mad_pd())
            result.append(self.fm_mode_pd())
            result.append(self.fm_min_pd())
            result.append(self.fm_max_pd())
            result.append(self.fm_range_pd())
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
        _unique_features = bdd_operations.BDDUniqueFeatures().execute(self.bdd_model).get_result()
        return FMPropertyMeasure(FMProperties.UNIQUE_FEATURES.value, 
                                 _unique_features, 
                                 len(_unique_features),
                                 get_ratio(_unique_features, self._features))
    
    def fm_pure_optional_features(self) -> FMPropertyMeasure:
        _pure_optional_features = [feat for feat, prob, in self._fip.items() if prob == 0.5]
        return FMPropertyMeasure(FMProperties.PURE_OPTIONAL_FEATURES.value, 
                                 _pure_optional_features, 
                                 len(_pure_optional_features),
                                 get_ratio(_pure_optional_features, self._features))

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
        _total_variability_res = round(_total_variability * 100, 2)
        _total_variability_str = str(_total_variability_res) if _total_variability_res > 0 else '{:.2e}'.format(_total_variability * 100)
        #_total_variability = get_percentage_str(_total_variability, 2) + "%"
        return FMPropertyMeasure(FMProperties.TOTAL_VARIABILITY.value, _total_variability)
    
    def fm_partial_variability(self) -> FMPropertyMeasure:
        _partial_variability = self._configurations / (2 ** len(self._variant_features) - 1)
        _partial_variability = get_percentage_str(_partial_variability, 2) + "%"
        return FMPropertyMeasure(FMProperties.PARTIAL_VARIABILITY.value, _partial_variability)
    
    def fm_homogeneity(self) -> FMPropertyMeasure:
        _homogeneity = bdd_operations.BDDHomogeneity().execute(self.bdd_model).get_result()
        _homogeneity = get_percentage_str(_homogeneity, 2) + "%"
        return FMPropertyMeasure(FMProperties.HOMOGENEITY.value, _homogeneity)

    def fm_product_distribution(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PRODUCT_DISTRIBUTION.value, None)

    def fm_mean_pd(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PD_MEAN.value, self._descriptive_statistics['Mean'])
    
    def fm_std_pd(self) -> FMPropertyMeasure:
        _std_pd = round(self._descriptive_statistics['Standard deviation'], 2)
        return FMPropertyMeasure(FMProperties.PD_STD.value, _std_pd)
    
    def fm_median_pd(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PD_MEDIAN.value, self._descriptive_statistics['Median'])
    
    def fm_mad_pd(self) -> FMPropertyMeasure:
        _mad_pd = round(self._descriptive_statistics['Median absolute deviation'], 2)
        return FMPropertyMeasure(FMProperties.PD_MAD.value, _mad_pd)
    
    def fm_mode_pd(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PD_MODE.value, self._descriptive_statistics['Mode'])
    
    def fm_min_pd(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PD_MIN.value, self._descriptive_statistics['Min'])
    
    def fm_max_pd(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PD_MAX.value, self._descriptive_statistics['Max'])
    
    def fm_range_pd(self) -> FMPropertyMeasure:
        return FMPropertyMeasure(FMProperties.PD_RANGE.value, self._descriptive_statistics['Range'])


def descriptive_statistics(prod_dist: list[int]) -> dict[str, Any]: # noqa: MC0001
    total_elements = sum(prod_dist)
    if total_elements == 0:
        return {
            'Mean': 0,
            'Standard deviation': 0,
            'Median': 0,
            'Median absolute deviation': 0,
            'Mode': 0,
            'Min': None,
            'Max': None,
            'Range': 0
        }

    total_sum = 0
    running_total = 0
    median1: Optional[float] = None
    median2: Optional[float] = None
    median_pos1 = (total_elements + 1) // 2
    median_pos2 = (total_elements + 2) // 2
    min_val = None
    max_val = None
    mode = None

    sum_squared_diff = 0
    abs_deviation_total = 0.0
    abs_deviation_running_total = 0
    mad1: Optional[float] = None
    mad2: Optional[float] = None
    mad_pos1 = (total_elements + 1) // 2
    mad_pos2 = (total_elements + 2) // 2

    for i, count in enumerate(prod_dist):
        if count > 0:
            if min_val is None:
                min_val = i
            max_val = i

            total_sum += i * count
            running_total += count

            if mode is None:
                mode = i

            if median1 is None and running_total >= median_pos1:
                median1 = i
            if median2 is None and running_total >= median_pos2:
                median2 = i

    mean = total_sum // total_elements
    median = (median1 + median2) // 2 if median1 is not None and median2 is not None else 0

    running_total = 0
    for i, count in enumerate(prod_dist):
        if count > 0:
            deviation = abs(i - median)
            abs_deviation_total += deviation * count
            running_total += count

            sum_squared_diff += count * (i - mean) ** 2

            abs_deviation_running_total += count
            if mad1 is None and abs_deviation_running_total >= mad_pos1:
                mad1 = deviation
            if mad2 is None and abs_deviation_running_total >= mad_pos2:
                mad2 = deviation
            if mad1 is not None and mad2 is not None:
                break

    std_dev = (sum_squared_diff / total_elements) ** 0.5
    mad = (mad1 + mad2) / 2 if mad1 is not None and mad2 is not None else 0

    statistics = {
        'Mean': mean,
        'Standard deviation': std_dev,
        'Median': median,
        'Median absolute deviation': mad,
        'Mode': mode,
        'Min': min_val,
        'Max': max_val,
        'Range': max_val - min_val if min_val is not None and max_val is not None else 0
    }
    return statistics