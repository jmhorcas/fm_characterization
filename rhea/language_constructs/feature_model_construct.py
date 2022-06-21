from rhea import LanguageConstruct 

from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature


class FeatureModelConstruct(LanguageConstruct):

    def __init__(self) -> None:
        self.fm = None

    @staticmethod
    def name() -> str:
        return 'Feature Model'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return 0 if fm is None else 1 

    def get(self) -> FeatureModel:
        return self.fm

    def apply(self, fm: FeatureModel) -> FeatureModel:
        fm = FeatureModel(root=None)
        self.fm = fm
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        return fm is None

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        lc = FeatureModelConstruct()
        return [lc] if lc.is_applicable(fm) else []
