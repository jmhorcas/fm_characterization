from multiprocessing.sharedctypes import Value
from typing import Any, Optional
from enum import Enum

from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature

from famapy.metamodels.fm_metamodel.operations import (
    average_branching_factor, 
    max_depth_tree
)


class FMProperties(Enum):
    VALID = 'Valid (not void)'
    FEATURES = 'Features'
    ABSTRACT_FEATURES = 'Abstract features'
    CONCRETE_FEATURES = 'Concrete features'
    TOP_FEATURES = 'Top features'  # Features that are first descendants of the root.
    TREE_RELATIONSHIPS = 'Tree relationships'
    MANDATORY_FEATURES = 'Mandatory features'
    OPTIONAL_FEATURES = 'Optional features'
    GROUP_FEATURES = 'Group features'
    ALTERNATIVE_GROUPS = 'Alternative groups'
    OR_GROUPS = 'Or groups'
    MUTEX_GROUPS = 'Mutex groups'
    CARDINALITY_GROUPS = 'Cardinality groups'
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


class FMMetric():

    def __init__(self, 
                 name: str, 
                 value: Optional[Any] = None, 
                 size: Optional[Any] = None,
                 ratio: Optional[Any] = None):
        self.name = name
        self.value = value
        self.size = size 
        self.ratio = ratio

    def get_metric(self) -> dict[str, Any]:
        return {'name': self.name, 
                'value': self.value,
                'size': self.size,
                'ratio': self.ratio}


class FMMetrics():

    def __init__(self, model: FeatureModel):
        self.fm = model
        
    def features(self) -> FMMetric:
        features = [f.name for f in self.fm.get_features()]
        return FMMetric(FMProperties.FEATURES.value, features, len(features))

    def abstract_features(self) -> FMMetric:
        abstract_features = [f.name for f in self.fm.get_features() if f.is_abstract]
        return FMMetric(FMProperties.ABSTRACT_FEATURES.value, 
                        abstract_features, 
                        len(abstract_features),
                        round(len(abstract_features) / len(self.fm.get_features()), 4))

    def nof_features(self) -> int:
        return len(self.fm.get_features())

    def nof_abstract_features(self) -> int:
        return sum(f.is_abstract for f in self.fm.get_features())

    def nof_concrete_features(self) -> int:
        return sum(not f.is_abstract for f in self.fm.get_features())
    
    def nof_top_features(self) -> int:
        return sum(len(r.children) for r in self.fm.root.get_relations())

    def nof_tree_relationships(self) -> int:
        return len(self.fm.get_relations())

    def nof_mandatory_features(self) -> int:
        return sum(f.is_mandatory() for f in self.fm.get_features())

    def nof_optional_features(self) -> int:
        return sum(f.is_optional() for f in self.fm.get_features())

    def nof_group_features(self) -> int:
        return sum(f.is_group() for f in self.fm.get_features())

    def nof_alternative_groups(self) -> int:
        return sum(f.is_alternative_group() for f in self.fm.get_features())

    def nof_or_groups(self) -> int:
        return sum(f.is_or_group() for f in self.fm.get_features())
    
    def nof_mutex_groups(self) -> int:
        return sum(f.is_mutex_group() for f in self.fm.get_features())

    def nof_cardinality_groups(self) -> int:
        return sum(f.is_cardinality_group() for f in self.fm.get_features())

    def nof_leaf_features(self) -> int:
        return sum(len(f.get_relations()) == 0 for f in self.fm.get_features())

    def avg_branching_factor(self) -> float:
        return average_branching_factor(self.fm)

    def min_children_per_feature(self) -> int:
        return min(sum(len(r.children) for r in feature.get_relations()) for feature in self.fm.get_features() if not feature.is_leaf())

    def max_children_per_feature(self) -> int:
        return max(sum(len(r.children) for r in feature.get_relations()) for feature in self.fm.get_features())
    
    def avg_children_per_feature(self) -> int:
        nof_children = sum(len(r.children) for feature in self.fm.get_features() for r in feature.get_relations())
        return round(nof_children / self.nof_features(), 2)
        
    def max_depth_tree(self) -> int:
        return max_depth_tree(self.fm)

    def nof_cross_tree_constraints(self) -> int:
        return len(self.fm.get_constraints())
    
    def nof_simple_constraints(self) -> int:
        return len(self.fm.get_simple_constraints())

    def nof_requires_constraints(self) -> int:
        return len(self.fm.get_requires_constraints())
    
    def nof_excludes_constraints(self) -> int:
        return len(self.fm.get_excludes_constraints())
    
    def nof_complex_constraints(self) -> int:
        return len(self.fm.get_complex_constraints())

    def nof_pseudocomplex_constraints(self) -> int:
        return len(self.fm.get_pseudocomplex_constraints())
    
    def nof_strictcomplex_constraints(self) -> int:
        return len(self.fm.get_strictcomplex_constraints())


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

