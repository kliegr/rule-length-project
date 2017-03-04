import pandas as pd
import csv
import itertools
import re
from columndef import *
import math
import detect
dfPageRank=pd.read_csv('literal_linked_stats/movies.name.pagerank.csv', delimiter="\t", quoting=csv.QUOTE_ALL)
dfPageRank.uri=dfPageRank.uri.replace("http://dbpedia.org/resource/","https://en.wikipedia.org/wiki/", regex=True)

dfOrigFile=pd.read_csv('literal_linked_stats/movies.name.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfMap=pd.merge(dfPageRank,dfOrigFile, how="inner",left_on="uri",right_on="uri")

dfMap.friendly=dfMap.friendly.replace("-","",regex=True)


dfMapDepth=pd.read_csv('literal_linked_stats/movies.name.with_depth.csv', delimiter=",", quoting=csv.QUOTE_ALL,index_col="id")
dfMapDepth.friendly.replace("-","",regex=True,inplace=True)
dfPairwise=pd.read_csv('literal_linked_stats/movies.name.pairwise.csv', delimiter=",", quoting=csv.QUOTE_ALL)

dfPairwise.name1=dfPairwise.name1.replace("http://dbpedia.org/class/yago/","",regex=True).replace("-","",regex=True).replace("^(?=\d)","X",regex=True)
dfPairwise.name2=dfPairwise.name2.replace("http://dbpedia.org/class/yago/","",regex=True).replace("-","",regex=True).replace("^(?=\d)","X",regex=True)


#dfLiteralImportance=pd.read_csv('crowdflower_output/literalimportance/customAgg842577.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfLiteralImportance_badTarget=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg842577_negative.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfLiteralImportance_goodTarget=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg842577_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)

def fixIDs_MOV(df):
 df.r1id=df.r1id.str[0:5]
 df.r2id=df.r2id.str[0:5]
 dfData.r1id = dfData.r1id.astype(str).replace("\.0","",regex=True)
 dfData.r2id = dfData.r2id.astype(str).replace("\.0","",regex=True)
 return df


def getStats(rule):  
  if rule.endswith("{Label=good}"):
    dfLiteralImportance=dfLiteralImportance_goodTarget
  else:
    if rule.endswith("{Label=bad}"):
      dfLiteralImportance=dfLiteralImportance_badTarget
    else:
      print "Error"

  #ant=rule.replace(["{} => {.*","} => {.*","=","{","}",",","^$","=1.0"],["","", "==","",""," <li> " ,"index>-1","</li>"], regex=True) 
  literals=re.sub(r"} => {.*","",rule).replace("=1.0","").replace("{","").split(",")
  #max(dfMap[dfMap.friendly.isin(literals)].pagerank)
  PageRanks=dfMap[dfMap.friendly.isin(literals)].pagerank.tolist()
  PageRankMax= max(PageRanks)
  PageRankMin= min(PageRanks)
  PageRankAvg= sum(PageRanks)/len(PageRanks)  
  Depths=dfMapDepth[dfMapDepth.friendly.isin(literals)].depth.tolist()
  DepthMax= max(Depths)
  DepthMin= min(Depths)  
  literalLengths=[len(x) for x in  literals]
  LabelLengthMax= max(literalLengths)
  LabelLengthMin= min(literalLengths)
  LabelLengthAvg= sum(literalLengths)/len(literalLengths)  
  LabelLengthSum= sum(literalLengths)
  
    
  LitImportance=dfLiteralImportance[dfLiteralImportance.friendly.isin(literals)].rating.tolist()
  LitImpMax= max(LitImportance)
  LitImpMin= min(LitImportance)
  LitImpAvg= sum(LitImportance)/len(LitImportance)  
  LitImpSum= sum(LitImportance)
  if len(literals)==1:
    minDistance=0.0
    maxDistance=0.0
    mindepthLCS=0.0
  else: 
    literalPairs=list(itertools.combinations(literals,2))
    try:
      minDistance=min([float(dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].minDistance) for x in literalPairs])
    except TypeError:
      print x[0]
      print x[1]
      raise
    maxDistance=max([float(dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].maxDistance) for x in literalPairs])
    #avgDistance=[dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].avgDistance for x in literalPairs]
    mindepthLCS=min([float(dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].depthLCS) for x in literalPairs])
    #TypeError cast by float() and ValueError by min/max when the literal is not find in the key file
  return DepthMax,DepthMin,LabelLengthMax,LabelLengthMin,LabelLengthAvg,minDistance,maxDistance,mindepthLCS,PageRankMax,PageRankMin,PageRankAvg,LitImpMax,LitImpMin,LitImpAvg,LitImpSum,LabelLengthSum


dfData=pd.read_csv('crowdflower_input/movies.raw.csv', delimiter=",", quoting=csv.QUOTE_ALL,dtype={"r1id":"str","r2id":"str"})
dfData["rulerelation"]= dfData.apply(lambda row: detect.detectType(row['r1'], row['r2']), axis=1)
dfData["algorithm"]= dfData.apply(lambda row: detect.detectAlgorithm(row['tag']), axis=1)

#Since URI translation does not work reliably (old wikipedia)

dfData["r1DepthMax"],dfData["r1DepthMin"],dfData["r1LabelLengthMax"],dfData["r1LabelLengthMin"],dfData["r1LabelLengthAvg"],dfData["r1minDistance"],dfData["r1maxDistance"],dfData["r1mindepthLCS"],dfData["r1PageRankMax"],dfData["r1PageRankMin"],dfData["r1PageRankAvg"],dfData["r1LitImpMax"],dfData["r1LitImpMin"],dfData["r1LitImpAvg"],dfData["r1LitImpSum"],dfData["r1LabelLengthSum"]=zip(*dfData.r1.apply(getStats))
dfData["r2DepthMax"],dfData["r2DepthMin"],dfData["r2LabelLengthMax"],dfData["r2LabelLengthMin"],dfData["r2LabelLengthAvg"],dfData["r2minDistance"],dfData["r2maxDistance"],dfData["r2mindepthLCS"],dfData["r2PageRankMax"],dfData["r2PageRankMin"],dfData["r2PageRankAvg"],dfData["r2LitImpMax"],dfData["r2LitImpMin"],dfData["r2LitImpAvg"],dfData["r2LitImpSum"],dfData["r2LabelLengthSum"]=zip(*dfData.r2.apply(getStats))
dfData=dfData.drop_duplicates(subset=["r1","r2"])

dfData=fixIDs_MOV(dfData)
#dfData=dfData.drop_duplicates(subset=["r1id","r2id"])
dfData.to_csv("postprocessed_crowdflower_output/movies.pairs.with_stats.csv",quoting=csv.QUOTE_NONNUMERIC,index_label="id")



