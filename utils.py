import requests
import zipfile
import shutil
import os
import subprocess
import pandas as pd

# Get the diretory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (one layer higher)
# ROOT_DIR = os.path.dirname(current_script_directory)


def download_and_decompress(filename):
    url = f"https://networks.skewed.de/net/{filename}/files/{filename}.csv.zip"
    destination = f"{filename}.csv.zip"

    if filename == "wikipedia":
        url = "https://networks.skewed.de/net/wikipedia_link/files/en.csv.zip"
        destination = "en.csv.zip"

    print(f"Downloading {filename}")
    # download_file(url, destination)
    response = requests.get(url, stream=True)
    with open(destination, "wb") as file:
        file.write(response.content)

    print(f"Unzipping {filename}")
    # unzip_file(destination, '.')

    with zipfile.ZipFile(destination, "r") as zip_ref:
        zip_ref.extract(zip_ref.namelist()[0], os.path.join(current_script_directory, "data"))

    shutil.move(
        os.path.join(current_script_directory, "data", "edges.csv"),
        os.path.join(current_script_directory, "data", f"{filename}.csv"),
    )
    os.remove(destination)


def compress_graph(input=None):
    # os.chdir(current_script_directory)
    # subprocess.run('pwd')

    if input is None:
        print("No input file specified")
        exit(1)
    else:
        # TODO: COMPLETE THE OUTPUT PATH
        java_cmd = f"""java it.unimi.dsi.webgraph.BVGraph -g ArcListASCIIGraph 
                    {os.path.join(current_script_directory,"data",f"{input}.csv")} 
                    {os.path.join(current_script_directory,"compressed_data",input)}""".split()
        subprocess.run(java_cmd)


if __name__ == "__main__":
    DATASETS = [
        "stanford_web",
        "google_web",
        "berkstan_web",
        "wikipedia",
        "twitter_social"
    ]

    compress_graph(DATASETS[0])
