from fm_characterization.models.fm_characterization import FMCharacterization

from fm_characterization.models.fm_characterization import FMCharacterization, FMProperties


def get_string_output(fm_characterization: FMCharacterization) -> str:
    lines = ['METRICS']
    lines.append(f'  {FMProperties.FEATURES.value}: {fm_characterization.metrics[FMProperties.FEATURES]}')
    lines.append(f'    {FMProperties.ABSTRACT_FEATURES.value}: {fm_characterization.metrics[FMProperties.ABSTRACT_FEATURES]}')
    lines.append(f'    {FMProperties.CONCRETE_FEATURES.value}: {fm_characterization.metrics[FMProperties.CONCRETE_FEATURES]}')

    lines.append(f'  {FMProperties.TREE_RELATIONSHIPS.value}: {fm_characterization.metrics[FMProperties.TREE_RELATIONSHIPS]}')
    lines.append(f'    {FMProperties.MANDATORY_FEATURES.value}: {fm_characterization.metrics[FMProperties.MANDATORY_FEATURES]}')
    lines.append(f'    {FMProperties.OPTIONAL_FEATURES.value}: {fm_characterization.metrics[FMProperties.OPTIONAL_FEATURES]}')
    lines.append(f'    {FMProperties.GROUP_FEATURES.value}: {fm_characterization.metrics[FMProperties.GROUP_FEATURES]}')
    lines.append(f'      {FMProperties.ALTERNATIVE_GROUPS.value}: {fm_characterization.metrics[FMProperties.ALTERNATIVE_GROUPS]}')
    lines.append(f'      {FMProperties.OR_GROUPS.value}: {fm_characterization.metrics[FMProperties.OR_GROUPS]}')
    
    lines.append(f'  {FMProperties.LEAF_FEATURES.value}: {fm_characterization.metrics[FMProperties.LEAF_FEATURES]}')
    lines.append(f'  {FMProperties.BRANCHING_FACTOR.value}: {fm_characterization.metrics[FMProperties.BRANCHING_FACTOR]}')
    lines.append(f'    {FMProperties.MIN_CHILDREN_PER_FEATURE.value}: {fm_characterization.metrics[FMProperties.MIN_CHILDREN_PER_FEATURE]}')
    lines.append(f'    {FMProperties.MAX_CHILDREN_PER_FEATURE.value}: {fm_characterization.metrics[FMProperties.MAX_CHILDREN_PER_FEATURE]}')
    lines.append(f'    {FMProperties.AVG_CHILDREN_PER_FEATURE.value}: {fm_characterization.metrics[FMProperties.AVG_CHILDREN_PER_FEATURE]}')
    lines.append(f'  {FMProperties.MAX_DEPTH_TREE.value}: {fm_characterization.metrics[FMProperties.MAX_DEPTH_TREE]}')

    lines.append(f'  {FMProperties.CROSS_TREE_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.CROSS_TREE_CONSTRAINTS]}')
    lines.append(f'    {FMProperties.SIMPLE_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.SIMPLE_CONSTRAINTS]}')
    lines.append(f'      {FMProperties.REQUIRES_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.REQUIRES_CONSTRAINTS]}')
    lines.append(f'      {FMProperties.EXCLUDES_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.EXCLUDES_CONSTRAINTS]}')
    lines.append(f'    {FMProperties.COMPLEX_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.COMPLEX_CONSTRAINTS]}')
    lines.append(f'      {FMProperties.PSEUDO_COMPLEX_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.PSEUDO_COMPLEX_CONSTRAINTS]}')
    lines.append(f'      {FMProperties.STRICT_COMPLEX_CONSTRAINTS.value}: {fm_characterization.metrics[FMProperties.STRICT_COMPLEX_CONSTRAINTS]}')

    lines.append('ANALYSIS')
    lines.append(f'  {FMProperties.CORE_FEATURES.value}: {fm_characterization.analysis[FMProperties.CORE_FEATURES]}')
    lines.append(f'  {FMProperties.VARIANT_FEATURES.value}: {fm_characterization.analysis[FMProperties.VARIANT_FEATURES]}')
    lines.append(f'  {FMProperties.DEAD_FEATURES.value}: {fm_characterization.analysis[FMProperties.DEAD_FEATURES]}')
    lines.append(f'  {FMProperties.CONFIGURATIONS.value}: {fm_characterization.analysis[FMProperties.CONFIGURATIONS]}')
    return '\n'.join(lines)