import os
import subprocess
# import graph_tool as gt
import argparse
from utils import download_and_decompress, compress_graph
from network_attributes import generate_attribute_report


# Get the directory of the current script
CURRENT_SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_SCRIPT_DIRECTORY)

# Get the parent directory (one layer higher)
# TODO: ADD TESTS

if __name__ == "__main__":
    DATASETS = ["stanford_web","google_web", "berkstan_web", "wikipedia","twitter_social"]
    # TODO: Add dataset not webgraph

    parser = argparse.ArgumentParser(description='Arguments to excecute exactly what you want.')
    parser.add_argument('--dataset', '-d', nargs='+', default=None, choices=DATASETS,
                        help='dataset name')
    parser.add_argument('--download', '-o', action='store_true', 
                        help='download dataset')
    parser.add_argument('--compress', '-c', action='store_true', default=False,
                        help='compress dataset')
    parser.add_argument('--report_dataset', '-p', action='store_true', default=False)
    parser.add_argument('--full_report', '-r', action='store_true', default=False)
    args = parser.parse_args()


    if not os.path.exists(os.path.join(CURRENT_SCRIPT_DIRECTORY, "data")):
        os.mkdir(os.path.join(CURRENT_SCRIPT_DIRECTORY, "data"))
    if not os.path.exists(os.path.join(CURRENT_SCRIPT_DIRECTORY, "stats")):
        os.mkdir(os.path.join(CURRENT_SCRIPT_DIRECTORY, "stats"))
        
    if args.dataset is None:
        data = ["stanford_web","google_web", "berkstan_web", "wikipedia","twitter_social"]
    else:
        data = args.dataset
    
    if args.download:
        for dataset in data:
            if not os.path.exists(os.path.join(CURRENT_SCRIPT_DIRECTORY, "data", f"{dataset}.csv")):
                download_and_decompress(dataset)
            else:
                print(f"{dataset} already exists skipping download!")

    if args.compress:
        for dataset in data:

            if  os.path.exists(os.path.join(CURRENT_SCRIPT_DIRECTORY, "compressed_data", f"{dataset}.graph")):
                print(f"{dataset} already exists skipping compression!")
                continue

            # First we want to check that the dataset is in a correct format (no comments, no headers, etc.)
            with open(os.path.join(ROOT_DIR,"data",f"{dataset}.csv") , 'r') as file:
                lines = file.readline()
                if lines[0] == "#":
                    print(f"{dataset} is not in the correct format yet\n please run sed -i '1d' {dataset}.csv to remove the header")
                    # TODO: Add another print to make them tab seperated
                    # time sed -i 's/,/\t/g' twitter_social.csv
                    exit(1)
                    # preprocess_dataset(dataset)
                else:
                    print(f"{dataset} is already in the correct format")

            compress_graph(dataset)

    if args.report_dataset:
        for dataset in data:
            if os.path.exists(os.path.join(CURRENT_SCRIPT_DIRECTORY, "data", f"{dataset}.csv")):
                print(f"Generating report for {dataset}")
                generate_attribute_report(dataset)
