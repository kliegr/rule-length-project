import pandas as pd
import csv
import itertools
import re
from columndef import *
import numpy as np
import math
import detect
from generate_text_traffic_translate import generateText
import hashlib

dfMap=pd.read_csv('literal_linked_stats/traffic_accidents.name.with_pagerank.csv', delimiter=",", quoting=csv.QUOTE_ALL,index_col="id")

dfMap.friendly.replace("-speakingCountriesAnd","speakingCountriesAnd",regex=True)

dfMapDepth=pd.read_csv('literal_linked_stats/traffic_accidents.name.with_depth.csv', delimiter=",", quoting=csv.QUOTE_ALL,index_col="id")
dfMapDepth.friendly.replace("-speakingCountriesAnd","speakingCountriesAnd",regex=True)
dfPairwise=pd.read_csv('literal_linked_stats/traffic_accidents_pairwise.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfPairwise.name1=dfPairwise.name1.replace("http://dbpedia.org/class/yago/","",regex=True).replace("-speakingCountriesAnd","speakingCountriesAnd",regex=True)
dfPairwise.name2=dfPairwise.name2.replace("http://dbpedia.org/class/yago/","",regex=True).replace("-speakingCountriesAnd","speakingCountriesAnd",regex=True)

dfLiteralImportance_highTarget=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg842634_negative.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfLiteralImportance_lowTarget=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg842634_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)

dfAttributeImportance=pd.read_csv('postprocessed_crowdflower_output/attributeimportance/customAgg876663.csv', delimiter=",", quoting=csv.QUOTE_ALL)

#add ids to dfAttributeImportance
dfAttributeImportanceTranslation=pd.read_csv('crowdflower_input_literal_importance/traffic_accidents.LiteralImportance.Annotation.Input.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfAttributeImportanceTranslation=dfAttributeImportanceTranslation.drop_duplicates(subset=["friendly","friendlyshow"])
for index, row in dfAttributeImportanceTranslation.iterrows():
  dfAttributeImportance["machine_readable_values"]=dfAttributeImportance["machine_readable_values"].str.replace(row["friendlyshow"],row["friendly"])


def updateInvHeurIDs(df):
 df_ = pd.DataFrame()
 df_["r1id"]=generateText(df[df.algorithm=="InvertedHeuristics"].r1string).apply(stringToInt)
 df_["r2id"]=generateText(df[df.algorithm=="InvertedHeuristics"].r2string).apply(stringToInt)
 df.update(df_)
 return df

def stringToInt(text):
  #return int(hashlib.md5(text).hexdigest(), 16)
  return str(int(hashlib.md5(text).hexdigest(), 16))[0:5]

def getStats(rule):  
  if rule.endswith("{Label=high}"):
    dfLiteralImportance=dfLiteralImportance_highTarget
  else:
    if rule.endswith("{Label=low}"):
      dfLiteralImportance=dfLiteralImportance_lowTarget
    else:
      print "Error"

  #ant=rule.replace(["{} => {.*","} => {.*","=","{","}",",","^$","=1.0"],["","", "==","",""," <li> " ,"index>-1","</li>"], regex=True) 
  literals=re.sub(r"} => {.*","",rule).replace("=1.0","").replace("{","").split(",")

  attribute_regex=re.sub(r"} => {.*","",rule).replace("=1.0","").replace("{","").replace(",","|")
  AttImportance=dfAttributeImportance[dfAttributeImportance.machine_readable_values.str.contains(attribute_regex)].rating.tolist()

  if len(AttImportance)==0:
    print (str(literals) + "\nWARNING literals  in stat file missing\n")
    AttImpMax= Decimal('NaN')
    AttImpMin= Decimal('NaN')
    AttImpAvg= Decimal('NaN')
    AttImpSum= Decimal('NaN')
  else:
    AttImpMax= max(AttImportance)
    AttImpMin= min(AttImportance)
    AttImpAvg= sum(AttImportance)/len(AttImportance)      
    AttImpSum= sum(AttImportance)


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
  LabelLengthSum=sum(literalLengths)
  LitImportance=dfLiteralImportance[dfLiteralImportance.friendly.isin(literals)].rating.tolist()
  if LitImportance:
    LitImpMax= max(LitImportance)
    LitImpMin= min(LitImportance)
    LitImpAvg= sum(LitImportance)/len(LitImportance)  
    LitImpSum= sum(LitImportance)
  else:
    LitImpMax=np.nan
    LitImpMin=np.nan
    LitImpAvg=np.nan  
    LitImpSum=np.nan  
  if len(literals)==1:
    minDistance=0.0
    maxDistance=0.0
    mindepthLCS=0.0
  else: 
    literalPairs=list(itertools.combinations(literals,2))
    minDistance=min([float(dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].minDistance) for x in literalPairs])
    maxDistance=max([float(dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].maxDistance) for x in literalPairs])
    #avgDistance=[dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].avgDistance for x in literalPairs]
    mindepthLCS=min([float(dfPairwise[(dfPairwise.name1== x[0]) & (dfPairwise.name2== x[1])].depthLCS) for x in literalPairs])
    #TypeError cast by float() and ValueError by min/max when the literal is not find in the key file
  return DepthMax,DepthMin,LabelLengthMax,LabelLengthMin,LabelLengthAvg,minDistance,maxDistance,mindepthLCS,PageRankMax,PageRankMin,PageRankAvg,LitImpMax,LitImpMin,LitImpAvg,LitImpSum,AttImpSum,AttImpMax,AttImpMin,AttImpAvg,LabelLengthSum

