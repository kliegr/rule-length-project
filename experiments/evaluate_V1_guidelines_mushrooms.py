import csv
import pandas as pd
import os 
import crowdflower

inputCSVFiles=[{"name":"MUSHROOMS", "statfile":'postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f956290.csv","crowdflower_output/V1Guidelines/f956954.csv"]}]
df=crowdflower.read_crowdflower_full_export(inputCSVFiles)
print df["dataset"].value_counts()
df_export=crowdflower.get_table_with_derived_metrics(df)
df_export[-df_export.tag.isin(["dfInvertedHeuristicsSixDiffInRuleLen","manualIncorrect"])].to_csv('stats/datafiles/V1-e12-mushrooms.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)

df_export[(df_export.tag=="dfInvertedHeuristicsSixDiffInRuleLen")|(df_export.tag=="manualIncorrect")].to_csv('stats/datafiles/V1-e13-mushrooms-correctVsIncorrect.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)

os.system("python chisquare.py stats/datafiles/V1-e12-mushrooms.csv > stats/V1-e12-mushrooms.chi")
os.system("python spearman.py stats/datafiles/V1-e12-mushrooms.csv > stats/V1-e12-mushrooms.spr")
os.system("Rscript partialCorrelation.R stats/datafiles/V1-e12-mushrooms.csv > stats/V1-e12-mushrooms.corr")
os.system("Rscript logreg.R stats/datafiles/V1-e12-mushrooms.csv > stats/V1-e12-mushrooms.reg")
os.system("python chisquare_TestIncorrectMushrooms.py stats/datafiles/V1-e13-mushrooms-correctVsIncorrect.csv > stats/V1-e13-mushrooms-correctVsIncorrect.chi")
