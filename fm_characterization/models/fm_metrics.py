from msilib.schema import Property
from multiprocessing.sharedctypes import Value
from typing import Any, Collection, Optional
from enum import Enum

from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature

from famapy.metamodels.fm_metamodel import operations as fm_operations


def get_ratio(collection1: Collection, collection2: Collection, precision: int = 4) -> float:
    if not collection2:
        return 0.0
    return round(len(collection1) / len(collection2), precision)


class FMProperty():

    def __init__(self, 
                 name: str,  
                 description: Optional[str] = None,  
                 parent: Optional['FMProperty'] = None):
        self.name = name
        self.description = description
        self.parent = parent

    def to_dict(self) -> dict[str, Any]:
        return {'name': self.name, 
                'description': self.description,
                'parent': self.parent.name if self.parent is not None else None,
                'level': self.level()}

    def level(self) -> int:
        """Return the level of parents."""
        if self.parent is None:
            return 0
        return 1 + self.parent.level()


class FMProperties(Enum):
    # METADATA
    NAME = FMProperty('Name', 'Name of the feature model.', None)
    DESCRIPTION = FMProperty('Description', 'Description of the feature model.', None)
    AUTHOR = FMProperty('Author', 'Author of the feature model', None)
    REFERENCE = FMProperty('Reference', 'Main paper for reference or DOI of the feature model', None)
    TAGS = FMProperty('Tags', 'Tags or keywords that identify the feature model.', None)

    # METRICS
    FEATURES = FMProperty('Features', "", None)
    ABSTRACT_FEATURES = FMProperty('Abstract features', "", FEATURES)
    CONCRETE_FEATURES = FMProperty('Concrete features', "", FEATURES)
    ROOT_FEATURE = FMProperty('Root feature', 'The root of the feature model.', None)
    TOP_FEATURES = FMProperty('Top features', 'Features that are first descendants of the root.', ROOT_FEATURE)
    TREE_RELATIONSHIPS = FMProperty('Tree relationships', "", None)
    MANDATORY_FEATURES = FMProperty('Mandatory features', "", TREE_RELATIONSHIPS)
    OPTIONAL_FEATURES = FMProperty('Optional features', "", TREE_RELATIONSHIPS)
    GROUP_FEATURES = FMProperty('Group features', "", TREE_RELATIONSHIPS)
    ALTERNATIVE_GROUPS = FMProperty('Alternative groups', "", GROUP_FEATURES)
    OR_GROUPS = FMProperty('Or groups', "", GROUP_FEATURES)
    MUTEX_GROUPS = FMProperty('Mutex groups', "", GROUP_FEATURES)
    CARDINALITY_GROUPS = FMProperty('Cardinality groups', "", GROUP_FEATURES)
    BRANCHING_FACTOR = FMProperty('Branching factor', "", None)  # Also 'Avg children per feature'
    MIN_CHILDREN_PER_FEATURE = FMProperty('Min children per non-leaf feature', "", BRANCHING_FACTOR)
    MAX_CHILDREN_PER_FEATURE = FMProperty('Max children per feature', "", BRANCHING_FACTOR)
    AVG_CHILDREN_PER_FEATURE = FMProperty('Avg children per feature', "", BRANCHING_FACTOR)
    LEAF_FEATURES = FMProperty('Leaf features', "", FEATURES)
    MAX_DEPTH_TREE = FMProperty('Max depth tree', "", None)

    CROSS_TREE_CONSTRAINTS = FMProperty('Cross-tree constraints', "", None)
    SIMPLE_CONSTRAINTS = FMProperty('Simple constraints', 'Requires and Excludes constraints.', CROSS_TREE_CONSTRAINTS)  # Requires and excludes
    REQUIRES_CONSTRAINTS = FMProperty('Requires constraints', "", SIMPLE_CONSTRAINTS)
    EXCLUDES_CONSTRAINTS = FMProperty('Excludes constraints', "", SIMPLE_CONSTRAINTS)
    COMPLEX_CONSTRAINTS = FMProperty('Complex constraints', "", CROSS_TREE_CONSTRAINTS)  # Prop logic constraints (aka advanced constraints)
    PSEUDO_COMPLEX_CONSTRAINTS = FMProperty('Pseudo-complex constraints', "", COMPLEX_CONSTRAINTS)
    STRICT_COMPLEX_CONSTRAINTS = FMProperty('Strict-complex constraints', "", COMPLEX_CONSTRAINTS)
    #MAX_CONSTRAINTS_PER_FEATURE = FMProperty('Max constraints per feature', "", None)
    #AVG_CONSTRAINTS_PER_FEATURE = FMProperty('Avg constraints per feature', "", None)

    #VALID = FMProperty('Valid (not void)', "", None)
    # CORE_FEATURES = 'Core features'  # Also 'Common features'
    # VARIANT_FEATURES = 'Variant features'  # Also 'Real optional features'
    # DEAD_FEATURES = 'Dead features'
    # UNIQUE_FEATURES = 'Unique features'
    # FALSE_OPTIONAL_FEATURES = 'False-optional features'
    # ATOMIC_SETS = 'Atomic sets'
    # CONFIGURATIONS = 'Configurations'