#this is a source list of rules with machine readable descriptions
dfData=pd.read_csv('crowdflower_input/traffic_accidents.raw.csv', delimiter=",", quoting=csv.QUOTE_ALL)

#load original "source" file with rules translated to strings
dfDataAddInfo=pd.read_csv('crowdflower_input/traffic_accidents.csv', delimiter=",", quoting=csv.QUOTE_ALL, usecols=["r1","r2"])

#rename columns with human readable description of rules 
dfDataAddInfo = dfDataAddInfo.rename(columns={'r1': 'r1string', 'r2': 'r2string'})

dfData=pd.concat([dfData,dfDataAddInfo],axis=1)


dfData["rulerelation"]= dfData.apply(lambda row: detect.detectType(row['r1'], row['r2']), axis=1)
dfData["algorithm"]= dfData.apply(lambda row: detect.detectAlgorithm(row['tag']), axis=1)

#ids for  inverted heuristic pairs were not set
dfData=updateInvHeurIDs(dfData)
#Since URI translation does not work reliably (old wikipedia)


dfData["r1DepthMax"],dfData["r1DepthMin"],dfData["r1LabelLengthMax"],dfData["r1LabelLengthMin"],dfData["r1LabelLengthAvg"],dfData["r1minDistance"],dfData["r1maxDistance"],dfData["r1mindepthLCS"],dfData["r1PageRankMax"],dfData["r1PageRankMin"],dfData["r1PageRankAvg"],dfData["r1LitImpMax"],dfData["r1LitImpMin"],dfData["r1LitImpAvg"],dfData["r1LitImpSum"],dfData["r1AttImpSum"],dfData["r1AttImpMax"],dfData["r1AttImpMin"],dfData["r1AttImpAvg"],dfData["r1LabelLengthSum"]=zip(*dfData.r1.apply(getStats))
dfData["r2DepthMax"],dfData["r2DepthMin"],dfData["r2LabelLengthMax"],dfData["r2LabelLengthMin"],dfData["r2LabelLengthAvg"],dfData["r2minDistance"],dfData["r2maxDistance"],dfData["r2mindepthLCS"],dfData["r2PageRankMax"],dfData["r2PageRankMin"],dfData["r2PageRankAvg"],dfData["r2LitImpMax"],dfData["r2LitImpMin"],dfData["r2LitImpAvg"],dfData["r2LitImpSum"],dfData["r2AttImpSum"],dfData["r2AttImpMax"],dfData["r2AttImpMin"],dfData["r2AttImpAvg"],dfData["r2LabelLengthSum"]=zip(*dfData.r2.apply(getStats))
dfData=dfData.drop_duplicates(subset=["r1","r2"])
dfData.r1id = dfData.r1id.astype(str).replace("\.0","",regex=True)
dfData.r2id = dfData.r2id.astype(str).replace("\.0","",regex=True)
dfData.to_csv("postprocessed_crowdflower_output/traffic_accidents_types.arules.pairs.with_stats.csv",quoting=csv.QUOTE_NONNUMERIC,index_label="id")