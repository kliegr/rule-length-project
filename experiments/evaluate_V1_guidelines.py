import csv
import pandas as pd
import crowdflower
import os
inputCSVFiles=[{"name":"TRAFFIC", "statfile":'postprocessed_crowdflower_output/traffic_accidents_types.arules.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f791490.csv"]},{"name":"QUALITY","statfile":'postprocessed_crowdflower_output/mercer.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f834875.csv"]},{"name":"MOVIES","statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f836187.csv"]}]

df=crowdflower.read_crowdflower_full_export(inputCSVFiles)
print df["dataset"].value_counts()
df_export=crowdflower.get_table_with_derived_metrics(df)
## CREATE DATASET WITH ONLY THE REQUIRED INFORMATION
df_export.to_csv('stats/datafiles/V1-quality_movies_traffic.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.algorithm=="InvertedHeuristics"].to_csv('stats/datafiles/V1-e1-invertedheuristics.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.algorithm=="arules"].to_csv('stats/datafiles/V1-e2-arules.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[(df_export.rulerelation=="differentLengthRulesR1subsumingR2Att") | (df_export.rulerelation=="differentLengthRulesR2subsumingR1Att")].to_csv('stats/datafiles/V1-e3-subsuming.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="sameLengthRulesNonDisjunctAtt"].to_csv('stats/datafiles/V1-e4-sameLengthRulesNonDisjunctAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="sameLengthRulesDisjunctAtt"].to_csv('stats/datafiles/V1-e5-sameLengthRulesDisjunctAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="differentLengthRulesNeitherDisjunctNorSubsumingAtt"].to_csv('stats/datafiles/V1-e6-differentLengthRulesNeitherDisjunctNorSubsumingAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.rulerelation=="differentLengthRulesDisjunctAtt"].to_csv('stats/datafiles/V1-e7-differentLengthRulesDisjunctAtt.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)

df_export[df_export.dataset=="QUALITY"].to_csv('stats/datafiles/V1-e8-quality.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.dataset=="MOVIES"].to_csv('stats/datafiles/V1-e9-movies.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)
df_export[df_export.dataset=="TRAFFIC"].to_csv('stats/datafiles/V1-e10-traffic.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)

files=["V1-quality_movies_traffic","V1-e1-invertedheuristics","V1-e2-arules","V1-e3-subsuming","V1-e4-sameLengthRulesNonDisjunctAtt","V1-e5-sameLengthRulesDisjunctAtt","V1-e6-differentLengthRulesNeitherDisjunctNorSubsumingAtt","V1-e7-differentLengthRulesDisjunctAtt","V1-e8-quality","V1-e9-movies","V1-e10-traffic"]

for f in files:
	os.system("python chisquare.py stats/datafiles/"+f+".csv > stats/"+f+".chi")
	os.system("python spearman.py stats/datafiles/"+f+".csv > stats/"+f+".spr")
	os.system("Rscript logreg.R stats/datafiles/"+f+".csv > stats/"+f+".reg")
	os.system("Rscript partialCorrelation.R stats/datafiles/"+f+".csv > stats/"+f+".corr")
print ""
