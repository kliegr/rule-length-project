import csv
import pandas as pd
import scipy.stats
import sys
metricTuplesFull=[("r1len","r2len","lenDelta","lenRatio"),("r1DepthMax","r2DepthMax","DepthMaxDelta","DepthMaxRatio"),("r1DepthMin","r2DepthMin","DepthMinDelta","DepthMinRatio"),("r1LabelLengthSum","r2LabelLengthSum","LabelLengthSumDelta","LabelLengthSumRatio"),("r1LabelLengthMax","r2LabelLengthMax","LabelLengthMaxDelta","LabelLengthMaxRatio"),("r1LabelLengthMin","r2LabelLengthMin","LabelLengthMinDelta","LabelLengthMinRatio"),("r1LabelLengthAvg","r2LabelLengthAvg","LabelLengthAvgDelta","LabelLengthAvgRatio"),("r1minDistance","r2minDistance","MinDistanceDelta","MinDistanceRatio"),("r1maxDistance","r1maxDistance","MaxDistanceDelta","MaxDistanceRatio"),("r1mindepthLCS","r1mindepthLCS","MinDepthLCSDelta","MinDepthLCSRatio"),("r1PageRankMax","r2PageRankMax","PageRankMaxDelta","PageRankMaxRatio"),("r1PageRankMin","r2PageRankMin","PageRankMinDelta","PageRankMinRatio"),("r1PageRankAvg","r2PageRankAvg","PageRankAvgDelta","PageRankAvgRatio"),("r1conf","r2conf","ConfDelta","ConfRatio"),("r1supp","r2supp","SuppDelta","SuppRatio"),("r1LitImpMax","r2LitImpMax","LitImpMaxDelta","LitImpMaxRatio"),("r1LitImpMin","r2LitImpMin","LitImpMinDelta","LitImpMinRatio"),("r1LitImpAvg","r2LitImpAvg","LitImpAvgDelta","LitImpAvgRatio"),("r1AttImpMax","r2AttImpMax","AttImpMaxDelta","AttImpMaxRatio"),("r1AttImpMin","r2AttImpMin","AttImpMinDelta","AttImpMinRatio"),("r1AttImpAvg","r2AttImpAvg","AttImpAvgDelta","AttImpAvgRatio"),("r1AttImpSum","r2AttImpSum","AttImpSumDelta","AttImpSumRatio"),("r1LitImpSum","r2LitImpSum","LitImpSumDelta","LitImpSumRatio")]


if len(sys.argv)>1:
  infile=sys.argv[1]
else:
  infile="stats/datafiles/V2-e11-mushrooms.csv"
dfAll=pd.read_csv(infile, delimiter=",", quoting=csv.QUOTE_ALL,index_col=False)

