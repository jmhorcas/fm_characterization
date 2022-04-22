import json
from typing import Any, Optional

from fm_characterization.models.fm_characterization import FMCharacterization
from fm_characterization.models.fm_metrics import FMProperty


SPACE = ' '


def get_parents_numbers(property: FMProperty) -> int:
    if property.parent is None:
        return 1
    return 1 + get_parents_numbers(property.parent)

def get_string_output(fm_characterization: FMCharacterization) -> str:
    lines = ['METADATA']
    for metric in fm_characterization.get_metadata():
        name = metric.property.name
        value = str(metric.value)
        lines.append(f'{name}: {value}')    

    lines.append('METRICS')
    for metric in fm_characterization.get_metrics():
        indentation = SPACE * get_parents_numbers(metric.property)
        name = metric.property.name
        value = str(metric.value) if metric.size is None else str(metric.size)
        ratio = f' ({str(metric.ratio*100)}%)' if metric.ratio is not None else ''
        lines.append(f'{indentation}{name}: {value}{ratio}')    
    
    lines.append('ANALYSIS')
    for metric in fm_characterization.get_analysis():
        indentation = SPACE * get_parents_numbers(metric.property)
        name = metric.property.name
        value = str(metric.value) if metric.size is None else str(metric.size)
        ratio = f' ({str(metric.ratio*100)}%)' if metric.ratio is not None else ''
        lines.append(f'{indentation}{name}: {value}{ratio}')    
    return '\n'.join(lines)

def to_json_str(fm_characterization: FMCharacterization, filepath: Optional[str] = None) -> str:
    result = to_json(fm_characterization)
    if filepath is not None:
        with open(filepath, 'w') as output_file:
            json.dump(result, output_file, indent=4)
    return json.dumps(result, indent=4).encode("utf8")


def to_json(fm_characterization: FMCharacterization) -> dict[Any]:
    metadata = []
    metrics = []
    analysis = []

    for metric in fm_characterization.get_metadata():
        metadata.append(metric.to_dict())

    for metric in fm_characterization.get_metrics():
        metrics.append(metric.to_dict())

    for metric in fm_characterization.get_analysis():
        analysis.append(metric.to_dict())


    result = {}
    result['metadata'] = metadata
    result['metrics'] = metrics
    result['analysis'] = analysis
    return result