import pandas as pd
import csv
import itertools
import re
import numpy as np
np.random.seed(0)
dfInvertedHeuristics=pd.read_csv('output/mushroom.invertedheuristics.pairs.filtered', delimiter=",", quoting=csv.QUOTE_ALL)

#manually designed incorrect rule
dfIncorrect=pd.read_csv('input/mushroom.incorrectrule.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfIncorrect["tag"]="manualIncorrect"
flag=True
flag=True
def SwapR1R2(df):
 swappedNames=list(map(lambda x: str.replace(x,"r1","r1#"),list(df.columns)))
 swappedNames=list(map(lambda x: str.replace(x,"r2","r1"),swappedNames))
 swappedNames=list(map(lambda x: str.replace(x,"r1#","r2"),swappedNames))
 mapping=dict(zip(list(df.columns),swappedNames))
 return df.rename(columns=mapping)

dfInvertedHeuristics["tag"]="dfInvertedHeuristics"

#there is only one such rule
dfInvertedHeuristicsSixDiffInRuleLen=dfInvertedHeuristics[(dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+6) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+6)]
dfInvertedHeuristicsSixDiffInRuleLen.is_copy=False
dfInvertedHeuristicsSixDiffInRuleLen.loc[:,"tag"]="dfInvertedHeuristicsSixDiffInRuleLen"

#all rules are poisonous
dfInvertedHeuristicsFiveDiffInRuleLen=dfInvertedHeuristics[(dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+5) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+5)].sample(n=2)
dfInvertedHeuristicsFiveDiffInRuleLen.is_copy=False
dfInvertedHeuristicsFiveDiffInRuleLen.loc[:,"tag"]="dfInvertedHeuristicsFiveDiffInRuleLen"

#select one poisonous and one edible
dfInvertedHeuristicsFourDiffInRuleLenP=dfInvertedHeuristics[((dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+4) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+4)) & (dfInvertedHeuristics.label=="p")].sample(n=1)
dfInvertedHeuristicsFourDiffInRuleLenP.is_copy=False
dfInvertedHeuristicsFourDiffInRuleLenP.loc[:,"tag"]="dfInvertedHeuristicsFourDiffInRuleLen"

dfInvertedHeuristicsFourDiffInRuleLenE=dfInvertedHeuristics[((dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+4) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+4)) & (dfInvertedHeuristics.label=="e")].sample(n=1)
dfInvertedHeuristicsFourDiffInRuleLenE.is_copy=False
dfInvertedHeuristicsFourDiffInRuleLenE.loc[:,"tag"]="dfInvertedHeuristicsFourDiffInRuleLen"

#select one poisonous and one edible
dfInvertedHeuristicsThreeDiffInRuleLenP=dfInvertedHeuristics[((dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+3) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+3)) & (dfInvertedHeuristics.label=="p")].sample(n=1)
dfInvertedHeuristicsThreeDiffInRuleLenP.is_copy=False
dfInvertedHeuristicsThreeDiffInRuleLenP.loc[:,"tag"]="dfInvertedHeuristicsThreeDiffInRuleLen"

dfInvertedHeuristicsThreeDiffInRuleLenE=dfInvertedHeuristics[((dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+3) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+3)) & (dfInvertedHeuristics.label=="e")].sample(n=1)
dfInvertedHeuristicsThreeDiffInRuleLenE.is_copy=False
dfInvertedHeuristicsThreeDiffInRuleLenE.loc[:,"tag"]="dfInvertedHeuristicsThreeDiffInRuleLen"

#select one poisonous and one edible
dfInvertedHeuristicsTwoDiffInRuleLenP=dfInvertedHeuristics[((dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+2) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+2)) & (dfInvertedHeuristics.label=="p")].sample(n=1)
dfInvertedHeuristicsTwoDiffInRuleLenP.is_copy=False
dfInvertedHeuristicsTwoDiffInRuleLenP.loc[:,"tag"]="dfInvertedHeuristicsTwoDiffInRuleLen"

dfInvertedHeuristicsTwoDiffInRuleLenE=dfInvertedHeuristics[((dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+2) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+2)) & (dfInvertedHeuristics.label=="e")].sample(n=1)
dfInvertedHeuristicsTwoDiffInRuleLenE.is_copy=False
dfInvertedHeuristicsTwoDiffInRuleLenE.loc[:,"tag"]="dfInvertedHeuristicsTwoDiffInRuleLen"

#there are only edible
dfInvertedHeuristicsOneDiffInRuleLen=dfInvertedHeuristics[(dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+1) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+1)].sample(n=2)
#otherwise there is warning: http://stackoverflow.com/questions/20625582/how-to-deal-with-this-pandas-warning
dfInvertedHeuristicsOneDiffInRuleLen.is_copy=False
dfInvertedHeuristicsOneDiffInRuleLen.loc[:,"tag"]="dfInvertedHeuristicsOneDiffInRuleLen"


out=pd.concat([dfInvertedHeuristicsOneDiffInRuleLen,dfInvertedHeuristicsTwoDiffInRuleLenE,dfInvertedHeuristicsTwoDiffInRuleLenP,dfInvertedHeuristicsThreeDiffInRuleLenE,dfInvertedHeuristicsThreeDiffInRuleLenP,dfInvertedHeuristicsFourDiffInRuleLenP,dfInvertedHeuristicsFourDiffInRuleLenE,dfInvertedHeuristicsFiveDiffInRuleLen,dfInvertedHeuristicsSixDiffInRuleLen,dfIncorrect])


#i=0
#for index, row in out.iterrows():  
#  row['r1'],row['r2'],row['r1len'],row['r2len']=splitpositionevenly(row['r1'],row['r2'],row['r1len'],row['r2len'])  

#shuffle rows, the results may still not be deterministic, if the input file is created by concurrent multithreading, which may garble some lines randomly
out=out.reindex(np.random.permutation(out.index))

#make sure rule legnth are evenly distributed between r1 and r2
split=int(len(out)/2)
firstHalf=out[0:split]
firstHalf=SwapR1R2(firstHalf)
secondHalf=out[split:]
out=pd.concat([firstHalf,secondHalf], ignore_index=True)
out=out.reindex(np.random.permutation(out.index))

if True:
  #The TEST rules are only suggestion, which needs further manual editing to be used as a test rule
  TESTQ=dfInvertedHeuristics.sample(n=20)
  TESTQ.is_copy=False
  TESTQ["tag"]="TEST"
  out=pd.concat([TESTQ,out])
#columns.append("tag")

out.to_csv("crowdflower_input/mushrooms.raw.csv",quoting=csv.QUOTE_NONNUMERIC)