## GENERATE CHISQUARE TABLES
print "========================= CHI SQUARE ANALYSIS ===================================="
print "=================================================================================="
for (r1Metric,r2Metric, deltaName,ratioName) in metricTuplesFull:
  #Extract rows with non-missing values of the current metric
  if not(r1Metric in dfAll.columns and r2Metric in dfAll.columns):
  	continue
  df = dfAll[dfAll[r1Metric].notnull() & dfAll[r2Metric].notnull()]
  print "=========================",r1Metric,r2Metric,"=================================="

  dfContingency = pd.DataFrame(columns=["lower","higher","samevalue"])
  #dfInvertedHeuristicsOther[(dfInvertedHeuristicsOther.r1len > dfInvertedHeuristicsOther.r2len) & (dfInvertedHeuristicsOther.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")]
  #dfInvertedHeuristicsOther[((dfInvertedHeuristicsOther.r1len > dfInvertedHeuristicsOther.r2len) & (dfInvertedHeuristicsOther.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")) | ((dfInvertedHeuristicsOther.r2len > dfInvertedHeuristicsOther.r1len) & (dfInvertedHeuristicsOther.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)"))].size

  dfContingency.loc["strong","higher"]=len(df[((df[r1Metric] > df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")) | ((df[r2Metric] > df[r1Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)"))])
  dfContingency.loc["weak","higher"]=len(df[((df[r1Metric] > df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)")) | ((df[r2Metric] > df[r1Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)"))])

  dfContingency.loc["strong","lower"]=len(df[((df[r1Metric] > df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)")) | ((df[r2Metric] > df[r1Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)"))])
  dfContingency.loc["weak","lower"]=len(df[((df[r1Metric] > df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)")) | ((df[r2Metric] > df[r1Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)"))])


  dfContingency.loc["strong","samevalue"]=len(df[((df[r1Metric] == df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)")) | ((df[r2Metric] == df[r1Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)"))])
  dfContingency.loc["weak","samevalue"]=len(df[((df[r1Metric] == df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)")) | ((df[r2Metric] == df[r1Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)"))])


  dfContingency.loc["nopreference","higher"]=0.5*len(df[((df[r1Metric] != df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="No preference"))])
  dfContingency.loc["nopreference","lower"]=0.5*len(df[((df[r1Metric] != df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="No preference"))])
  dfContingency.loc["nopreference","samevalue"]=len(df[((df[r1Metric] == df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="No preference"))])
  
  print dfContingency  
  print "CHECKSUM: Number of total rows: ",len(dfAll),"; Number of rows with non-missing input:", len(df), "; Sum of counts in contingency table:", sum(dfContingency.sum(1))
  try:
    if sum(dfContingency.samevalue)==0:
      dfContingency=dfContingency.drop("samevalue",1)    
      print "WARNING: samevalue column ignored (all zeros)"
    chi2, p, dof, expected = scipy.stats.chi2_contingency(dfContingency)
    print  "p value", str(p)
    with open('summary.csv', 'a') as file:
      file.write(infile+"," + r1Metric + " vs " + r2Metric + "," + str(chi2) + "," + str(p) +", strong - weak - no preference,"+ str(len(df)) + ",ChiSquare test on contingency table\n" )
  except  ValueError:
    print "There was a zero frequency"  
  
  print "\n== simpler version merging weak and strong to 'positive preference' =="
  dfContingency = pd.DataFrame(columns=["lower","higher","samevalue"])
  dfContingency.loc["positive pref","higher"]=len(df[((df[r1Metric] > df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)"))) | ((df[r2Metric] > df[r1Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)") | (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)")))])

  dfContingency.loc["positive pref","lower"]=len(df[((df[r1Metric] > df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)"))) | ((df[r2Metric] > df[r1Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)")))])    
  
  dfContingency.loc["positive pref","samevalue"]=len(df[(df[r1Metric] == df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)") | (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)") | (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)") | (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)"))])  
  dfContingency.loc["no preference","higher"]=0.5*len(df[((df[r1Metric] != df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="No preference"))])
  dfContingency.loc["no preference","lower"]=0.5*len(df[((df[r1Metric] != df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="No preference"))])
  dfContingency.loc["no preference","samevalue"]=len(df[((df[r1Metric] == df[r2Metric]) & (df.which_of_the_rules_do_you_find_as_more_plausible=="No preference"))])
  print dfContingency
  print "CHECKSUM: Number of total rows: ",len(dfAll),"; Number of rows with non-missing input:", len(df), "; Sum of counts in contingency table:", sum(dfContingency.sum(1))  
  
  
  print "Average difference: " + str((df[r1Metric] - df[r2Metric]).abs().mean())
  try:
    if sum(dfContingency.samevalue)==0:
      dfContingency=dfContingency.drop("samevalue",1)        
      print "WARNING:  samevalue column ignored (all zeros)"
    chi2, p, dof, expected = scipy.stats.chi2_contingency(dfContingency)
    with open('summary.csv', 'a') as file:
      file.write(infile+"," + r1Metric + " vs " + r2Metric + "," + str(chi2) + "," + str(p) +", positive - no preference,"+ str(len(df))+ ",ChiSquare test on contingency table\n" )
    print  "p value", str(p)
  except  ValueError:
    print "There was a zero frequency"
    
print "\nNote: 'lower/higher' means lower/higher value of the metric than the other rule. For no preference and different value of the metric for r1 and r2, the count is equally split between 'higher' and 'lower'."
