import json

from fm_characterization.models.fm_characterization import FMCharacterization
from fm_characterization.models.fm_metrics import FMProperty


SPACE = ' '


def get_parents_numbers(property: FMProperty) -> int:
    if property.parent is None:
        return 1
    return 1 + get_parents_numbers(property.parent)

def get_string_output(fm_characterization: FMCharacterization) -> str:
    lines = ['METRICS']
    for metric in fm_characterization.get_metrics():
        indentation = SPACE * get_parents_numbers(metric.property)
        name = metric.property.name
        value = str(metric.value) if metric.size is None else str(metric.size)
        ratio = f' ({str(metric.ratio*100)}%)' if metric.ratio is not None else ''
        lines.append(f'{indentation}{name}: {value}{ratio}')    
    return '\n'.join(lines)

def to_json(fm_characterization: FMCharacterization, filepath: str) -> None:
    result = []
    for metric in fm_characterization.get_metrics():
        result.append(metric.to_dict())
    with open(filepath, 'w') as output_file:
        json.dump(result, output_file, indent=4)
    