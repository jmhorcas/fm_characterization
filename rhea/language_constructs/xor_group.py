import itertools

from rhea import LanguageConstruct 

from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Relation


class XorGroup(LanguageConstruct):

    def __init__(self, feature_name: str, child1_name: str, child2_name: str) -> None:
        self.child1_name = child1_name
        self.child2_name = child2_name
        self.feature_name = feature_name
        self.feature = None

    @staticmethod
    def name() -> str:
        return 'Alternative (xor) Group'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return len(fm.get_alternative_group_features())

    def get(self) -> Feature:
        return self.feature

    def apply(self, fm: FeatureModel) -> FeatureModel:
        feature = fm.get_feature_by_name(self.feature_name)
        child1 = Feature(name=self.child1_name, parent=feature)
        child2 = Feature(name=self.child2_name, parent=feature)
        relation = Relation(parent=feature, children=[child1, child2], card_min=1, card_max=1)
        feature.add_relation(relation)
        self.feature = feature
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        if fm is None:
            return False
        feature = fm.get_feature_by_name(self.feature_name) 
        child1 = fm.get_feature_by_name(self.child1_name)
        child2 = fm.get_feature_by_name(self.child2_name)
        return feature is not None and child1 is None and child2 is None and not feature.get_relations()

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None:
            return []
        lcs = []
        features = [f for f in fm.get_features() if not f.get_relations()]
        child_combinations = itertools.combinations(features_names, 2)
        for child1_name, child2_name in child_combinations:
            for f in features:
                lc = XorGroup(f.name, child1_name, child2_name)
                if lc.is_applicable(fm):
                    lcs.append(lc)
        return lcs
