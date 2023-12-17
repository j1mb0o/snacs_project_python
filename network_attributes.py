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
    # TODO: Degree Centrality
    # Sum the outdegree divided by the number of nodes - 1
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
    """
        The average shortest path length in a graph, as computed by the `average_shortest_path_length` metric,
        can impact compression in several ways. The average shortest path length provides insights into the overall 
        "connectedness" or "distance" between nodes in the graph. Here are some ways in which this metric might impact graph compression:

    1. **Graph Structure:**
       - **Short Paths:** If the average shortest path length is small, it indicates that nodes in the graph are closely connected,
        and there are short paths between most pairs of nodes. Compression algorithms may exploit such local connectivity to represent the graph more efficiently.

       - **Long Paths:** Conversely, if the average shortest path length is large, 
       the graph may have more distant connections between nodes. 
       Compression algorithms might face challenges in efficiently representing long-range connections.
    """
    return rx.digraph_unweighted_average_shortest_path_length(G, disconnected=True)


def generate_attribute_report(name: str, random: bool = False):
    """
    Generate a report of the attributes of the graph
    """
    start = perf_counter()
    if random:
        G = rx.PyDiGraph.read_edge_list(f"random-graphs/{name}.csv")
    else:
        G = rx.PyDiGraph.read_edge_list(f"data/{name}.csv")
    print(name)
    # G = rx.PyDiGraph.read_edge_list(f"../data/{name}.tsv")
    
    print("Getting number of nodes")
    nodes = len(G.node_indices())

    print("Getting number of edges")
    edges = len(G.edge_indices())
    # exit()
    print("Getting density")
    dens = density(G)
    
    # print("Getting average out degree centrality")
    # avg_out = average_out_degree_centrality(G)
    
    # print("Getting average betweenness centrality")
    # avg_bet = average_betweenness_centrality(G)
    
    # print("Getting average closeness centrality")
    
    # g_nx = __convert_rustworkx_to_networkx(G)

    # avg_close = np.mean(list(nx.closeness_centrality(g_nx).values()))
    # avg_close = average_closeness_centrality(G)

    
    print("Getting global clustering coefficient")
    global_clust = global_clustering_coefficient(G)
    
    # print("Getting average shortest path length")
    # avg_short = average_shorted_path_length(G)

    end = perf_counter()

    graph_dict = {
        "Number of Nodes": nodes,
        "Number of Edges": edges,
        "Density": dens,
        # "Average Out Degree Centrality": avg_out,
        # "Average Betweenness Centrality": avg_bet,
        # "Average Closeness Centrality": avg_close,
        "Global Clustering Coefficient": global_clust,
        # "Average Shortest Path Length": avg_short,
        "Time": end - start 
    }
    
    df = pd.DataFrame(list(graph_dict.items()), columns=['Attribute', 'Value'])
    df.to_csv(f"{name}_final.csv", index=False)


if __name__ == "__main__":

    argparse = argparse.ArgumentParser(description='Analyse random graphs')
    argparse.add_argument('--random','-r', action='store_true', help='random or not')
    # generate_attribute_report('google')
    for file in os.listdir("random-graphs"):
        print(file)
        generate_attribute_report(file.split('.')[0], True)
    # generate_attribute_report('soc-gemsec-RO_like', True)