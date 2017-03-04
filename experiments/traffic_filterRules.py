#remove pairs of rules where any of the rules contains an attribute not linkable to Wikipedia
import pandas as pd
import csv
dfData=pd.read_csv('output/traffic_accidents_types.arules.pairs10per', delimiter=",", quoting=csv.QUOTE_ALL)
dfMap=pd.read_csv('crowdflower_input_literal_importance/traffic_accidents.name.map', delimiter=",", quoting=csv.QUOTE_ALL)
negativeList='|'.join(dfMap.friendly[dfMap.uri.isnull()])
indexToDrop=dfData[dfData['r1'].str.contains(negativeList) | dfData['r2'].str.contains(negativeList)].index
dfData=dfData.drop(indexToDrop)
dfData.to_csv("output/traffic_accidents_types.arules.pairs.filtered",quoting=csv.QUOTE_NONNUMERIC)