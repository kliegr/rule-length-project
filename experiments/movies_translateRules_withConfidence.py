import pandas as pd
import csv
import itertools
import re
from columndef import *
import math
dfMap=pd.read_csv('output/movies.name.map', delimiter=",", quoting=csv.QUOTE_ALL)

instanceCount=2000

import numpy as np

generatelinks=False

dfMap["used"]="False"
def linked(rule):  
  #ant=rule.replace(["{} => {.*","} => {.*","=","{","}",",","^$","=1.0"],["","", "==","",""," <li> " ,"index>-1","</li>"], regex=True)
  literals=re.findall("(?<=\<li>).*?(?=&nbsp;)",rule)
  for literal in literals :
    translation = dfMap[dfMap.friendly==literal]
    literalFriendly=re.sub("X([0-9]+s?)(.*)","\g<2> Released In \g<1>",literal)
    literalFriendly=re.sub("(?<=[a-z])(?=[A-Z0-9])"," ",literalFriendly)    
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

def generateText(column):
 return column.replace([" => {Label=","}$","{","}",",","=1.0"],["then the movie is rated as <b>","</b>" ,"if the movie falls into all of the following group(s) (simultaneously) <ul><li>", "&nbsp;</li></ul>", "&nbsp;<b>and</b> </li><li>",""], regex=True)
 
def countInstances(string):
  return re.sub("[\[\]']","",string)
  
def generateClues2(supportRel,label,confidence):
 supportAbs=supportRel*instanceCount
 coverageAbs=supportAbs/confidence
 return "In our data, there are <b>{0}</b> movies which match the conditions of this rule. Out of these <b>{2}</b> are predicted correctly as having {3} rating. The confidence of the rule is <b>{1}%</b>. <p>In other words, out of the <b>{0}</b> movies that match all the conditions of the rule, the number of movies that are rated as <b>{3}</b> as predicted by the rule is {2}. The rule thus predicts correctly the rating in  {2}/{0}={1} percent of cases.</p>".format(int(round(coverageAbs,0)),int(round(confidence*100,0)), int(round(supportAbs,0)),label) 

 
dfData=pd.read_csv('output/movies.pairs.selected', delimiter=",", quoting=csv.QUOTE_ALL)
dfJuliusInput=pd.read_csv('input/movies_inverted_rule_learner.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfJuliusInput=dfJuliusInput.drop_duplicates(subset=["r1","r2"])
dfInvertedWithIDs1 = pd.merge(dfData[dfData.tag=="dfInvertedHeuristics"],dfJuliusInput, left_on=["r1","r2"], right_on=["r2","r1"], how="inner",suffixes=('_x', ''))
dfInvertedWithIDs2 = pd.merge(dfData[dfData.tag=="dfInvertedHeuristics"],dfJuliusInput, left_on=["r1","r2"], right_on=["r1","r2"], how="inner",suffixes=('_x', ''))

def fillInMissingConf(rtext,existingSup):  
  #evaluates to true if not nan
  if existingSup == existingSup:
    return existingSup
  if len(dfJuliusInput[dfJuliusInput.r1==rtext])>0:
    return dfJuliusInput[dfJuliusInput.r1==rtext].r1sup.iloc[0]
  if len(dfJuliusInput[dfJuliusInput.r2==rtext]):
    return dfJuliusInput[dfJuliusInput.r2==rtext].r2sup.iloc[0]
  else:
    #this should not happen
    return ""

dfData['r1supp']=dfData.apply(lambda row: fillInMissingConf(row['r1'], row['r1supp']), axis=1)
dfData['r2supp']=dfData.apply(lambda row: fillInMissingConf(row['r2'], row['r2supp']), axis=1)

dfData.r1=generateText(dfData.r1)
dfData.r2=generateText(dfData.r2)

dfData.r1=dfData.r1.apply(linked)
dfData.r2=dfData.r2.apply(linked)

dfData['cluer1']=dfData.apply(lambda row: generateClues2(row['r1supp'], row['label'],row['r1conf']), axis=1)
dfData['cluer2']=dfData.apply(lambda row: generateClues2(row['r2supp'], row['label'],row['r2conf']), axis=1)

#all column names need to be lower case
columns.append("which_of_the_rules_do_you_find_as_more_plausible_gold")
columns.append("which_of_the_rules_do_you_find_as_more_plausible_gold_reason")
columns.append("_golden")

dfData["which_of_the_rules_do_you_find_as_more_plausible_gold"]=""
dfData["which_of_the_rules_do_you_find_as_more_plausible_gold_reason"]=""
dfData["_golden"]=""

dfData.loc[dfData.tag=="TEST","_golden"]="TRUE"
dfData.loc[dfData.tag=="TEST",["r1len","r2len","r1conf","r2conf","r1supp","r2supp","correctlyclassifiedoverlap","coverageoverlap","intersectionwholerule","literalintersectionlength","r1correct","r2correct","r1coverage","r2coverage"]]=""

dfData[dfData.tag!="TEST"].to_csv("output/movies.rules.pairs.translated.withconfidence.csv",columns=columns,quoting=csv.QUOTE_NONNUMERIC,index_label="id")

dfData[dfData.tag=="TEST"].to_csv("testquestions/movies.test.withconfidence.csv",columns=columns,quoting=csv.QUOTE_NONNUMERIC,index_label="id")

#appends the usage information for each literal
#dfMap.to_csv('output/movies.name.map', delimiter=",", quoting=csv.QUOTE_ALL,index_label="id")
