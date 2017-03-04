import csv
import pandas as pd
import scipy.stats
import sys

if len(sys.argv)>1:
  infile=sys.argv[1]
else:
  infile="stats/datafiles/V2-e17-mushrooms-correctVsIncorrect.csv"
df=pd.read_csv(infile, delimiter=",", quoting=csv.QUOTE_ALL,index_col=False)

## GENERATE CHISQUARE TABLES
print "========================= CHI SQUARE ANALYSIS ===================================="
print "=================================================================================="

r1Metric="r1len"
r2Metric="r2len"
print "\n== simpler version merging weak and strong to 'positive preference' =="
dfContingency = pd.DataFrame(columns=["correct","incorrect"])
dfContingency.loc["positive pref-longer","correct"]=len(df[((df["tag"] == "dfInvertedHeuristicsSixDiffInRuleLen") & (df[r1Metric] > df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)"))) | ((df[r2Metric] > df[r1Metric]) & (df["tag"] == "dfInvertedHeuristicsSixDiffInRuleLen") & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)") | (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)")))])
dfContingency.loc["positive pref-shorter","correct"]=len(df[((df["tag"] == "dfInvertedHeuristicsSixDiffInRuleLen") & (df[r1Metric] > df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)"))) | ((df[r2Metric] > df[r1Metric]) & (df["tag"] == "dfInvertedHeuristicsSixDiffInRuleLen") & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)")))])    
dfContingency.loc["positive pref-longer","incorrect"]=len(df[((df["tag"] == "manualIncorrect") & (df[r1Metric] > df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)"))) | ((df[r2Metric] > df[r1Metric]) & (df["tag"] == "manualIncorrect") & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)") | (df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)")))])
dfContingency.loc["positive pref-shorter","incorrect"]=len(df[((df["tag"] == "manualIncorrect") & (df[r1Metric] > df[r2Metric]) & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 2 (weak preference)"))) | ((df[r2Metric] > df[r1Metric]) & (df["tag"] == "manualIncorrect") & ((df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (strong preference)")|(df.which_of_the_rules_do_you_find_as_more_plausible=="Rule 1 (weak preference)")))])    
dfContingency.loc["no preference","correct"]=len(df[(df["tag"] == "dfInvertedHeuristicsSixDiffInRuleLen")&(df.which_of_the_rules_do_you_find_as_more_plausible=="No preference")])
dfContingency.loc["no preference","incorrect"]=len(df[(df["tag"] == "manualIncorrects")&(df.which_of_the_rules_do_you_find_as_more_plausible=="No preference")])

print dfContingency
print "CHECKSUM: Number of total rows: ",len(df), "; Sum of counts in contingency table:", sum(dfContingency.sum(1))
print "Average difference: " + str((df[r1Metric] - df[r2Metric]).abs().mean())
try:
  if dfContingency.loc["no preference","correct"]==0 | dfContingency.loc["no preference","incorrect"] :
    dfContingency=dfContingency.drop("no preference",0)
    print "WARNING:  no preference column ignored (contained a zero frequency)"
  chi2, p, dof, expected = scipy.stats.chi2_contingency(dfContingency)
  print  "p value", str(p)
except  ValueError:
  print "There was a zero frequency"
    
