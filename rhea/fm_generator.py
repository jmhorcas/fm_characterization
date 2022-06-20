
from famapy.metamodels.fm_metamodel.models import FeatureModel

from rhea import LanguageConstruct
from rhea.language_constructs import (
    FeatureModelConstruct,
    RootFeature,
    OptionalFeature,
    MandatoryFeature
)


class FMGenerator():
    pass

def get_applicable_language_constructs_instances(fm: FeatureModel, 
                                                 features_names: set[str],
                                                 language_constructs: list[LanguageConstruct]) -> list[LanguageConstruct]:
    lcs = []
    # Feature model construct
    if FeatureModelConstruct in language_constructs:
        lc = FeatureModelConstruct()
        return [FeatureModelConstruct()]
    # Root feature
    if fm.root is None:
        for f_name in features_names:
            lcs.append(RootFeature(f_name))
        return lcs
    # Optional and mandatory features
    parents = [f for f in fm.get_features() if not f.is_group()]
    for f_name in features_names:
        for p in parents:

            lcs.append(OptionalFeature(f_name, p.name))
            lcs.append(MandatoryFeature(f_name, p.name))
    return lcs