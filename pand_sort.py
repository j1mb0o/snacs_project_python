import pandas as pd

df = pd.read_csv("data/soc-gemsec-RO.csv", sep='\t',header=None)

print(df.head())
df.sort_values(by=[0, 1], inplace=True)

print(df.head(20))
df.to_csv("data/soc-gemsec-RO.csv",sep='\t', header=False, index=False)