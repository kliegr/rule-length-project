import csv
import pandas as pd
import os 
import crowdflower
inputCSVFiles=[{"name":"MOVIES", "statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V3guidelines_with_explicit_frequency/f843916.csv"]}]
df=crowdflower.read_crowdflower_full_export(inputCSVFiles)
print df["dataset"].value_counts()
df_export=crowdflower.get_table_with_derived_metrics(df)
df_export.to_csv('stats/datafiles/V3_movies.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.algorithm=="InvertedHeuristics"].to_csv('stats/datafiles/V3-Movies-e1-invertedheuristics.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.algorithm=="arules"].to_csv('stats/datafiles/V3-Movies-e2-arules.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[(df_export.rulerelation=="differentLengthRulesR1subsumingR2Att") | (df_export.rulerelation=="differentLengthRulesR2subsumingR1Att")].to_csv('stats/datafiles/V3-Movies-e3-subsuming.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="sameLengthRulesNonDisjunctAtt"].to_csv('stats/datafiles/V3-Movies-e4-sameLengthRulesNonDisjunctAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="sameLengthRulesDisjunctAtt"].to_csv('stats/datafiles/V3-Movies-e5-sameLengthRulesDisjunctAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="differentLengthRulesNeitherDisjunctNorSubsumingAtt"].to_csv('stats/datafiles/V3-Movies-e6-differentLengthRulesNeitherDisjunctNorSubsumingAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="differentLengthRulesDisjunctAtt"].to_csv('stats/datafiles/V3-Movies-e7-differentLengthRulesDisjunctAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
files=["V3_movies","V3-Movies-e1-invertedheuristics","V3-Movies-e2-arules","V3-Movies-e3-subsuming","V3-Movies-e4-sameLengthRulesNonDisjunctAtt","V3-Movies-e5-sameLengthRulesDisjunctAtt","V3-Movies-e6-differentLengthRulesNeitherDisjunctNorSubsumingAtt","V3-Movies-e7-differentLengthRulesDisjunctAtt"]

for f in files:
	os.system("python chisquare.py stats/datafiles/"+f+".csv > stats/"+f+".chi")
	os.system("python spearman.py stats/datafiles/"+f+".csv > stats/"+f+".spr")
	os.system("Rscript logreg.R stats/datafiles/"+f+".csv > stats/"+f+".reg")
	os.system("Rscript partialCorrelation.R stats/datafiles/"+f+".csv > stats/"+f+".corr")
