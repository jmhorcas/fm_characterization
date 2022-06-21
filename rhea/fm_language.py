import copy
import queue
from famapy.metamodels.fm_metamodel.models import FeatureModel, Feature

from rhea import LanguageConstruct


class FMLanguage():

    def __init__(self, lcs: list[LanguageConstruct]) -> None:
        self.lcs = lcs

    def generate_feature_models(self, features_names: set[str]) -> list[FeatureModel]:
        incomplete_feature_models = queue.Queue()
        incomplete_feature_models.put(None)
        completed_fms = []
        while not incomplete_feature_models.empty():
            fm = incomplete_feature_models.get()
            applicable_lcs = []
            for lc in self.lcs:
                applicable_lcs.extend(lc.get_applicable_instances(fm, features_names))
            if not applicable_lcs:
                completed_fms.append(fm)
            else:
                for alc in applicable_lcs:
                    new_fm = copy.deepcopy(fm)
                    incomplete_feature_models.put(alc.apply(new_fm))
        return completed_fms
