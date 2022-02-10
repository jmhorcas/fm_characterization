
from famapy.metamodels.fm_metamodel.models import FeatureModel

from famapy.metamodels.fm_metamodel.operations import (
    average_branching_factor, 
    max_depth_tree
)


class FMMetrics():

    def __init__(self, model: FeatureModel):
        self.fm = model
        self._nof_constraints = _nof_constraints(model)

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
        return self.nof_requires_constraints() + self.nof_excludes_constraints()

    def nof_requires_constraints(self) -> int:
        return self._nof_constraints[0]
    
    def nof_excludes_constraints(self) -> int:
        return self._nof_constraints[1]
    
    def nof_complex_constraints(self) -> int:
        return self.nof_pseudocomplex_constraints() + self.nof_strictcomplex_constraints()

    def nof_pseudocomplex_constraints(self) -> int:
        return self._nof_constraints[2]
    
    def nof_strictcomplex_constraints(self) -> int:
        return self._nof_constraints[3]


def _nof_constraints(feature_model: FeatureModel) -> tuple[int, int, int]:
    """Return a tuple with the number of different types of constraints.
    
    The tuple includes:
      1. Requires constraints.
      2. Excludes constraints.
      3. Pseudo-complex constraints.
      4. Strict-complex constraints.
    """
    nof_requires_constraints = 0
    nof_excludes_constraints = 0
    nof_pseudocomplex_constraints = 0
    nof_strictcomplex_constraints = 0
    for c in feature_model.get_constraints():
        clauses = c.ast.get_clauses()
        if len(clauses) == 1 and len(clauses[0]) == 2:
            nof_negative_clauses = sum(var.startswith('-') for var in clauses[0])
            if nof_negative_clauses == 1:
                nof_requires_constraints += 1
            elif nof_negative_clauses == 2:
                nof_excludes_constraints += 1
            else:
                nof_strictcomplex_constraints += 1
        else:
            strictcomplex = False
            i = iter(clauses)
            while not strictcomplex and (cls := next(i, None)) is not None:
                if len(cls) != 2:
                    strictcomplex = True
                else:
                    nof_negative_clauses = sum(var.startswith('-') for var in cls)
                    if nof_negative_clauses not in [1, 2]:
                        strictcomplex = True
            if strictcomplex:
                nof_strictcomplex_constraints += 1
            else:
                nof_pseudocomplex_constraints += 1
    return (nof_requires_constraints, nof_excludes_constraints, nof_pseudocomplex_constraints, nof_strictcomplex_constraints)

