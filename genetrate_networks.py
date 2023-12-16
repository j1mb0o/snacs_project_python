import os
import rustworkx as rx
import argparse

def generate_random_graphs(networks:list):
    """
    Generate random graphs to mimic the real ones
    """
    if networks is None:
        for file in os.listdir(os.path.join(ROOT, 'data')):
            print(file)
            G = rx.PyDiGraph.read_edge_list(os.path.join(ROOT, 'data', file))
            G_nodes = len(G.node_indices())
            G_edges = len(G.edge_indices())

            print(f"Generating randomg graph to mimic {file.split('.')[0]} with {G_nodes:,} nodes and {G_edges:,} edges")
            rx.directed_gnm_random_graph(num_nodes=G_nodes, num_edges=G_edges, seed=42).write_edge_list(
                os.path.join(ROOT, 'random-graphs', f"{file.split('.')[0]}_like.csv")
            )
    else:
        for dataset in networks:
            print(dataset)
            G = rx.PyDiGraph.read_edge_list(os.path.join(ROOT, 'data', f"{dataset}.csv"))
            G_nodes = len(G.node_indices())
            G_edges = len(G.edge_indices())

            print(f"Generating randomg graph to mimic {dataset} with {G_nodes:,} nodes and {G_edges:,} edges")
            rx.directed_gnm_random_graph(num_nodes=G_nodes, num_edges=G_edges, seed=42).write_edge_list(
                os.path.join(ROOT, 'random-graphs', f"{dataset}_like.csv")
            )

if __name__ == '__main__':  

    argparse = argparse.ArgumentParser(description='Generate random graphs to mimic the real ones')
    argparse.add_argument('--dataset', 
                          '-d', 
                          nargs='+', 
                          default=None, 
                          choices=['google_like', 'random', 'stanford_like', 'berkstan_like', 'wikipedia_like', 'twitter_like'],
                        help='dataset name')
    arg = argparse.parse_args()

    ROOT = os.path.dirname(os.path.relpath(__file__))
    print(os.listdir(os.path.join(ROOT, 'data')))

    if arg.dataset is None:

        for file in os.listdir(os.path.join(ROOT, 'data')):
            print(file)
            G = rx.PyDiGraph.read_edge_list(os.path.join(ROOT, 'data', file))
            G_nodes = len(G.node_indices())
            G_edges = len(G.edge_indices())

            print(f"Generating randomg graph to mimic {file.split('.')[0]} with {G_nodes:,} nodes and {G_edges:,} edges")
            rx.directed_gnm_random_graph(num_nodes=G_nodes, num_edges=G_edges, seed=42).write_edge_list(
                os.path.join(ROOT, 'random-graphs', f"{file.split('.')[0]}_like.csv")
            )
    else:
        for dataset in arg.dataset:
            G = rx.PyDiGraph.read_edge_list(os.path.join(ROOT, 'data', f"{dataset}.csv"))
            G_nodes = len(G.node_indices())
            G_edges = len(G.edge_indices())

            print(f"Generating randomg graph to mimic {dataset} with {G_nodes:,} nodes and {G_edges:,} edges")
            rx.directed_gnm_random_graph(num_nodes=G_nodes, num_edges=G_edges, seed=42).write_edge_list(
                os.path.join(ROOT, 'random-graphs', f"{dataset}_like.csv")
            )