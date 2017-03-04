import pandas as pd
import csv
import itertools
import re
import numpy as np
from columndef import *
np.random.seed(0)
df=pd.read_csv('output/movies.arules.pairs.filtered', delimiter=",", quoting=csv.QUOTE_ALL)
dfInvertedHeuristics=pd.read_csv('output/movies.invertedheuristics.pairs.filtered', delimiter=",", quoting=csv.QUOTE_ALL)
#duplicates are dropped in movies_filterRules.py
#dfInvertedHeuristics=dfInvertedHeuristics.drop_duplicates()

flag=True
def SwapR1R2(df):
 swappedNames=list(map(lambda x: str.replace(x,"r1","r1#"),list(df.columns)))
 swappedNames=list(map(lambda x: str.replace(x,"r2","r1"),swappedNames))
 swappedNames=list(map(lambda x: str.replace(x,"r1#","r2"),swappedNames))
 mapping=dict(zip(list(df.columns),swappedNames))
 return df.rename(columns=mapping)


dfInvertedHeuristics["tag"]="dfInvertedHeuristics"
df["tag"]="arules"

out=pd.concat([dfInvertedHeuristics,df], ignore_index=True)
out=out.reindex(np.random.permutation(out.index))
#take first have of rows and reverse r1 and r2. The reason is that length of r1 and r2 is not randomly distributed.
split=int(len(out)/2)
firstHalf=out[0:split]
firstHalf=SwapR1R2(firstHalf)
secondHalf=out[split:]
out=pd.concat([firstHalf,secondHalf], ignore_index=True)
out=out.reindex(np.random.permutation(out.index))

TESTQ=out.sample(n=20)
TESTQ["tag"]="TEST"
out=pd.concat([out,TESTQ],ignore_index=True)

#columns.append("tag")

#these fields are required by crowdflower
out.to_csv("output/movies.raw.csv",columns=columns,quoting=csv.QUOTE_NONNUMERIC,index_col="id")



