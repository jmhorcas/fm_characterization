from typing import Any
from enum import Enum

from famapy.metamodels.fm_metamodel.models import FeatureModel

from fm_characterization.models.fm_metrics import FMMetrics
from fm_characterization.models.fm_analysis import FMAnalysis


class FMProperties(Enum):
    FEATURES = 'Features'
    CROSS_TREE_CONSTRAINTS = 'Cross-tree constraints'
    SIMPLE_CONSTRAINTS = 'Simple constraints'  # Requires and excludes
    ADVANCED_CONSTRAINTS = 'Advanced constraints'  # Prop logic constraints
    MAX_CONSTRAINTS_PER_FEATURE = 'Max constraints per feature'
    AVG_CONSTRAINTS_PER_FEATURE = 'Avg constraints per feature'
    GROUP_FEATURES = 'Group features'
    ALTERNATIVE_GROUPS = 'Alternative groups'
    OR_GROUPS = 'Or groups'
    CARDINALITY_GROUPS = 'Cardinality groups'
    MUTEX_GROUPS = 'Mutex groups'
    ABSTRACT_FEATURES = 'Abstract features'
    MANDATORY_FEATURES = 'Mandatory features'
    OPTIONAL_FEATURES = 'Optional features'
    LEAF_FEATURES = 'Leaf features'
    MAX_DEPTH_TREE = 'Max depth tree'
    BRANCHING_FACTOR = 'Branching factor'  # Also 'Avg children per feature'
    MAX_CHILDREN_PER_FEATURES = 'Max children per feature'
    CONFIGURATIONS = 'Configurations'
    VARIANT_FEATURES = 'Variant features'  # Also 'Real optional features'
    CORE_FEATURES = 'Core features'  # Also 'Common features'
    DEAD_FEATURES = 'Dead features'
    FALSE_OPTIONAL_FEATURES = 'False-optional features'
    ATOMIC_SETS = 'Atomic sets'


class FMCharacterization:

    def __init__(self, model: FeatureModel):
        self.feature_model = model
        self.metrics = self._get_metrics()
        self.analysis = self._get_analysis()

    def _get_metrics(self) -> dict[FMProperties, Any]:
        metrics = FMMetrics(self.feature_model)
        data = {}
        data[FMProperties.FEATURES] = metrics.nof_features()
        data[FMProperties.CROSS_TREE_CONSTRAINTS] = metrics.nof_cross_tree_constraints()
        data[FMProperties.GROUP_FEATURES] = metrics.nof_group_features()
        data[FMProperties.ALTERNATIVE_GROUPS] = metrics.nof_alternative_groups()
        data[FMProperties.OR_GROUPS] = metrics.nof_or_groups()
        data[FMProperties.ABSTRACT_FEATURES] = metrics.nof_abstract_features()
        data[FMProperties.LEAF_FEATURES] = metrics.nof_leaf_features()
        data[FMProperties.BRANCHING_FACTOR] = metrics.avg_branching_factor()
        data[FMProperties.MAX_DEPTH_TREE] = metrics.max_depth_tree()
        return data

    def _get_analysis(self) -> dict[FMProperties, Any]:
        analysis = FMAnalysis(self.feature_model)
        data = {}
        data[FMProperties.CONFIGURATIONS] = analysis.count_configurations()
        data[FMProperties.CORE_FEATURES] = analysis.nof_core_features()
        data[FMProperties.DEAD_FEATURES] = analysis.nof_dead_features()
        data[FMProperties.FALSE_OPTIONAL_FEATURES] = analysis.nof_false_optional_features()
        return data