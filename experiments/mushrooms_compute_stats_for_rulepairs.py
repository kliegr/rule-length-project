import pandas as pd
import csv
import itertools
import re
import math
import hashlib
import detect
from decimal import Decimal
def detectAlgorithm(tag):
  if "manual" in tag:
    algorithm="manual"
  else:
    algorithm="InvertedHeuristics"
  return algorithm


dfLiteralImportance_poisonousTarget=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg855714_negative.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfLiteralImportance_edibleTarget=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg855714_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)

dfAttributeImportance=pd.read_csv('postprocessed_crowdflower_output/attributeimportance/customAgg876173.csv', delimiter=",", quoting=csv.QUOTE_ALL)
def getStats(rule): 
  if rule.endswith("{label=p}"):
    dfLiteralImportance=dfLiteralImportance_poisonousTarget
  else:
    if rule.endswith("{label=e}"):
      dfLiteralImportance=dfLiteralImportance_edibleTarget
    else:
      print "Error"
  literals=re.sub(r"} => {.*","",rule).replace("{","").split(",")
  attributes=re.sub(r"=[^,]","",re.sub(r"} => {.*","",rule).replace("{","")).split(",")
  LitImportance=dfLiteralImportance[dfLiteralImportance.orig.isin(literals)].rating.tolist()
  AttImportance=dfAttributeImportance[dfAttributeImportance.orig.isin(attributes)].rating.tolist()
  LitImpMax= max(LitImportance)
  LitImpMin= min(LitImportance)
  LitImpAvg= sum(LitImportance)/len(LitImportance)  
  LitImpSum= sum(LitImportance)
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

  literalLengths=[len(x) for x in  literals]
  LabelLengthMax= max(literalLengths)
  LabelLengthMin= min(literalLengths)
  LabelLengthAvg= sum(literalLengths)/len(literalLengths)  
  LabelLengthSum=sum(literalLengths)
  return LabelLengthMax,LabelLengthMin,LabelLengthAvg,LitImpMax,LitImpMin,LitImpAvg,LitImpSum,AttImpSum,AttImpMax,AttImpMin,AttImpAvg,LabelLengthSum

def stringToInt(text):
 return str(int(hashlib.md5(text).hexdigest(), 16))[0:5]

dfData=pd.read_csv('crowdflower_input/mushrooms.raw.csv', delimiter=",", quoting=csv.QUOTE_ALL)

#Since URI translation does not work reliably (old wikipedia)

#all invheur except one case, which is manual
dfData["algorithm"]= dfData.apply(lambda row: detectAlgorithm(row['tag']), axis=1)


dfData["r1LabelLengthMax"],dfData["r1LabelLengthMin"],dfData["r1LabelLengthAvg"],dfData["r1LitImpMax"],dfData["r1LitImpMin"],dfData["r1LitImpAvg"],dfData["r1LitImpSum"],dfData["r1AttImpSum"],dfData["r1AttImpMax"],dfData["r1AttImpMin"],dfData["r1AttImpAvg"],dfData["r1LabelLengthSum"]=zip(*dfData.r1.apply(getStats))
dfData["r2LabelLengthMax"],dfData["r2LabelLengthMin"],dfData["r2LabelLengthAvg"],dfData["r2LitImpMax"],dfData["r2LitImpMin"],dfData["r2LitImpAvg"],dfData["r2LitImpSum"],dfData["r2AttImpSum"],dfData["r2AttImpMax"],dfData["r2AttImpMin"],dfData["r2AttImpAvg"],dfData["r2LabelLengthSum"]=zip(*dfData.r2.apply(getStats))
dfData["r1id"]=dfData.r1.apply(stringToInt)
dfData["r2id"]=dfData.r2.apply(stringToInt)
dfData["rulerelation"]= dfData.apply(lambda row: detect.detectType(row['r1'], row['r2']), axis=1)

dfData=dfData.drop_duplicates(subset=["r1","r2"])

dfData.r1id = dfData.r1id.astype(str).replace("\.0","",regex=True)
dfData.r2id = dfData.r2id.astype(str).replace("\.0","",regex=True)

dfData.to_csv("postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv",quoting=csv.QUOTE_NONNUMERIC,index_label="id")