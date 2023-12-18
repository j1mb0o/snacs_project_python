import rustworkx as rx
import networkx as nx
from time import perf_counter
import pandas as pd
import numpy as np
import os
import argparse

def average_betweenness_centrality(G):
    return np.mean(list(rx.digraph_betweenness_centrality(G).values()))


def assortativity(G):
    g = __convert_rustworkx_to_networkx(G)
    return nx.degree_assortativity_coefficient(g)


def average_out_degree_centrality(G):
    n = len(G.node_indices())
    out_deg = {k: G.out_degree(k) / (n - 1) for k in G.node_indices()}
    return np.mean(list(out_deg.values()))


def density(G):
    # A dense graph might have more redundancy that can be exploited for compression
    n = len(G.nodes())
    m = len(G.edges())
    return m / (n * (n - 1))


def __convert_rustworkx_to_networkx(graph):
    """Convert a rustworkx PyGraph or PyDiGraph to a networkx graph."""
    edge_list = graph.edge_list()
    list_of_tuples = [(edge[0], edge[1]) for edge in edge_list]
    digraph = nx.DiGraph(list_of_tuples)
    return digraph


def average_closeness_centrality(G):
    return np.mean(list(rx.digraph_closeness_centrality(G).values()))


def global_clustering_coefficient(G):
    return rx.transitivity(G)


def average_shorted_path_length(G):
    return rx.digraph_unweighted_average_shortest_path_length(G, disconnected=True)


def generate_attribute_report(name: str, random: bool = False):
    """
    Generate a report of the attributes of the graph
    """
    OUT_DIR = 'random-networks-stats' if random else 'stats'
    start = perf_counter()
    if random:
        G = rx.PyDiGraph.read_edge_list(f"random-graphs/{name}.csv")
    else:
        G = rx.PyDiGraph.read_edge_list(f"data/{name}.csv")
    print(name)
    
    print("Getting number of nodes")
    nodes = len(G.node_indices())

    print("Getting number of edges")
    edges = len(G.edge_indices())
    print("Getting density")
    dens = density(G)
    
    print("Getting global clustering coefficient")
    global_clust = global_clustering_coefficient(G)

    print("Getting average shortest path length")
    avg_short = average_shorted_path_length(G)
    if not random:
        print("Getting average out degree centrality")
        avg_out = average_out_degree_centrality(G)
        
        print("Getting average betweenness centrality")
        avg_bet = average_betweenness_centrality(G)
        
        print("Getting average closeness centrality")
        
        g_nx = __convert_rustworkx_to_networkx(G)

        avg_close = np.mean(list(nx.closeness_centrality(g_nx).values()))
        avg_close = average_closeness_centrality(G)

        end = perf_counter()

        graph_dict = {
            "Number of Nodes": nodes,
            "Number of Edges": edges,
            "Density": dens,
            "Average Out Degree Centrality": avg_out,
            "Average Betweenness Centrality": avg_bet,
            "Average Closeness Centrality": avg_close,
            "Global Clustering Coefficient": global_clust,
            "Average Shortest Path Length": avg_short,
            "Time": end - start 
        }
    else:
        end = perf_counter()
        graph_dict = {
            "Number of Nodes": nodes,
            "Number of Edges": edges,
            "Density": dens,
            "Global Clustering Coefficient": global_clust,
            "Average Shortest Path Length": avg_short,
            "Time": end - start 
        }

    df = pd.DataFrame(list(graph_dict.items()), columns=None)
    df.to_csv(os.path.join(OUT_DIR,f"{name}.csv"), index=False)


def generate_whole_report(random: bool = False):
    dfs = []
    networks = ['foldoc_like', 'google_like', 'notre_dame_like', 'stanford_web_like'] if random else ['foldoc', 'google', 'notre_dame', 'stanford_web']
    DIR = 'random-graphs' if random else 'data'
    OUT_DIR = 'random-networks-stats' if random else 'stats' 
    
    for network in networks:
        df = pd.read_csv(os.path.join(DIR,f'{network}.csv') , header=None)
        df = df.transpose()
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        df["Network"] = network.capitalize()

        # Rearrange the columns to make 'Network' the first column
        df = df.reindex(['Network'] + list(df.columns[:-1]), axis=1)

        # Change the data type of certain columns to integer
        cols_to_int = ['Number of Nodes', 'Number of Edges']  # replace with your column names
        for col in cols_to_int:
            df[col] = df[col].astype(int).apply(lambda x: "{:,}".format(x))

        # Apply a prefix of 10e-4 to certain columns
        cols_to_scale = ['Density', 'Average Out Degree Centrality', 'Average Betweenness Centrality']  # replace with your column names
        for col in cols_to_scale:
            df[col] = df[col].apply(lambda x: "{:0.4e}".format(x))

        rest_cols = ["Average Closeness Centrality", "Global Clustering Coefficient", "Average Shortest Path Length"]
        for col in rest_cols:
            df[col] = df[col].apply(lambda x: "{:.4}".format(x))

        dfs.append(df)

    result = pd.concat(dfs)
    result.to_csv(os.path.join(OUT_DIR,'all-stats.csv') , index=False)
    result.to_latex(os.path.join(OUT_DIR,'all-stats.csv'), index=False)

if __name__ == "__main__":

    argparse = argparse.ArgumentParser(description='Analyse random graphs')
    argparse.add_argument('--random','-r', action='store_true', help='random or not')
    argparse.add_argument('--whole','-w', action='store_true', help='whole report')
    argparse.add_argument('--report','-rp', action='store_true', help='attribute report')
    args = argparse.parse_args()

    if args.whole:
        generate_whole_report(args.random)

    
    # generate_attribute_report('foldoc')
    if args.report:
        if args.random:
            for file in os.listdir("random-graphs"):
                print(file)
                generate_attribute_report(file.split('.')[0], args.random)
        else:
            for file in os.listdir("data"):
                print(file)
                generate_attribute_report(file.split('.')[0], args.random)