import pandas as pd
import csv
import itertools
import re
import numpy as np
from columndef import *
np.random.seed(0)
# error_bad_lines=False - some input lines might be garbled due to parallel access to the file in processing
df=pd.read_csv('output/traffic_accidents_types.arules.pairs.filtered', delimiter=",", quoting=csv.QUOTE_ALL)
dfInvertedHeuristics=pd.read_csv('input/traffic_accidents_inverted_rule_learner.csv', delimiter=",", quoting=csv.QUOTE_ALL)

flag=True
def swapR1R2(df):
 swappedNames=list(map(lambda x: str.replace(x,"r1","r1#"),list(df.columns)))
 swappedNames=list(map(lambda x: str.replace(x,"r2","r1"),swappedNames))
 swappedNames=list(map(lambda x: str.replace(x,"r1#","r2"),swappedNames))
 mapping=dict(zip(list(df.columns),swappedNames))
 return df.rename(columns=mapping)

dfInvertedHeuristicsLargeDiffInRuleLen=dfInvertedHeuristics[(dfInvertedHeuristics.r1len>dfInvertedHeuristics.r2len+1) | (dfInvertedHeuristics.r2len>dfInvertedHeuristics.r1len+1) ]
#otherwise there is warning: http://stackoverflow.com/questions/20625582/how-to-deal-with-this-pandas-warning
dfInvertedHeuristicsLargeDiffInRuleLen.is_copy=False
dfInvertedHeuristicsLargeDiffInRuleLen.loc[:,"tag"]="dfInvertedHeuristicsLargeDiffInRuleLen"
dfInvertedHeuristicsOther=dfInvertedHeuristics[(dfInvertedHeuristics.r1len==dfInvertedHeuristics.r2len+1) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len+1) | (dfInvertedHeuristics.r2len==dfInvertedHeuristics.r1len)].sample(n=20-len(dfInvertedHeuristicsLargeDiffInRuleLen))
dfInvertedHeuristicsOther["tag"]="dfInvertedHeuristicsOther"

differentLengthRulesDisjunctAttH=df[(df.r1len!=df.r2len) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.literalintersectionlength==0.0) & (df.label=="high")].sample(n=5)
differentLengthRulesDisjunctAttH["tag"]="differentLengthRulesDisjunctAttH"
differentLengthRulesDisjunctAttL=df[(df.r1len!=df.r2len) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.literalintersectionlength==0.0) & (df.label=="low")].sample(n=5)
differentLengthRulesDisjunctAttL["tag"]="differentLengthRulesDisjunctAttL"
differentLengthRulesNeitherDisjunctNorSubsumingAttH=df[(df.r1len!=df.r2len) &(df.r1len!=df.literalintersectionlength) & (df.r2len!=df.literalintersectionlength) &  (df.correctlyclassifiedoverlap==1.0) & (df.coverageoverlap ==1.0) & (df.label=="high")].sample(n=5)
differentLengthRulesNeitherDisjunctNorSubsumingAttH["tag"]="differentLengthRulesNeitherDisjunctNorSubsumingAttH"
differentLengthRulesNeitherDisjunctNorSubsumingAttL=df[(df.r1len!=df.r2len) & (df.r1len!=df.literalintersectionlength) & (df.r2len!=df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) &  (df.label=="low")].sample(n=5)
differentLengthRulesNeitherDisjunctNorSubsumingAttL["tag"]="differentLengthRulesNeitherDisjunctNorSubsumingAttL"

#returns empty on 2 mil. rule set with coverage overlap required
#possible solution: use only differentLengthRulesR2subsumingR1AttH, differentLengthRulesR2subsumingR1AttL and  swap r1 and r2
#differentLengthRulesR1subsumingR2AttH=df[(df.r1len!=df.r2len) & (df.r2len==df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.label=="high")].sample(n=5)
#differentLengthRulesR1subsumingR2AttH["tag"]="differentLengthRulesR1subsumingR2AttH"
#returns empty on 2 mil. rule set with coverage overlap required
#differentLengthRulesR1subsumingR2AttL=df[(df.r1len!=df.r2len) & (df.r2len==df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.label=="low")].sample(n=5)
#differentLengthRulesR1subsumingR2AttL["tag"]="differentLengthRulesR1subsumingR2AttL"

