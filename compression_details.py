import os
import argparse
import pandas as pd
import rustworkx as rx


def generate_compression_report(random=False):

    stats = {"Network":[], "bits/node":[], "bits/node(compressed)":[], "Size reduction (%)":[] }
    DIR_DATA = "random-graphs" if random else "data"
    DIR_COMP = "random-compressed-networks" if random else "compressed-networks"
    OUTPUT_FILE = "random-networks-compression-statistics.csv" if random else "networks-compression-statistics.csv"
    OUTPUT_DIR = "compression-statistics" 

    for filename in os.listdir(DIR_DATA):
        print(filename.split('.')[0])
        g = rx.PyGraph.read_edge_list(os.path.join(DIR_DATA, filename))
        
        print('Number of nodes: ', len(g.node_indices()))
        stats["Network"].append(filename.split('.')[0])
        
        bits_node = os.path.getsize(os.path.join(DIR_DATA, filename)) * 8 / len(g.node_indices())
        stats["bits/node"].append(bits_node)
        
        bits_node_compressed = os.path.getsize(os.path.join(DIR_COMP,f"{filename}.graph")) * 8 / len(g.node_indices())
        stats["bits/node(compressed)"].append(bits_node_compressed)

        diff = (bits_node - bits_node_compressed) / bits_node * 100
        stats["Size reduction (%)"].append(diff)

    df = pd.DataFrame(stats)
    df.to_csv(os.path.join(OUTPUT_DIR,OUTPUT_FILE), index=False)
    df.to_latex(os.path.join(OUTPUT_DIR,OUTPUT_FILE.split('.')[0]+'.tex'), index=False)

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--random", help="Generate compression report for random networks", action="store_true")
    args = parser.parse_args()
    generate_compression_report(args.random)