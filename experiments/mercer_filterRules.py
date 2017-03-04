#remove pairs of rules where any of the rules contains an attribute not linkable to Wikipedia
import pandas as pd
import csv
import hashlib

def stringToInt(text):
 return int(hashlib.md5(text).hexdigest(), 16)


#identify literals not mapped to Wikipedia
dfMap=pd.read_csv('output/mercer.name.map', delimiter=",", quoting=csv.QUOTE_ALL)
negativeList='|'.join(dfMap.friendly[dfMap.uri.isnull()])

#drop any arules pairs containing literals not mapped to Wikipedia
dfData=pd.read_csv('output/mercer.arules.pairs', delimiter=",", quoting=csv.QUOTE_ALL)
indexToDrop=dfData[dfData['r1'].str.contains(negativeList) | dfData['r2'].str.contains(negativeList)].index
dfData=dfData.drop(indexToDrop)
dfData.to_csv("output/mercer.arules.pairs.filtered",quoting=csv.QUOTE_NONNUMERIC)

#drop any inverted heuristics pairs containing literals not mapped to Wikipedia
dfData=pd.read_csv('input/mercer2015__inverted_rule_learner.csv', delimiter=",", quoting=csv.QUOTE_ALL)
indexToDrop=dfData[dfData['r1'].str.contains(negativeList) | dfData['r2'].str.contains(negativeList)].index
dfData=dfData.drop(indexToDrop)
dfData["r1id"]=dfData.r1.apply(stringToInt)
dfData["r2id"]=dfData.r2.apply(stringToInt)

#drop any inverted heuristics pairs with support of one
dfData=dfData.drop(dfData[(dfData['r1truepos']==1) & (dfData['r2truepos']==1)].index)


dfData.to_csv("output/mercer.invertedheuristics.pairs.filtered",quoting=csv.QUOTE_NONNUMERIC)
