from typing import Optional

from famapy.metamodels.fm_metamodel.models import FeatureModel

from fm_characterization.models.fm_metrics import FMMetric, FMAnalysis


class FMCharacterization:

    def __init__(self, model: FeatureModel, name: str = None):
        self._feature_model = model
        self.name = name
        self._analysis = FMAnalysis(self._feature_model)
        self.set_metadata(name)

    def set_metadata(self, 
                     name: Optional[str] = None,
                     description: Optional[str] = None,
                     author: Optional[str] = None,
                     reference: Optional[str] = None,
                     tags: Optional[list[str]] = None):
        data = []
        data.append(self._analysis.name(name))
        data.append(self._analysis.description(description))
        data.append(self._analysis.author(author))
        data.append(self._analysis.reference(reference))
        data.append(self._analysis.tags(tags))
        self._metadata = data

    def get_metadata(self) -> list[FMMetric]:
        return self._metadata

    def get_metrics(self) -> list[FMMetric]:
        metrics = []
        metrics.append(self._analysis.features())
        metrics.append(self._analysis.abstract_features())
        metrics.append(self._analysis.concrete_features())
        metrics.append(self._analysis.root_feature())
        metrics.append(self._analysis.top_features())
        metrics.append(self._analysis.leaf_features())
        metrics.append(self._analysis.tree_relationships())
        metrics.append(self._analysis.mandatory_features())
        metrics.append(self._analysis.optional_features())
        metrics.append(self._analysis.group_features())
        metrics.append(self._analysis.alternative_groups())
        metrics.append(self._analysis.or_groups())
        metrics.append(self._analysis.mutex_groups())
        metrics.append(self._analysis.cardinality_groups())
        metrics.append(self._analysis.max_depth_tree())
        metrics.append(self._analysis.avg_branching_factor())
        metrics.append(self._analysis.avg_children_per_feature())
        metrics.append(self._analysis.min_children_per_feature())
        metrics.append(self._analysis.max_children_per_feature())
        metrics.append(self._analysis.cross_tree_constraints())
        metrics.append(self._analysis.simple_constraints())
        metrics.append(self._analysis.requires_constraints())
        metrics.append(self._analysis.excludes_constraints())
        metrics.append(self._analysis.complex_constraints())
        metrics.append(self._analysis.pseudocomplex_constraints())
        metrics.append(self._analysis.strictcomplex_constraints())
        return metrics


    # def get_metrics2(self) -> dict[FMProperties, Any]:
    #     metrics = FMMetrics(self._feature_model)
    #     data = {}
    #     data[FMProperties.FEATURES] = metrics.nof_features()
    #     data[FMProperties.ABSTRACT_FEATURES] = metrics.nof_abstract_features()
    #     data[FMProperties.CONCRETE_FEATURES] = metrics.nof_concrete_features()
    #     data[FMProperties.TOP_FEATURES] = metrics.nof_top_features()
    #     data[FMProperties.TREE_RELATIONSHIPS] = metrics.nof_tree_relationships()
    #     data[FMProperties.MANDATORY_FEATURES] = metrics.nof_mandatory_features()
    #     data[FMProperties.OPTIONAL_FEATURES] = metrics.nof_optional_features()
    #     data[FMProperties.GROUP_FEATURES] = metrics.nof_group_features()
    #     data[FMProperties.ALTERNATIVE_GROUPS] = metrics.nof_alternative_groups()
    #     data[FMProperties.OR_GROUPS] = metrics.nof_or_groups()
    #     data[FMProperties.MUTEX_GROUPS] = metrics.nof_mutex_groups()
    #     data[FMProperties.CARDINALITY_GROUPS] = metrics.nof_cardinality_groups()
        
    #     data[FMProperties.BRANCHING_FACTOR] = metrics.avg_branching_factor()
    #     data[FMProperties.MIN_CHILDREN_PER_FEATURE] = metrics.min_children_per_feature()
    #     data[FMProperties.MAX_CHILDREN_PER_FEATURE] = metrics.max_children_per_feature()
    #     data[FMProperties.AVG_CHILDREN_PER_FEATURE] = metrics.avg_children_per_feature()
    #     data[FMProperties.LEAF_FEATURES] = metrics.nof_leaf_features()
    #     data[FMProperties.MAX_DEPTH_TREE] = metrics.max_depth_tree()

    #     data[FMProperties.CROSS_TREE_CONSTRAINTS] = metrics.nof_cross_tree_constraints()
    #     data[FMProperties.SIMPLE_CONSTRAINTS] = metrics.nof_simple_constraints()
    #     data[FMProperties.REQUIRES_CONSTRAINTS] = metrics.nof_requires_constraints()
    #     data[FMProperties.EXCLUDES_CONSTRAINTS] = metrics.nof_excludes_constraints()
    #     data[FMProperties.COMPLEX_CONSTRAINTS] = metrics.nof_complex_constraints()
    #     data[FMProperties.PSEUDO_COMPLEX_CONSTRAINTS] = metrics.nof_pseudocomplex_constraints()
    #     data[FMProperties.STRICT_COMPLEX_CONSTRAINTS] = metrics.nof_strictcomplex_constraints()
       
    #     return data

    # def get_analysis(self) -> dict[FMProperties, Any]:
    #     analysis = FMAnalysis(self._feature_model)
    #     data = {}
    #     data[FMProperties.VALID] = analysis.valid_fm()
    #     data[FMProperties.CORE_FEATURES] = analysis.nof_core_features()
    #     data[FMProperties.VARIANT_FEATURES] = analysis.nof_variant_features()
    #     data[FMProperties.DEAD_FEATURES] = analysis.nof_dead_features()
    #     data[FMProperties.FALSE_OPTIONAL_FEATURES] = analysis.nof_false_optional_features()
    #     data[FMProperties.ATOMIC_SETS] = analysis.nof_atomic_sets()
    #     data[FMProperties.CONFIGURATIONS] = utils.get_nof_configuration_as_str(analysis.count_configurations(), analysis.bdd_model is None, self.metrics[FMProperties.CROSS_TREE_CONSTRAINTS])
    #     return data