class FMMetric():

    def __init__(self, 
                 property: Property,
                 value: Optional[Any] = None,  # Example: the list of abstract features
                 size: Optional[Any] = None,  # Example: number of abstract features
                 ratio: Optional[Any] = None):  # Example: percentage of abstract features from the total number of features
        self.property = property
        self.value = value
        self.size = size 
        self.ratio = ratio

    def to_dict(self) -> dict[str, Any]:
        result = {'value': self.value,
                  'size': self.size,
                  'ratio': self.ratio}
        return self.property.to_dict() | result


class FMAnalysis():

    def __init__(self, model: FeatureModel):
        self.fm = model
    
    # METADATA
    def name(self, value: Optional[str] = None) -> FMMetric:
        value = value if value is not None else self.fm.root.name 
        return FMMetric(FMProperties.NAME.value, value)
    
    def description(self, value: Optional[str] = None) -> FMMetric:
        if value is None:
            return FMMetric(FMProperties.DESCRIPTION.value)    
        return FMMetric(FMProperties.DESCRIPTION.value, value)

    def author(self, value: Optional[str] = None) -> FMMetric:
        if value is None:
            return FMMetric(FMProperties.AUTHOR.value)    
        return FMMetric(FMProperties.AUTHOR.value, value)
    
    def reference(self, value: Optional[str] = None) -> FMMetric:
        if value is None:
            return FMMetric(FMProperties.REFERENCE.value)    
        return FMMetric(FMProperties.REFERENCE.value, value)

    def tags(self, value: Optional[list[str]] = None) -> FMMetric:
        if value is None:
            return FMMetric(FMProperties.TAGS.value)    
        return FMMetric(FMProperties.TAGS.value, value)

    # METRICS
    def features(self) -> FMMetric:
        _features = [f.name for f in self.fm.get_features()]
        return FMMetric(FMProperties.FEATURES.value, _features, len(_features))

    def abstract_features(self) -> FMMetric:
        _abstract_features = [f.name for f in self.fm.get_features() if f.is_abstract]
        return FMMetric(FMProperties.ABSTRACT_FEATURES.value, 
                        _abstract_features, 
                        len(_abstract_features),
                        get_ratio(_abstract_features, self.fm.get_features()))

    def concrete_features(self) -> FMMetric:
        _concrete_features = [f.name for f in self.fm.get_features() if not f.is_abstract]
        return FMMetric(FMProperties.CONCRETE_FEATURES.value, 
                        _concrete_features, 
                        len(_concrete_features),
                        get_ratio(_concrete_features, self.fm.get_features()))
    
    def root_feature(self) -> FMMetric:
        _root_feature = self.fm.root.name
        return FMMetric(FMProperties.ROOT_FEATURE.value, 
                        _root_feature)

    def top_features(self) -> FMMetric:
        _top_features = [f.name for r in self.fm.root.get_relations() for f in r.children]
        return FMMetric(FMProperties.TOP_FEATURES.value, 
                        _top_features, 
                        len(_top_features),
                        get_ratio(_top_features, self.fm.get_features()))

    def leaf_features(self) -> FMMetric:
        leaf_features = [f.name for f in self.fm.get_features() if len(f.get_relations()) == 0]
        return FMMetric(FMProperties.LEAF_FEATURES.value, 
                        leaf_features, 
                        len(leaf_features),
                        get_ratio(leaf_features, self.fm.get_features()))

    def tree_relationships(self) -> FMMetric:
        _tree_relationships = [str(r) for r in self.fm.get_relations()]
        return FMMetric(FMProperties.TREE_RELATIONSHIPS.value, 
                        _tree_relationships, 
                        len(_tree_relationships))

    def mandatory_features(self) -> FMMetric:
        _tree_relationships = [r for r in self.fm.get_relations()]
        _mandatory_features = [f.name for f in self.fm.get_mandatory_features()]
        return FMMetric(FMProperties.MANDATORY_FEATURES.value, 
                        _mandatory_features, 
                        len(_mandatory_features),
                        get_ratio(_mandatory_features, _tree_relationships))

    def optional_features(self) -> FMMetric:
        _tree_relationships = [r for r in self.fm.get_relations()]
        _optional_features = [f.name for f in self.fm.get_optional_features()]
        return FMMetric(FMProperties.OPTIONAL_FEATURES.value, 
                        _optional_features, 
                        len(_optional_features),
                        get_ratio(_optional_features, _tree_relationships))

    def group_features(self) -> FMMetric:
        _tree_relationships = [r for r in self.fm.get_relations()]
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        return FMMetric(FMProperties.GROUP_FEATURES.value, 
                        _group_features, 
                        len(_group_features),
                        get_ratio(_group_features, _tree_relationships))
    
    def alternative_groups(self) -> FMMetric:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _alternative_groups = [f.name for f in self.fm.get_alternative_group_features()]
        return FMMetric(FMProperties.ALTERNATIVE_GROUPS.value, 
                        _alternative_groups, 
                        len(_alternative_groups),
                        get_ratio(_alternative_groups, _group_features))
    
    def or_groups(self) -> FMMetric:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _or_groups = [f.name for f in self.fm.get_or_group_features()]
        return FMMetric(FMProperties.OR_GROUPS.value, 
                        _or_groups, 
                        len(_or_groups),
                        get_ratio(_or_groups, _group_features))

    def mutex_groups(self) -> FMMetric:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _mutex_groups = [f.name for f in self.fm.get_features() if f.is_mutex_group()]
        return FMMetric(FMProperties.MUTEX_GROUPS.value, 
                        _mutex_groups, 
                        len(_mutex_groups),
                        get_ratio(_mutex_groups, _group_features))

    def cardinality_groups(self) -> FMMetric:
        _group_features = [f.name for f in self.fm.get_features() if f.is_group()]
        _cardinality_groups = [f.name for f in self.fm.get_features() if f.is_cardinality_group()]
        return FMMetric(FMProperties.CARDINALITY_GROUPS.value, 
                        _cardinality_groups, 
                        len(_cardinality_groups),
                        get_ratio(_cardinality_groups, _group_features))
    
    def max_depth_tree(self) -> FMMetric:
        _max_depth_tree = fm_operations.max_depth_tree(self.fm)
        return FMMetric(FMProperties.MAX_DEPTH_TREE.value, 
                        _max_depth_tree)

    def avg_branching_factor(self) -> FMMetric:
        _avg_branching_factor = fm_operations.average_branching_factor(self.fm)
        return FMMetric(FMProperties.BRANCHING_FACTOR.value, 
                        _avg_branching_factor)

    def min_children_per_feature(self) -> FMMetric:
        _min_children_per_feature = min(sum(len(r.children) for r in feature.get_relations()) for feature in self.fm.get_features() if not feature.is_leaf())
        return FMMetric(FMProperties.MIN_CHILDREN_PER_FEATURE.value, 
                        _min_children_per_feature)

    def max_children_per_feature(self) -> FMMetric:
        _max_children_per_feature = max(sum(len(r.children) for r in feature.get_relations()) for feature in self.fm.get_features())
        return FMMetric(FMProperties.MAX_CHILDREN_PER_FEATURE.value, 
                        _max_children_per_feature)

    def avg_children_per_feature(self) -> FMMetric:
        nof_children = sum(len(r.children) for feature in self.fm.get_features() for r in feature.get_relations())
        _avg_children_per_feature = round(nof_children / len(self.fm.get_features()), 2)
        return FMMetric(FMProperties.AVG_CHILDREN_PER_FEATURE.value, 
                        _avg_children_per_feature)

    def cross_tree_constraints(self) -> FMMetric:
        _cross_tree_constraints = [str(ctc) for ctc in self.fm.get_constraints()]
        return FMMetric(FMProperties.CROSS_TREE_CONSTRAINTS.value, 
                        _cross_tree_constraints,
                        len(_cross_tree_constraints))

    def simple_constraints(self) -> FMMetric:
        _simple_constraints = [str(ctc) for ctc in self.fm.get_simple_constraints()]
        return FMMetric(FMProperties.SIMPLE_CONSTRAINTS.value, 
                        _simple_constraints,
                        len(_simple_constraints),
                        get_ratio(_simple_constraints, self.fm.get_constraints()))

    def requires_constraints(self) -> FMMetric:
        _requires_constraints = [str(ctc) for ctc in self.fm.get_requires_constraints()]
        return FMMetric(FMProperties.REQUIRES_CONSTRAINTS.value, 
                        _requires_constraints,
                        len(_requires_constraints),
                        get_ratio(_requires_constraints, self.fm.get_simple_constraints()))

    def excludes_constraints(self) -> FMMetric:
        _excludes_constraints = [str(ctc) for ctc in self.fm.get_excludes_constraints()]
        return FMMetric(FMProperties.EXCLUDES_CONSTRAINTS.value, 
                        _excludes_constraints,
                        len(_excludes_constraints),
                        get_ratio(_excludes_constraints, self.fm.get_simple_constraints()))

    def complex_constraints(self) -> FMMetric:
        _complex_constraints = [str(ctc) for ctc in self.fm.get_complex_constraints()]
        return FMMetric(FMProperties.COMPLEX_CONSTRAINTS.value, 
                        _complex_constraints,
                        len(_complex_constraints),
                        get_ratio(_complex_constraints, self.fm.get_constraints()))

    def pseudocomplex_constraints(self) -> FMMetric:
        _pseudocomplex_constraints = [str(ctc) for ctc in self.fm.get_pseudocomplex_constraints()]
        return FMMetric(FMProperties.PSEUDO_COMPLEX_CONSTRAINTS.value, 
                        _pseudocomplex_constraints,
                        len(_pseudocomplex_constraints),
                        get_ratio(_pseudocomplex_constraints, self.fm.get_complex_constraints()))

    def strictcomplex_constraints(self) -> FMMetric:
        _strictcomplex_constraints = [str(ctc) for ctc in self.fm.get_strictcomplex_constraints()]
        return FMMetric(FMProperties.STRICT_COMPLEX_CONSTRAINTS.value, 
                        _strictcomplex_constraints,
                        len(_strictcomplex_constraints),
                        get_ratio(_strictcomplex_constraints, self.fm.get_complex_constraints()))


