from typing import Any
from enum import Enum

from famapy.metamodels.fm_metamodel.models import FeatureModel

from fm_characterization.models.fm_metrics import FMMetrics
from fm_characterization.models.fm_analysis import FMAnalysis
from fm_characterization.models import utils 


class FMProperties(Enum):
    FEATURES = 'Features'
    ABSTRACT_FEATURES = 'Abstract features'
    CONCRETE_FEATURES = 'Concrete features'
    TREE_RELATIONSHIPS = 'Tree relationships'
    MANDATORY_FEATURES = 'Mandatory features'
    OPTIONAL_FEATURES = 'Optional features'
    GROUP_FEATURES = 'Group features'
    ALTERNATIVE_GROUPS = 'Alternative groups'
    OR_GROUPS = 'Or groups'
    #CARDINALITY_GROUPS = 'Cardinality groups'
    #MUTEX_GROUPS = 'Mutex groups'
    BRANCHING_FACTOR = 'Branching factor'  # Also 'Avg children per feature'
    MIN_CHILDREN_PER_FEATURE = 'Min children per non-leaf feature'
    MAX_CHILDREN_PER_FEATURE = 'Max children per feature'
    AVG_CHILDREN_PER_FEATURE = 'Avg children per feature'
    LEAF_FEATURES = 'Leaf features'
    MAX_DEPTH_TREE = 'Max depth tree'

    CROSS_TREE_CONSTRAINTS = 'Cross-tree constraints'
    SIMPLE_CONSTRAINTS = 'Simple constraints'  # Requires and excludes
    REQUIRES_CONSTRAINTS = 'Requires constraints'
    EXCLUDES_CONSTRAINTS = 'Excludes constraints'
    COMPLEX_CONSTRAINTS = 'Complex constraints'  # Prop logic constraints (aka advanced constraints)
    PSEUDO_COMPLEX_CONSTRAINTS = 'Pseudo-complex constraints'
    STRICT_COMPLEX_CONSTRAINTS = 'Strict-complex constraints'
    #MAX_CONSTRAINTS_PER_FEATURE = 'Max constraints per feature'
    #AVG_CONSTRAINTS_PER_FEATURE = 'Avg constraints per feature'

    CORE_FEATURES = 'Core features'  # Also 'Common features'
    VARIANT_FEATURES = 'Variant features'  # Also 'Real optional features'
    DEAD_FEATURES = 'Dead features'
    UNIQUE_FEATURES = 'Unique features'
    FALSE_OPTIONAL_FEATURES = 'False-optional features'
    ATOMIC_SETS = 'Atomic sets'
    CONFIGURATIONS = 'Configurations'

class FMCharacterization:

    def __init__(self, model: FeatureModel):
        self.feature_model = model
        self.metrics = self.get_metrics()
        self.analysis = self.get_analysis()

    def get_metrics(self) -> dict[FMProperties, Any]:
        metrics = FMMetrics(self.feature_model)
        data = {}
        data[FMProperties.FEATURES] = metrics.nof_features()
        data[FMProperties.ABSTRACT_FEATURES] = metrics.nof_abstract_features()
        data[FMProperties.CONCRETE_FEATURES] = metrics.nof_concrete_features()
        data[FMProperties.TREE_RELATIONSHIPS] = metrics.nof_tree_relationships()
        data[FMProperties.MANDATORY_FEATURES] = metrics.nof_mandatory_features()
        data[FMProperties.OPTIONAL_FEATURES] = metrics.nof_optional_features()
        data[FMProperties.GROUP_FEATURES] = metrics.nof_group_features()
        data[FMProperties.ALTERNATIVE_GROUPS] = metrics.nof_alternative_groups()
        data[FMProperties.OR_GROUPS] = metrics.nof_or_groups()
        
        data[FMProperties.BRANCHING_FACTOR] = metrics.avg_branching_factor()
        data[FMProperties.MIN_CHILDREN_PER_FEATURE] = metrics.min_children_per_feature()
        data[FMProperties.MAX_CHILDREN_PER_FEATURE] = metrics.max_children_per_feature()
        data[FMProperties.AVG_CHILDREN_PER_FEATURE] = metrics.avg_children_per_feature()
        data[FMProperties.LEAF_FEATURES] = metrics.nof_leaf_features()
        data[FMProperties.MAX_DEPTH_TREE] = metrics.max_depth_tree()

        data[FMProperties.CROSS_TREE_CONSTRAINTS] = metrics.nof_cross_tree_constraints()
        data[FMProperties.SIMPLE_CONSTRAINTS] = metrics.nof_simple_constraints()
        data[FMProperties.REQUIRES_CONSTRAINTS] = metrics.nof_requires_constraints()
        data[FMProperties.EXCLUDES_CONSTRAINTS] = metrics.nof_excludes_constraints()
        data[FMProperties.COMPLEX_CONSTRAINTS] = metrics.nof_complex_constraints()
        data[FMProperties.PSEUDO_COMPLEX_CONSTRAINTS] = metrics.nof_pseudocomplex_constraints()
        data[FMProperties.STRICT_COMPLEX_CONSTRAINTS] = metrics.nof_strictcomplex_constraints()
       
        return data

    def get_analysis(self) -> dict[FMProperties, Any]:
        analysis = FMAnalysis(self.feature_model)
        data = {}
        data[FMProperties.CORE_FEATURES] = analysis.nof_core_features()
        data[FMProperties.VARIANT_FEATURES] = analysis.nof_variant_features()
        data[FMProperties.DEAD_FEATURES] = analysis.nof_dead_features()
        data[FMProperties.FALSE_OPTIONAL_FEATURES] = analysis.nof_false_optional_features()
        data[FMProperties.CONFIGURATIONS] = utils.get_nof_configuration_as_str(analysis.count_configurations(), analysis.bdd_model is None, self.metrics[FMProperties.CROSS_TREE_CONSTRAINTS])
        return data