differentLengthRulesR1subsumingR2AttH=df[(df.r1len!=df.r2len) & (df.r1len==df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0)  & (df.label=="high")].sample(n=5)
differentLengthRulesR1subsumingR2AttH=swapR1R2(differentLengthRulesR1subsumingR2AttH)
differentLengthRulesR1subsumingR2AttH["tag"]="differentLengthRulesR1subsumingR2AttH"

differentLengthRulesR1subsumingR2AttL=df[(df.r1len!=df.r2len) & (df.r1len==df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.label=="low")].sample(n=5)
differentLengthRulesR1subsumingR2AttL=swapR1R2(differentLengthRulesR1subsumingR2AttL)
differentLengthRulesR1subsumingR2AttL["tag"]="differentLengthRulesR1subsumingR2AttL"

differentLengthRulesR2subsumingR1AttH=df[(df.r1len!=df.r2len) & (df.r1len==df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0)  & (df.label=="high")].sample(n=5)
differentLengthRulesR2subsumingR1AttH["tag"]="differentLengthRulesR2subsumingR1AttH"
differentLengthRulesR2subsumingR1AttL=df[(df.r1len!=df.r2len) & (df.r1len==df.literalintersectionlength) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.label=="low")].sample(n=5)
differentLengthRulesR2subsumingR1AttL["tag"]="differentLengthRulesR2subsumingR1AttL"


sameLengthRulesDisjunctAttH=df[(df.r1len==df.r2len) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.literalintersectionlength==0.0) & (df.label=="high")].sample(n=5)
sameLengthRulesDisjunctAttH["tag"]="sameLengthRulesDisjunctAttH"
sameLengthRulesDisjunctAttL=df[(df.r1len==df.r2len) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.literalintersectionlength==0.0) & (df.label=="low")].sample(n=5)
sameLengthRulesDisjunctAttL["tag"]="sameLengthRulesDisjunctAttL"
sameLengthRulesNonDisjunctAttH=df[(df.r1len==df.r2len) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.literalintersectionlength>0.0) & (df.label=="high")].sample(n=5)
sameLengthRulesNonDisjunctAttH["tag"]="sameLengthRulesNonDisjunctAttH"
sameLengthRulesNonDisjunctAttL=df[(df.r1len==df.r2len) & (df.correctlyclassifiedoverlap==1.0) &  (df.coverageoverlap ==1.0) & (df.literalintersectionlength>0.0) & (df.label=="low")].sample(n=5)
sameLengthRulesNonDisjunctAttL["tag"]="sameLengthRulesNonDisjunctAttL"

out=pd.concat([differentLengthRulesDisjunctAttH,differentLengthRulesDisjunctAttL,differentLengthRulesNeitherDisjunctNorSubsumingAttH,differentLengthRulesNeitherDisjunctNorSubsumingAttL,differentLengthRulesR1subsumingR2AttH,differentLengthRulesR1subsumingR2AttL,differentLengthRulesR2subsumingR1AttH,differentLengthRulesR2subsumingR1AttL,sameLengthRulesDisjunctAttH,sameLengthRulesDisjunctAttL,sameLengthRulesNonDisjunctAttH,sameLengthRulesNonDisjunctAttL,dfInvertedHeuristicsLargeDiffInRuleLen,dfInvertedHeuristicsOther])


#i=0
#for index, row in out.iterrows():  
#  row['r1'],row['r2'],row['r1len'],row['r2len']=splitpositionevenly(row['r1'],row['r2'],row['r1len'],row['r2len'])  

#shuffle rows, the results may still not be deterministic, if the input file is created by concurrent multithreading, which may garble some lines randomly

out=out.reindex(np.random.permutation(out.index))
if False:
  TESTQ=df.sample(n=20)
  TESTQ["tag"]="TEST"
  out=pd.concat(TESTQ,out)
#columns.append("tag")

#these fields are required by crowdflower
out.to_csv("crowflower_input/traffic_accidents.raw.csv",columns=columns,quoting=csv.QUOTE_NONNUMERIC)
