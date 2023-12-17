import pandas as pd
import os
# df = pd.read_csv("data/soc-gemsec-RO.csv", sep='\t',header=None)

# print(df.head())
# df.sort_values(by=[0, 1], inplace=True)

# print(df.head(20))
# df.to_csv("data/soc-gemsec-RO.csv",sep='\t', header=False, index=False)

for file in os.listdir('random-graphs'):
    print(file)
    df = pd.read_csv(f"random-graphs/{file}", sep=' ',header=None)
    df.sort_values(by=[0, 1], inplace=True)
    df.to_csv("random-graphs/"+file,sep='\t', header=False, index=False)