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
        print(e)
        pass
    try:
        return UVLReader(filename).transform()
    except Exception as e:
        print(e)
        pass
    try:
        return FeatureIDEReader(filename).transform()
    except Exception as e:
        print(e)
        pass
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

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_single_file, os.path.join(extract_dir, file)): file for file in extracted_files if file.endswith('.uvl')}
        
        for future in as_completed(futures):
            try:
                characterization = future.result()
                if characterization:
                    model_count += 1
                    if dataset_characterization is None:
                        dataset_characterization = characterization
                        # Initialize metrics data
                        for m in characterization.metrics.get_metrics():
                            metrics_data[m.property.name] = {'sizes': [], 'ratios': []}
                    
                    current_metrics = {m.property.name: m.size if m.size is not None else m.value for m in characterization.metrics.get_metrics()}
                    current_ratios = {m.property.name: m.ratio for m in characterization.metrics.get_metrics() if m.ratio is not None}
                    
                    # Store size metrics
                    for key, value in current_metrics.items():
                        metrics_data[key]['sizes'].append(value)
                    
                    # Store ratio metrics
                    for key, value in current_ratios.items():
                        metrics_data[key]['ratios'].append(value)
            except Exception as e:
                print(f"Error processing file {futures[future]}: {e}")

    if model_count > 0 and metrics_data:
        dataset_characterization_json = dataset_characterization.to_json()
        dataset_characterization_json['metadata'][0]['value'] = zip_filename

        # Calculate mean values for each metric
        mean_values = {}
        for name, data in metrics_data.items():
            values = data['sizes']
            if values:
                mean_value = mean(values)
                mean_values[name] = mean_value
                metrics_data[name]['stats'] = {
                    'mean': mean_value,
                    'median': median(values),
                    'min': min(values),
                    'max': max(values)
                }

        metrics_with_ratios = get_metrics_with_ratios()

        # Calculate and assign metrics and ratios
        for metric in dataset_characterization_json['metrics']:
            name = metric['name']
            if name in metrics_data:
                sizes = metrics_data[name]['sizes']
                metric['size'] = mean(sizes) if sizes else None
                metric['stats'] = {
                    'mean': mean(sizes) if sizes else None,
                    'median': median(sizes) if sizes else None,
                    'min': min(sizes) if sizes else None,
                    'max': max(sizes) if sizes else None
                }

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

    return None