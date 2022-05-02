from fm_characterization import FMProperties, FMPropertyMeasure
from .fm_utils import get_ratio

from famapy.metamodels.fm_metamodel.models import FeatureModel
from famapy.metamodels.fm_metamodel import operations as fm_operations


class FMMetrics():

    def __init__(self, model: FeatureModel):
        self.fm = model
                     
    def get_metrics(self) -> list[FMPropertyMeasure]:
        result = []
        result.append(self.fm_features())
        result.append(self.fm_abstract_features())
        result.append(self.fm_concrete_features())
        result.append(self.fm_root_feature())
        result.append(self.fm_top_features())
        result.append(self.fm_leaf_features())
        result.append(self.fm_tree_relationships())
        result.append(self.fm_mandatory_features())
        result.append(self.fm_optional_features())
        result.append(self.fm_group_features())
        result.append(self.fm_alternative_groups())
        result.append(self.fm_or_groups())
        result.append(self.fm_mutex_groups())
        result.append(self.fm_cardinality_groups())
        result.append(self.fm_max_depth_tree())
        result.append(self.fm_avg_branching_factor())
        result.append(self.fm_avg_children_per_feature())
        result.append(self.fm_min_children_per_feature())
        result.append(self.fm_max_children_per_feature())
        result.append(self.fm_cross_tree_constraints())
        result.append(self.fm_simple_constraints())
        result.append(self.fm_requires_constraints())
        result.append(self.fm_excludes_constraints())
        result.append(self.fm_complex_constraints())
        result.append(self.fm_pseudocomplex_constraints())
        result.append(self.fm_strictcomplex_constraints())
        return result

    def fm_features(self) -> FMPropertyMeasure:
        _features = [f.name for f in self.fm.get_features()]
        return FMPropertyMeasure(FMProperties.FEATURES.value, _features, len(_features))

    def fm_abstract_features(self) -> FMPropertyMeasure:
        _abstract_features = [f.name for f in self.fm.get_features() if f.is_abstract]
        return FMPropertyMeasure(FMProperties.ABSTRACT_FEATURES.value, 
                        _abstract_features, 
                        len(_abstract_features),
                        get_ratio(_abstract_features, self.fm.get_features()))

    def fm_concrete_features(self) -> FMPropertyMeasure:
        _concrete_features = [f.name for f in self.fm.get_features() if not f.is_abstract]
        return FMPropertyMeasure(FMProperties.CONCRETE_FEATURES.value, 
                        _concrete_features, 
                        len(_concrete_features),
                        get_ratio(_concrete_features, self.fm.get_features()))
    
    def fm_root_feature(self) -> FMPropertyMeasure:
        _root_feature = self.fm.root.name
        return FMPropertyMeasure(FMProperties.ROOT_FEATURE.value, 
                        _root_feature)

    def fm_top_features(self) -> FMPropertyMeasure:
        _top_features = [f.name for r in self.fm.root.get_relations() for f in r.children]
        return FMPropertyMeasure(FMProperties.TOP_FEATURES.value, 
                        _top_features, 
                        len(_top_features),
                        get_ratio(_top_features, self.fm.get_features()))

    def fm_leaf_features(self) -> FMPropertyMeasure:
        leaf_features = [f.name for f in self.fm.get_features() if len(f.get_relations()) == 0]
        return FMPropertyMeasure(FMProperties.LEAF_FEATURES.value, 
                        leaf_features, 
                        len(leaf_features),
                        get_ratio(leaf_features, self.fm.get_features()))

    def fm_tree_relationships(self) -> FMPropertyMeasure:
        _tree_relationships = [str(r) for r in self.fm.get_relations()]
        return FMPropertyMeasure(FMProperties.TREE_RELATIONSHIPS.value, 
                        _tree_relationships, 
                        len(_tree_relationships))

    def fm_mandatory_features(self) -> FMPropertyMeasure:
        _tree_relationships = [r for r in self.fm.get_relations()]
        _mandatory_features = [f.name for f in self.fm.get_mandatory_features()]
        return FMPropertyMeasure(FMProperties.MANDATORY_FEATURES.value, 
                        _mandatory_features, 
                        len(_mandatory_features),
                        get_ratio(_mandatory_features, _tree_relationships))

    def fm_optional_features(self) -> FMPropertyMeasure:
        _tree_relationships = [r for r in self.fm.get_relations()]
        _optional_features = [f.name for f in self.fm.get_optional_features()]
        return FMPropertyMeasure(FMProperties.OPTIONAL_FEATURES.value, 
                        _optional_features, 
                        len(_optional_features),
                        get_ratio(_optional_features, _tree_relationships))

    def fm_group_features(self) -> FMPropertyMeasure:
        _tree_relationships = [r for r in self.fm.get_relations()]
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        return FMPropertyMeasure(FMProperties.GROUP_FEATURES.value, 
                        _group_features, 
                        len(_group_features),
                        get_ratio(_group_features, _tree_relationships))
    
    def fm_alternative_groups(self) -> FMPropertyMeasure:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _alternative_groups = [f.name for f in self.fm.get_alternative_group_features()]
        return FMPropertyMeasure(FMProperties.ALTERNATIVE_GROUPS.value, 
                        _alternative_groups, 
                        len(_alternative_groups),
                        get_ratio(_alternative_groups, _group_features))
    
    def fm_or_groups(self) -> FMPropertyMeasure:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _or_groups = [f.name for f in self.fm.get_or_group_features()]
        return FMPropertyMeasure(FMProperties.OR_GROUPS.value, 
                        _or_groups, 
                        len(_or_groups),
                        get_ratio(_or_groups, _group_features))

    def fm_mutex_groups(self) -> FMPropertyMeasure:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _mutex_groups = [f.name for f in self.fm.get_features() if f.is_mutex_group()]
        return FMPropertyMeasure(FMProperties.MUTEX_GROUPS.value, 
                        _mutex_groups, 
                        len(_mutex_groups),
                        get_ratio(_mutex_groups, _group_features))

    def fm_cardinality_groups(self) -> FMPropertyMeasure:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _cardinality_groups = [f.name for f in self.fm.get_features() if f.is_cardinality_group()]
        return FMPropertyMeasure(FMProperties.CARDINALITY_GROUPS.value, 
                        _cardinality_groups, 
                        len(_cardinality_groups),
                        get_ratio(_cardinality_groups, _group_features))
    
    def fm_max_depth_tree(self) -> FMPropertyMeasure:
        _max_depth_tree = fm_operations.max_depth_tree(self.fm)
        return FMPropertyMeasure(FMProperties.MAX_DEPTH_TREE.value, 
                        _max_depth_tree)

    def fm_avg_branching_factor(self) -> FMPropertyMeasure:
        _avg_branching_factor = fm_operations.average_branching_factor(self.fm)
        return FMPropertyMeasure(FMProperties.BRANCHING_FACTOR.value, 
                        _avg_branching_factor)

    def fm_min_children_per_feature(self) -> FMPropertyMeasure:
        _min_children_per_feature = min(sum(len(r.children) for r in feature.get_relations()) for feature in self.fm.get_features() if not feature.is_leaf())
        return FMPropertyMeasure(FMProperties.MIN_CHILDREN_PER_FEATURE.value, 
                        _min_children_per_feature)

    def fm_max_children_per_feature(self) -> FMPropertyMeasure:
        _max_children_per_feature = max(sum(len(r.children) for r in feature.get_relations()) for feature in self.fm.get_features())
        return FMPropertyMeasure(FMProperties.MAX_CHILDREN_PER_FEATURE.value, 
                        _max_children_per_feature)

    def fm_avg_children_per_feature(self) -> FMPropertyMeasure:
        nof_children = sum(len(r.children) for feature in self.fm.get_features() for r in feature.get_relations())
        _avg_children_per_feature = round(nof_children / len(self.fm.get_features()), 2)
        return FMPropertyMeasure(FMProperties.AVG_CHILDREN_PER_FEATURE.value, 
                        _avg_children_per_feature)

    def fm_cross_tree_constraints(self) -> FMPropertyMeasure:
        _cross_tree_constraints = [str(ctc) for ctc in self.fm.get_constraints()]
        return FMPropertyMeasure(FMProperties.CROSS_TREE_CONSTRAINTS.value, 
                        _cross_tree_constraints,
                        len(_cross_tree_constraints))

    def fm_simple_constraints(self) -> FMPropertyMeasure:
        _simple_constraints = [str(ctc) for ctc in self.fm.get_simple_constraints()]
        return FMPropertyMeasure(FMProperties.SIMPLE_CONSTRAINTS.value, 
                        _simple_constraints,
                        len(_simple_constraints),
                        get_ratio(_simple_constraints, self.fm.get_constraints()))

    def fm_requires_constraints(self) -> FMPropertyMeasure:
        _requires_constraints = [str(ctc) for ctc in self.fm.get_requires_constraints()]
        return FMPropertyMeasure(FMProperties.REQUIRES_CONSTRAINTS.value, 
                        _requires_constraints,
                        len(_requires_constraints),
                        get_ratio(_requires_constraints, self.fm.get_simple_constraints()))

    def fm_excludes_constraints(self) -> FMPropertyMeasure:
        _excludes_constraints = [str(ctc) for ctc in self.fm.get_excludes_constraints()]
        return FMPropertyMeasure(FMProperties.EXCLUDES_CONSTRAINTS.value, 
                        _excludes_constraints,
                        len(_excludes_constraints),
                        get_ratio(_excludes_constraints, self.fm.get_simple_constraints()))

    def fm_complex_constraints(self) -> FMPropertyMeasure:
        _complex_constraints = [str(ctc) for ctc in self.fm.get_complex_constraints()]
        return FMPropertyMeasure(FMProperties.COMPLEX_CONSTRAINTS.value, 
                        _complex_constraints,
                        len(_complex_constraints),
                        get_ratio(_complex_constraints, self.fm.get_constraints()))

    def fm_pseudocomplex_constraints(self) -> FMPropertyMeasure:
        _pseudocomplex_constraints = [str(ctc) for ctc in self.fm.get_pseudocomplex_constraints()]
        return FMPropertyMeasure(FMProperties.PSEUDO_COMPLEX_CONSTRAINTS.value, 
                        _pseudocomplex_constraints,
                        len(_pseudocomplex_constraints),
                        get_ratio(_pseudocomplex_constraints, self.fm.get_complex_constraints()))

    def fm_strictcomplex_constraints(self) -> FMPropertyMeasure:
        _strictcomplex_constraints = [str(ctc) for ctc in self.fm.get_strictcomplex_constraints()]
        return FMPropertyMeasure(FMProperties.STRICT_COMPLEX_CONSTRAINTS.value, 
                        _strictcomplex_constraints,
                        len(_strictcomplex_constraints),
                        get_ratio(_strictcomplex_constraints, self.fm.get_complex_constraints()))