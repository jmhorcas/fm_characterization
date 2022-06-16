import copy
import functools
import itertools
from typing import Optional 

from famapy.core.models.ast import AST, ASTOperation, Node
from famapy.metamodels.fm_metamodel.models import (
    FeatureModel, 
    Feature, 
    Relation,
    Constraint
)


class FMGenerator():

    def __init__(self, feature_model: Optional[FeatureModel] = None) -> None:
        self._fm = feature_model

    def get_feature_model(self) -> FeatureModel:
        return self._fm

    def create_fm(self) -> None:
        self._fm = FeatureModel(root=None)

    def create_root(self, root_name: str) -> None:
        self.get_feature_model().root = Feature(name=root_name)

    def create_mandatory_feature(self, feature_name: str, parent_name: str) -> None:
        parent = self.get_feature_model().get_feature_by_name(parent_name)
        feature = Feature(name=feature_name, parent=parent)
        relation = Relation(parent=parent, children=[feature], card_min=1, card_max=1)
        parent.add_relation(relation)
    
    def create_optional_feature(self, feature_name: str, parent_name: str) -> None:
        parent = self.get_feature_model().get_feature_by_name(parent_name)
        feature = Feature(name=feature_name, parent=parent)
        relation = Relation(parent=parent, children=[feature], card_min=0, card_max=1)
        parent.add_relation(relation)

    def create_or_group(self, feature_name: str, child1_name: str, child2_name: str) -> None:
        feature = self.get_feature_model().get_feature_by_name(feature_name)
        child1 = Feature(name=child1_name, parent=feature)
        child2 = Feature(name=child2_name, parent=feature)
        relation = Relation(parent=feature, children=[child1, child2], card_min=1, card_max=2)
        feature.add_relation(relation)

    def create_xor_group(self, feature_name: str, child1_name: str, child2_name: str) -> None:
        feature = self.get_feature_model().get_feature_by_name(feature_name)
        child1 = Feature(name=child1_name, parent=feature)
        child2 = Feature(name=child2_name, parent=feature)
        relation = Relation(parent=feature, children=[child1, child2], card_min=1, card_max=1)
        feature.add_relation(relation)
    
    def create_child_feature_in_group(self, feature_name: str, parent_name: str) -> None:
        parent = self.get_feature_model().get_feature_by_name(parent_name)
        feature = Feature(name=feature_name, parent=parent)
        relation = next(r for r in parent.get_relations())  # Assume there is only one group relation per feature
        relation.add_child(feature)
        if relation.is_or():
            relation.card_max += 1

    def create_requires_constraint(self, left_feature_name: str, right_feature_name: str) -> None:
        left_feature = self.get_feature_model().get_feature_by_name(left_feature_name)
        right_feature = self.get_feature_model().get_feature_by_name(right_feature_name)
        ast = AST.create_simple_binary_operation(operation=ASTOperation.REQUIRES, left=left_feature.name, right=right_feature.name)
        ctcs = self.get_feature_model().get_constraints()
        ctc = Constraint(f'CTC{len(ctcs)+1}', ast)
        ctcs.append(ctc)
    
    def create_excludes_constraint(self, left_feature_name: str, right_feature_name: str) -> None:
        left_feature = self.get_feature_model().get_feature_by_name(left_feature_name)
        right_feature = self.get_feature_model().get_feature_by_name(right_feature_name)
        ast = AST.create_simple_binary_operation(operation=ASTOperation.EXCLUDES, left=left_feature.name, right=right_feature.name)
        ctcs = self.get_feature_model().get_constraints()
        ctc = Constraint(f'CTC{len(ctcs)+1}', ast)
        ctcs.append(ctc)

    def create_cnf_constraint(self, positive_features_names: list[str], negative_features_names: list[str]) -> None:
        positive_features = [self.get_feature_model().get_feature_by_name(f) for f in positive_features_names]
        negative_features = [self.get_feature_model().get_feature_by_name(f) for f in negative_features_names]
        ast_root_pos = functools.reduce(lambda a, b: AST.create_binary_operation(operation=ASTOperation.OR, left=(a if isinstance(a, Node) else Node(a)), right=(b if isinstance(b, Node) else Node(b))).root, positive_features)
        ast_root_neg = functools.reduce(lambda a, b: AST.create_binary_operation(operation=ASTOperation.OR, left=(a if isinstance(a, Node) else Node(a)), right=(b if isinstance(b, Node) else Node(b))).root, negative_features)
        ast = AST.create_binary_operation(operation=ASTOperation.OR, left=ast_root_pos, right=ast_root_neg)
        ctcs = self.get_feature_model().get_constraints()
        ctc = Constraint(f'CTC{len(ctcs)+1}', ast)
        ctcs.append(ctc)

    def identify_possible_feature_parents(self) -> list[Feature]:
        """Identify the possible features in the feature model where a new feature can be added as an optional or mandatory feature."""
        return [f for f in self.get_feature_model().get_features() if not f.is_group()]

    def identify_possible_group_parents(self) -> list[Feature]:
        """Identify the possible group features in the feature model where a new feature can be added as a child."""
        return [f for f in self.get_feature_model().get_features() if f.is_group()]

    def identify_possible_groups(self) -> list[Feature]:
        """Identify the possible features in the feature model where a new group relation can be added."""
        return [f for f in self.get_feature_model().get_features() if not f.get_relations()]


