import pandas as pd
import csv
import itertools
import re
#from joblib import Parallel, delayed  
#import multiprocessing
from columndef import *

import sys, getopt


def processRulePairs(r1,r2):
  global i
  global ne
  global out
  global outfile
  global ruleQ
  global ruleQAntOnly
  i=i+1  
  r1Set=dfData.query(ruleQ[r1]).index #problem
  r2Set=dfData.query(ruleQ[r2]).index  
  r1SetCov=dfData.query(ruleQAntOnly[r1]).index
  r2SetCov=dfData.query(ruleQAntOnly[r2]).index  
  intersectionWholeRule=list(set(r1Set).intersection(set(r2Set)))
  intersectionAntecedent=list(set(r1SetCov).intersection(set(r2SetCov)))
  literalIntersection=list(set(ruleLiterals[r1]).intersection(set(ruleLiterals[r2])))
  #the rule pairs needs to have at least one instance common
  if len(intersectionWholeRule)>0:
   ne=ne+1
   #dice coefficient
#   ['r1id','r2id', 'r1len','r2len',"r1","r2", 'correctlyclassifiedoverlap','coverageoverlap', 'label','r1conf', 'r2conf','r1supp', 'r2supp','intersectionwholerule','literalintersectionlength','r1correct','r2correct','r1coverage','r2coverage','tag']
   out.loc[ne]=[r1,r2,ruleLen[r1],ruleLen[r2],df.rules[r1],df.rules[r2],dice(intersectionWholeRule,r1Set,r2Set),dice(intersectionAntecedent,r1SetCov,r2SetCov),ruleLabel[r1],df.confidence[r1],df.confidence[r2],df.support[r1],df.support[r2],list(dfData.iloc[intersectionWholeRule].Movie),len(literalIntersection),list(dfData.iloc[r1Set].Movie),list(dfData.iloc[r2Set].Movie),list(dfData.iloc[r1SetCov].Movie),list(dfData.iloc[r2SetCov].Movie),"","",""]     
  if divmod(i,1000)[1]==0:
   print ("i=",i)
   print ("len(out)",len(out))  
   #clear data frame
   out = pd.DataFrame(columns=columns)
  if divmod(ne,100)[1]==0:
   print ("ne=",ne)

def dice(intersection,set1,set2):
  return float(2*len(intersection))/float((len(set1)+len(set2)))

i=0
ne=0
df=pd.read_csv('output/movies.arules', delimiter=",", quoting=csv.QUOTE_ALL,usecols=["rules","support","confidence","lift"])
#replace dot in literal names (which is inserted by  R rule generation) with dash
#df["rules"]=df.rules.replace("(?<=[^1])[.](?=[^0])","-", regex=True)

#R prepends some column names with X, replace all those
#df["rules"]=df.rules.replace("(?<=[{,])X","", regex=True)

dfData=pd.read_csv('output/movies_shortened.csv', delimiter=",", quoting=csv.QUOTE_ALL)

ruleQ = df.rules.replace(["{} => {", "} => {","=","{","}",",","(?<=Label==)","$",'(?<===)([^\d\s]+)'],[""," and ", "==","",""," and ",'','','"\\1"'], regex=True)
ruleQAntOnly = df.rules.replace(["{} => {.*","} => {.*","=","{","}",",","^$",'(?<===)([^\d\s]+)'],["","", "==","",""," and " ,"index>-1",'"\\1"' ], regex=True)
ruleLabel=df.rules.replace([r".*Label=(good|bad).*$"],[r"\1"], regex=True)
ruleLen= ruleQAntOnly.str.count("==")
ruleLiterals=ruleQAntOnly.str.split(" and ")
#df.matchingRows=dfData.query(df.rules).index
  
#dfData.query(rulesAntOnly[1])
rulepairs=list(itertools.combinations(df.index,2))

out = pd.DataFrame(columns=columns)

outfile='output/movies.arules.pairs'

for r1,r2 in rulepairs:
  processRulePairs(r1,r2)
out.to_csv(outfile, header=True, quoting=csv.QUOTE_ALL)

