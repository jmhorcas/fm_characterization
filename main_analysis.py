import argparse

from alive_progress import alive_it

from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.fm_metamodel.operations import FMMetrics

from fm_characterization.fm_utils import METRICS_ORDER


def main(fm_filepath: str) -> None:
    print(f'Reading model {fm_filepath}...')
    fm_model = alive_it(UVLReader(fm_filepath).transform())

    print(f'Obtaining metrics from FM...')
    fm_metrics = alive_it(FMMetrics().execute(fm_model).get_result())

    print(f'Ordering metrics...')
    metrics_dict = {item['name']: item for item in fm_metrics}
    ordered_metrics = [metrics_dict[name] for name in METRICS_ORDER if name in metrics_dict]

    for metric in ordered_metrics:
        print(f'{" "*metric["level"]}'\
              f'{metric["name"]}: '\
              f'{metric["result"] if metric["size"] is None else ""}'\
              f'{metric["size"] if metric["size"] is not None else ""} '\
              f'({round(metric["ratio"]*100, 2) if metric["ratio"] is not None else ""}%)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Product Line analysis.')
    parser.add_argument(metavar='fm', dest='fm_filepath', type=str, help='Input feature model (.uvl).')
    args = parser.parse_args()

    main(args.fm_filepath)