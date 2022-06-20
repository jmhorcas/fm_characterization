import copy

from rhea import LanguageConstruct 

from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Relation


class OptionalFeature(LanguageConstruct):

    def __init__(self, name: str, parent_name: str) -> None:
        self.name = name
        self.parent_name = parent_name
        self.feature = None

    @staticmethod
    def name() -> str:
        return 'Optional Feature'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return len(fm.get_optional_features())

    def get(self) -> Feature:
        return self.feature

    def apply(self, fm: FeatureModel) -> FeatureModel:
        parent = fm.get_feature_by_name(self.parent_name)
        self.feature = Feature(name=self.name, parent=parent)
        relation = Relation(parent=parent, children=[self.feature], card_min=0, card_max=1)
        parent.add_relation(relation)
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        if fm is None:
            return False
        feature = fm.get_feature_by_name(self.name) 
        parent = fm.get_feature_by_name(self.parent_name)
        return feature is None and parent is not None and any(not f.is_group() for f in fm.get_features())

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None:
            return []
        lcs = []
        parents = [f for f in fm.get_features() if not f.is_group()]
        for f_name in features_names:
            for p in parents:
                lc = OptionalFeature(f_name, p.name)
                if lc.is_applicable(fm):
                    lcs.append(lc)
        return lcs