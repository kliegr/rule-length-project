import pandas as pd
import csv
import itertools
import re
from columndef import *
import math
from generate_text_traffic_translate import generateText
dfMap=pd.read_csv('crowdflower_input_literal_importance/traffic_accidents.name.map', delimiter=",", quoting=csv.QUOTE_ALL,index_col="id")

generatelinks=False

dfMap["used"]="False"
def linked(rule):  
  literals=re.findall("(?<=\<li>).*?(?=&nbsp;)",rule)
  for literal in literals :
    translation = dfMap[dfMap.friendly==literal]
    literalFriendly=re.sub("(?<=[a-z])(?=[A-Z0-9])"," ",literal)
    if len(translation)==1:
      if generatelinks:
        rule=rule.replace(literal,"<a href="+translation.uri.values[0]+' target="_blank">'+literalFriendly+"</a>")
        dfMap.loc[dfMap[dfMap.friendly==literal].index,"used"]="True"
      else:
        rule=rule.replace(literal,literalFriendly)
        dfMap.loc[dfMap[dfMap.friendly==literal].index,"used"]="True"
    else:
     print ('translation not found for', literal)
  return rule



 
def niceListOfInstances(string):
  return re.sub("[\[\]']","",string)
  
def generateClues(correct,coverage,label,confidence):
 if pd.isnull(correct) :
   return "" #this is the case for rules from Julius
 if float(confidence)==1.0:
  return "Following countries fall into all of the groups defined by the rule: <b>" +niceListOfInstances(correct)+ "</b><br/> All these countries have a risk of traffic accidents <b>" + label +"</b>"
 else:
  return "Following countries fall into all of the groups defined by the rule: <b>" +niceListOfInstances(coverage) + " </b><br/>For "  + str(correct.count(",")+1) + " of these countries ("+niceListOfInstances(correct) +"), the rule correctly predicts the rate of traffic accidents as <b>" + label + "</b>." 
 
 
dfData=pd.read_csv('crowdflower_input/traffic_accidents.raw.csv', delimiter=",", quoting=csv.QUOTE_ALL)


dfData.r1=generateText(dfData.r1)
dfData.r2=generateText(dfData.r2)

#Since URI translation does not work reliably (old wikipedia)

dfData.r1=dfData.r1.apply(linked)
dfData.r2=dfData.r2.apply(linked)

dfData['cluer1']=dfData.apply(lambda row: generateClues(row['r1correct'], row['r1coverage'], row['label'],row['r1conf']), axis=1)
dfData['cluer2']=dfData.apply(lambda row: generateClues(row['r2correct'], row['r2coverage'], row['label'],row['r2conf']), axis=1)

#all column names need to be lower case
columns.append("which_of_the_rules_do_you_find_as_more_plausible_gold")
columns.append("which_of_the_rules_do_you_find_as_more_plausible_gold_reason")
columns.append("_golden")

dfData["which_of_the_rules_do_you_find_as_more_plausible_gold"]=""
dfData["which_of_the_rules_do_you_find_as_more_plausible_gold_reason"]=""
dfData["_golden"]=""

dfData.loc[dfData.tag=="TEST","_golden"]="TRUE"
dfData.loc[dfData.tag=="TEST",["r1len","r2len","r1conf","r2conf","r1supp","r2supp","correctlyclassifiedoverlap","coverageoverlap","intersectionwholerule","literalintersectionlength","r1correct","r2correct","r1coverage","r2coverage"]]=""

dfData[dfData.tag!="TEST"].to_csv("crowdflower_input/traffic_accidents.csv",columns=columns,quoting=csv.QUOTE_NONNUMERIC,index_label="id")

#needs to be manually edited afterwards
dfData[dfData.tag=="TEST"].to_csv("testquestions/traffic.test",columns=columns,quoting=csv.QUOTE_NONNUMERIC,index_label="id")

dfMap.to_csv('crowdflower_input_literal_importance/traffic_accidents.name.map', delimiter=",", quoting=csv.QUOTE_ALL,index_label="id")
