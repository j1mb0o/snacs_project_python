import os
import argparse
import subprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compress networks')
    parser.add_argument('--network', '-n', nargs='+', help='networks to compress')
    parser.add_argument('--random', '-r', action='store_true', help='random or not')
    arg = parser.parse_args()
    
    ROOT_DIR = os.path.dirname(os.path.relpath(__file__))

    # java_cmd = f"""java it.unimi.dsi.webgraph.BVGraph -g ArcListASCIIGraph 
    #                 {os.path.join(ROOT_DIR,"data",f"{input}.csv")} 
    #                 {os.path.join(ROOT_DIR,"compressed-networks",input)}""".split()
    # subprocess.run(java_cmd)
    # print(arg.network)
    if arg.network is None:
        for input in os.listdir(os.path.join(ROOT_DIR,"data")):
            if input.endswith(".csv"):
                print(input)
                java_cmd = f"""java it.unimi.dsi.webgraph.BVGraph -g ArcListASCIIGraph 
                                {os.path.join(ROOT_DIR,"data",f"{input}")} 
                                {os.path.join(ROOT_DIR,"compressed-networks",input)}""".split()
                subprocess.run(java_cmd)
            # print(input)