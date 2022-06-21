from rhea import LanguageConstruct 

from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Relation


class OrChildFeature(LanguageConstruct):

    def __init__(self, child_name: str, parent_name: str) -> None:
        self.child_name = child_name
        self.parent_name = parent_name
        self.feature = None

    @staticmethod
    def name() -> str:
        return 'Or child feature'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return sum(f.get_parent() is not None and f.get_parent().is_or_group() for f in fm.get_features())

    def get(self) -> Feature:
        return self.feature

    def apply(self, fm: FeatureModel) -> FeatureModel:
        parent = fm.get_feature_by_name(self.parent_name)
        relation = next(r for r in parent.get_relations() if r.is_or())  # Assume there is only one group relation per feature
        child = Feature(name=self.child_name, parent=parent)
        relation.add_child(child)
        relation.card_max += 1
        self.feature = child
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        if fm is None:
            return False
        parent = fm.get_feature_by_name(self.parent_name)
        child = fm.get_feature_by_name(self.child_name)
        if parent is None or child is not None:
            return False
        relation = next(r for r in parent.get_relations() if r.is_or())  # Assume there is only one group relation per feature
        return relation is not None

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None:
            return []
        lcs = []
        parents = [f for f in fm.get_features() if f.is_or_group()]
        for child_name in features_names:
            for p in parents:
                lc = OrChildFeature(child_name, p.name)
                if lc.is_applicable(fm):
                    lcs.append(lc)
        return lcs
