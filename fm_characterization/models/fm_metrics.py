
from famapy.metamodels.fm_metamodel.models import FeatureModel

from famapy.metamodels.fm_metamodel.operations import (
    average_branching_factor, 
    max_depth_tree
)

class FMMetrics():

    def __init__(self, model: FeatureModel):
        self.fm = model

    def nof_features(self) -> int:
        return nof_features(self.fm)

    def nof_group_features(self) -> int:
        return nof_group_features(self.fm)

    def nof_alternative_groups(self) -> int:
        return nof_alternative_groups(self.fm)

    def nof_or_groups(self) -> int:
        return nof_or_groups(self.fm)
    
    def nof_abstract_features(self) -> int:
        return nof_abstract_features(self.fm)

    def nof_leaf_features(self) -> int:
        return nof_leaf_features(self.fm)

    def nof_cross_tree_constraints(self) -> int:
        return nof_cross_tree_constraints(self.fm)
    
    def avg_branching_factor(self) -> float:
        return average_branching_factor(self.fm)

    def max_depth_tree(self) -> int:
        return max_depth_tree(self.fm)


def nof_features(feature_model: FeatureModel) -> int:
    return len(feature_model.get_features())

def nof_group_features(feature_model: FeatureModel) -> int:
    return sum(f.is_group() for f in feature_model.get_features())

def nof_alternative_groups(feature_model: FeatureModel) -> int:
    return sum(f.is_alternative_group() for f in feature_model.get_features())

def nof_or_groups(feature_model: FeatureModel) -> int:
    return sum(f.is_or_group() for f in feature_model.get_features())

def nof_abstract_features(feature_model: FeatureModel) -> int:
    return sum(f.is_abstract for f in feature_model.get_features())

def nof_leaf_features(feature_model: FeatureModel) -> int:
    return sum(len(f.get_relations()) == 0 for f in feature_model.get_features())

def nof_cross_tree_constraints(feature_model: FeatureModel) -> int:
    return len(feature_model.get_constraints())
