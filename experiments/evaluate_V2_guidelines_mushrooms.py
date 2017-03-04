import csv
import pandas as pd
import os 
import crowdflower

inputCSVFiles=[{"name":"MUSHROOMS", "statfile":'postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f855702.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f860274.csv"]}]
df=crowdflower.read_crowdflower_full_export(inputCSVFiles)
print df["dataset"].value_counts()
df_export=crowdflower.get_table_with_derived_metrics(df)
df_export[-df_export.tag.isin(["dfInvertedHeuristicsSixDiffInRuleLen","manualIncorrect"])].to_csv('stats/datafiles/V2-e11-mushrooms.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)

df_export[(df_export.tag=="dfInvertedHeuristicsSixDiffInRuleLen")|(df_export.tag=="manualIncorrect")].to_csv('stats/datafiles/V2-e17-mushrooms-correctVsIncorrect.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)

os.system("python chisquare.py stats/datafiles/V2-e11-mushrooms.csv > stats/V2-e11-mushrooms.chi")
os.system("python spearman.py stats/datafiles/V2-e11-mushrooms.csv > stats/V2-e11-mushrooms.spr")
os.system("Rscript partialCorrelation.R stats/datafiles/V2-e11-mushrooms.csv > stats/V2-e11-mushrooms.corr")
os.system("Rscript logreg.R stats/datafiles/V2-e11-mushrooms.csv > stats/V2-e11-mushrooms.reg")
os.system("python chisquare_TestIncorrectMushrooms.py stats/datafiles/V2-e17-mushrooms-correctVsIncorrect.csv > stats/V2-e17-mushrooms-correctVsIncorrect.chi")