def generate_all_feature_models(n_features: int, generate_constraints: bool) -> list[FeatureModel]:
    complete_models = set()
    models = list()
    features = [f'F{i}' for i in range(1, n_features + 1)]
    
    # Create the feature model with only the root feature
    fm_generator = FMGenerator()
    fm_generator.create_fm()
    fm_generator.create_root(features.pop(0))
    models.append((fm_generator.get_feature_model(), features))
    
    while models:
        #print(f'models: {[str(m) for m in models]}')
        #print(f'complete_models: {[str(m) for m in complete_models]}')
        m, features = models.pop()
        if len(features) == 0:
            complete_models.add(m)
        else:
            gen = FMGenerator(m)
            if len(features) > 1:
                # Create groups
                parents = gen.identify_possible_groups()
                child1_name = features[0]
                child2_name = features[1]
                for p in parents:
                    new_gen = FMGenerator(copy.deepcopy(m))
                    new_gen.create_or_group(p.name, child1_name, child2_name)
                    models.append((new_gen.get_feature_model(), features[2:]))
                for p in parents:
                    new_gen = FMGenerator(copy.deepcopy(m))
                    new_gen.create_xor_group(p.name, child1_name, child2_name)
                    models.append((new_gen.get_feature_model(), features[2:]))
            feature_name = features[0]
            parents = gen.identify_possible_feature_parents()
            # Create optional features
            for p in parents:
                new_gen = FMGenerator(copy.deepcopy(m))
                new_gen.create_optional_feature(feature_name, p.name)
                models.append((new_gen.get_feature_model(), features[1:]))
            # Create mandatory features
            for p in parents:
                new_gen = FMGenerator(copy.deepcopy(m))
                new_gen.create_mandatory_feature(feature_name, p.name)
                models.append((new_gen.get_feature_model(), features[1:]))

            parents = gen.identify_possible_group_parents()
            # Create child of group
            for p in parents:
                new_gen = FMGenerator(copy.deepcopy(m))
                new_gen.create_child_feature_in_group(feature_name, p.name)
                models.append((new_gen.get_feature_model(), features[1:]))
    
    #for m in models:
    #    print(f'm:{[str(f) for f in m.get_features()]} -> {str(m)}')
    if generate_constraints:
        if n_features > 1:
            features = [f'F{i}' for i in range(1, n_features + 1)]
            pair_wise = itertools.combinations(features, 2)
            for left, right in pair_wise:
                models = copy.copy(complete_models)
                for m in models:
                    new_gen = FMGenerator(copy.deepcopy(m))
                    new_gen.create_requires_constraint(left, right)
                    complete_models.add(new_gen.get_feature_model())
                
                    new_gen = FMGenerator(copy.deepcopy(m))
                    new_gen.create_excludes_constraint(left, right)
                    complete_models.add(new_gen.get_feature_model())

    return complete_models