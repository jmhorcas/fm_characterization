from typing import Any, Optional
from enum import Enum


class FMProperty():
    '''It defines a property of the feature model.
    
    Each property has a name, a description, and maybe a property parent.
    The property parent is used to organize the properties in a hierarchy.
    '''

    def __init__(self, 
                 name: str,  
                 description: Optional[str] = None,  
                 parent: Optional['FMProperty'] = None):
        self.name = name
        self.description = description
        self.parent = parent

    def to_dict(self) -> dict[str, Any]:
        return {'name': self.name, 
                'description': self.description,
                'parent': self.parent.name if self.parent is not None else None,
                'level': self.level()}

    def level(self) -> int:
        '''Return the level of parents.'''
        if self.parent is None:
            return 0
        return 1 + self.parent.level()


class FMPropertyMeasure():
    """It represent the measure of a property.
    
    It has the value of the measure, it can also have a size and a ratio.
    Example:
        property: Abstract Features.
        value: the list of abstract features.
        size: the length of the list.
        ratio: the percentage of abstract features with regards the total number of features.
    """
    def __init__(self, 
                 property: FMProperty,
                 value: Optional[Any] = None,  # Example: the list of abstract features
                 size: Optional[Any] = None,  # Example: number of abstract features
                 ratio: Optional[Any] = None):  # Example: percentage of abstract features from the total number of features
        self.property = property
        self.value = value
        self.size = size 
        self.ratio = ratio

    def to_dict(self) -> dict[str, Any]:
        result = {'value': self.value,
                  'size': self.size,
                  'ratio': self.ratio}
        return self.property.to_dict() | result


class FMProperties(Enum):
    # METADATA
    NAME = FMProperty('Name', 'Name of the feature model.', None)
    DESCRIPTION = FMProperty('Description', 'Description of the feature model.', None)
    AUTHOR = FMProperty('Author', 'Author of the feature model', None)
    YEAR = FMProperty('Year', 'Year of creation of the feature model', None)
    REFERENCE = FMProperty('Reference', 'Main paper for reference or DOI of the feature model', None)
    TAGS = FMProperty('Tags', 'Tags or keywords that identify the feature model.', None)
    DOMAIN = FMProperty('Domain', 'Domain of the feature model.', None)

    # METRICS
    FEATURES = FMProperty('Features', 'Set of features in the feature model.', None)
    ABSTRACT_FEATURES = FMProperty('Abstract features', 'Features used to structure the feature model that, however, do not have any impact at implementation level.', FEATURES)
    CONCRETE_FEATURES = FMProperty('Concrete features', 'Features that are mapped to at least one implementation artifact.', FEATURES)
    ROOT_FEATURE = FMProperty('Root feature', 'The root of the feature model.', None)
    TOP_FEATURES = FMProperty('Top features', 'Features that are first descendants of the root.', ROOT_FEATURE)
    TREE_RELATIONSHIPS = FMProperty('Tree relationships', '', None)
    MANDATORY_FEATURES = FMProperty('Mandatory features', '', TREE_RELATIONSHIPS)
    OPTIONAL_FEATURES = FMProperty('Optional features', '', TREE_RELATIONSHIPS)
    GROUP_FEATURES = FMProperty('Group features', '', TREE_RELATIONSHIPS)
    ALTERNATIVE_GROUPS = FMProperty('Alternative groups', '', GROUP_FEATURES)
    OR_GROUPS = FMProperty('Or groups', '', GROUP_FEATURES)
    MUTEX_GROUPS = FMProperty('Mutex groups', '', GROUP_FEATURES)
    CARDINALITY_GROUPS = FMProperty('Cardinality groups', '', GROUP_FEATURES)
    BRANCHING_FACTOR = FMProperty('Branching factor', '', None)  # Also 'Avg children per feature'
    MIN_CHILDREN_PER_FEATURE = FMProperty('Min children per feature', '', BRANCHING_FACTOR)
    MAX_CHILDREN_PER_FEATURE = FMProperty('Max children per feature', '', BRANCHING_FACTOR)
    AVG_CHILDREN_PER_FEATURE = FMProperty('Avg children per feature', '', BRANCHING_FACTOR)
    LEAF_FEATURES = FMProperty('Leaf features', '', FEATURES)
    MAX_DEPTH_TREE = FMProperty('Max depth tree', '', None)

    CROSS_TREE_CONSTRAINTS = FMProperty('Cross-tree constraints', '', None)
    SIMPLE_CONSTRAINTS = FMProperty('Simple constraints', 'Requires and Excludes constraints.', CROSS_TREE_CONSTRAINTS)  # Requires and excludes
    REQUIRES_CONSTRAINTS = FMProperty('Requires constraints', '', SIMPLE_CONSTRAINTS)
    EXCLUDES_CONSTRAINTS = FMProperty('Excludes constraints', '', SIMPLE_CONSTRAINTS)
    COMPLEX_CONSTRAINTS = FMProperty('Complex constraints', '', CROSS_TREE_CONSTRAINTS)  # Prop logic constraints (aka advanced constraints)
    PSEUDO_COMPLEX_CONSTRAINTS = FMProperty('Pseudo-complex constraints', '', COMPLEX_CONSTRAINTS)
    STRICT_COMPLEX_CONSTRAINTS = FMProperty('Strict-complex constraints', '', COMPLEX_CONSTRAINTS)
    #MAX_CONSTRAINTS_PER_FEATURE = FMProperty('Max constraints per feature', '', None)
    #AVG_CONSTRAINTS_PER_FEATURE = FMProperty('Avg constraints per feature', '', None)

    VALID = FMProperty('Valid (not void)', '', None)
    CORE_FEATURES = FMProperty('Core features', '', None)  # Also 'Common features'
    VARIANT_FEATURES = FMProperty('Variant features', '', None)  # Also 'Real optional features'
    DEAD_FEATURES = FMProperty('Dead features', '', None)
    UNIQUE_FEATURES = FMProperty('Unique features', '', None)
    FALSE_OPTIONAL_FEATURES = FMProperty('False-optional features', '', None)
    CONFIGURATIONS = FMProperty('Configurations', '', None)
    # ATOMIC_SETS = FMProperty('Atomic sets', '', None)  # Atomic sets need to be fixed in FLAMA.