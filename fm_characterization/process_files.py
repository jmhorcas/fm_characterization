import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median
from typing import Optional, Dict, Any

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, FeatureIDEReader

from fm_characterization import FMCharacterization, FMProperties
from .fm_utils import get_ratio_sizes


def read_fm_file(filename: str) -> Optional[FeatureModel]:
    try:
        if filename.endswith(".uvl"):
            return UVLReader(filename).transform()
        elif filename.endswith(".xml") or filename.endswith(".fide"):
            return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(f"Error reading file with specific handler: {e}")
    
    try:
        return UVLReader(filename).transform()
    except Exception as e:
        print(f"Error reading file with UVLReader: {e}")
    
    try:
        return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(f"Error reading file with FeatureIDEReader: {e}")
    
    return None


def process_single_file(file_path: str) -> Optional[FMCharacterization]:
    fm = read_fm_file(file_path)
    if fm:
        return FMCharacterization(fm)
    return None
def get_metrics_with_ratios() -> Dict[str, Any]:
    return {
        FMProperties.ABSTRACT_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.CONCRETE_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.ROOT_FEATURE.value.name: FMProperties.FEATURES.value.name,
        FMProperties.TOP_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.LEAF_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.COMPOUND_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.ABSTRACT_LEAF_FEATURES.value.name: FMProperties.ABSTRACT_FEATURES.value.name,
        FMProperties.ABSTRACT_COMPOUND_FEATURES.value.name: FMProperties.ABSTRACT_FEATURES.value.name,
        FMProperties.CONCRETE_LEAF_FEATURES.value.name: FMProperties.CONCRETE_FEATURES.value.name,
        FMProperties.CONCRETE_COMPOUND_FEATURES.value.name: FMProperties.CONCRETE_FEATURES.value.name,
        FMProperties.SOLITARY_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.GROUPED_FEATURES.value.name: FMProperties.FEATURES.value.name,
        FMProperties.MANDATORY_FEATURES.value.name: FMProperties.SOLITARY_FEATURES.value.name,
        FMProperties.OPTIONAL_FEATURES.value.name: FMProperties.SOLITARY_FEATURES.value.name,
        FMProperties.FEATURE_GROUPS.value.name: FMProperties.TREE_RELATIONSHIPS.value.name,
        FMProperties.ALTERNATIVE_GROUPS.value.name: FMProperties.GROUPED_FEATURES.value.name,
        FMProperties.OR_GROUPS.value.name: FMProperties.GROUPED_FEATURES.value.name,
        FMProperties.MUTEX_GROUPS.value.name: FMProperties.GROUPED_FEATURES.value.name,
        FMProperties.CARDINALITY_GROUPS.value.name: FMProperties.GROUPED_FEATURES.value.name,
        FMProperties.SIMPLE_CONSTRAINTS.value.name: FMProperties.CROSS_TREE_CONSTRAINTS.value.name,
        FMProperties.REQUIRES_CONSTRAINTS.value.name: FMProperties.SIMPLE_CONSTRAINTS.value.name,
        FMProperties.EXCLUDES_CONSTRAINTS.value.name: FMProperties.SIMPLE_CONSTRAINTS.value.name,
        FMProperties.COMPLEX_CONSTRAINTS.value.name: FMProperties.CROSS_TREE_CONSTRAINTS.value.name,
        FMProperties.PSEUDO_COMPLEX_CONSTRAINTS.value.name: FMProperties.COMPLEX_CONSTRAINTS.value.name,
        FMProperties.STRICT_COMPLEX_CONSTRAINTS.value.name: FMProperties.COMPLEX_CONSTRAINTS.value.name,
        FMProperties.EXTRA_CONSTRAINT_REPRESENTATIVENESS.value.name: (FMProperties.FEATURES.value.name, 2)  # Specific precision
    }

def calculate_ratio(mean_values: Dict[str, float], numerator_name: str, denominator_name: str, precision: int = 4) -> Optional[float]:
    if numerator_name in mean_values and denominator_name in mean_values:
        return get_ratio_sizes(mean_values[numerator_name], mean_values[denominator_name], precision)
    return None

def process_files(extracted_files: list, extract_dir: str, zip_filename: str) -> Optional[Dict[str, Any]]:
    metrics_data = {}
    model_count = 0
    dataset_characterization = None

    futures = submit_file_processing_tasks(extracted_files, extract_dir)
    for future, file in futures.items():
        try:
            characterization = future.result()
            if characterization:
                model_count += 1
                dataset_characterization = initialize_characterization(dataset_characterization, characterization, metrics_data)
                update_metrics_data(metrics_data, characterization)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    if model_count > 0 and metrics_data:
        return generate_dataset_characterization_json(dataset_characterization, metrics_data, zip_filename)

    return None

def submit_file_processing_tasks(extracted_files: list, extract_dir: str):
    with ThreadPoolExecutor() as executor:
        return {executor.submit(process_single_file, os.path.join(extract_dir, file)): file for file in extracted_files if file.endswith('.uvl')}

def initialize_characterization(current_characterization, new_characterization, metrics_data):
    if current_characterization is None:
        current_characterization = new_characterization
        for m in new_characterization.metrics.get_metrics():
            metrics_data[m.property.name] = {'sizes': [], 'ratios': []}
    return current_characterization

def update_metrics_data(metrics_data, characterization):
    current_metrics = {m.property.name: m.size if m.size is not None else m.value for m in characterization.metrics.get_metrics()}
    current_ratios = {m.property.name: m.ratio for m in characterization.metrics.get_metrics() if m.ratio is not None}
    
    for key, value in current_metrics.items():
        metrics_data[key]['sizes'].append(value)
    
    for key, value in current_ratios.items():
        metrics_data[key]['ratios'].append(value)

def generate_dataset_characterization_json(dataset_characterization, metrics_data, zip_filename):
    dataset_characterization_json = dataset_characterization.to_json()
    dataset_characterization_json['metadata'][0]['value'] = zip_filename

    mean_values = calculate_mean_values(metrics_data)
    metrics_with_ratios = get_metrics_with_ratios()

    for metric in dataset_characterization_json['metrics']:
        name = metric['name']
        if name in metrics_data:
            assign_metric_stats(metric, metrics_data[name])

            # Calculate specific ratios if defined in metrics_with_ratios
            if name in metrics_with_ratios:
                ratio_info = metrics_with_ratios[name]
                if isinstance(ratio_info, tuple):
                    denominator_name, precision = ratio_info
                else:
                    denominator_name = ratio_info
                    precision = 4  # Default precision
                try:
                    metric['ratio'] = calculate_ratio(mean_values, name, denominator_name, precision)
                except KeyError as e:
                    print(f"Error calculating ratio for {name}: {e}")

    return dataset_characterization_json

def calculate_mean_values(metrics_data):
    mean_values = {}
    for name, data in metrics_data.items():
        values = data['sizes']
        if values:
            stats = calculate_stats(values)
            mean_values[name] = stats['mean']
            metrics_data[name]['stats'] = stats
    return mean_values

def calculate_stats(values):
    return {
        'mean': mean(values),
        'median': median(values),
        'min': min(values),
        'max': max(values)
    }

def assign_metric_stats(metric, data):
    sizes = data['sizes']
    if sizes:
        stats = calculate_stats(sizes)
        metric['size'] = stats['mean']
        metric['stats'] = stats