# def _nof_constraints(feature_model: FeatureModel) -> tuple[int, int, int]:
#     """Return a tuple with the number of different types of constraints.
    
#     The tuple includes:
#       1. Requires constraints.
#       2. Excludes constraints.
#       3. Pseudo-complex constraints.
#       4. Strict-complex constraints.
#     """
#     nof_requires_constraints = 0
#     nof_excludes_constraints = 0
#     nof_pseudocomplex_constraints = 0
#     nof_strictcomplex_constraints = 0
#     for c in feature_model.get_constraints():
#         clauses = c.ast.get_clauses()
#         if len(clauses) == 1 and len(clauses[0]) == 2:
#             nof_negative_clauses = sum(var.startswith('-') for var in clauses[0])
#             if nof_negative_clauses == 1:
#                 nof_requires_constraints += 1
#             elif nof_negative_clauses == 2:
#                 nof_excludes_constraints += 1
#             else:
#                 nof_strictcomplex_constraints += 1
#         else:
#             strictcomplex = False
#             i = iter(clauses)
#             while not strictcomplex and (cls := next(i, None)) is not None:
#                 if len(cls) != 2:
#                     strictcomplex = True
#                 else:
#                     nof_negative_clauses = sum(var.startswith('-') for var in cls)
#                     if nof_negative_clauses not in [1, 2]:
#                         strictcomplex = True
#             if strictcomplex:
#                 nof_strictcomplex_constraints += 1
#             else:
#                 nof_pseudocomplex_constraints += 1
#     return (nof_requires_constraints, nof_excludes_constraints, nof_pseudocomplex_constraints, nof_strictcomplex_constraints)

