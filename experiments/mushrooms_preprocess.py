import csv
import pandas as pd
df=pd.read_csv('input/mushroom_with_duplicate_entries.csv', delimiter=",", quoting=csv.QUOTE_ALL)
df=df.drop_duplicates(subset=["r1","r2"])
df.to_csv('output/mushroom.invertedheuristics.pairs.filtered', delimiter=",", quoting=csv.QUOTE_ALL,index=False)


