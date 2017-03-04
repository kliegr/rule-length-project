
#according to http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.spearmanr.html
#scipy.stats.spearmanr supports tie-handling (http://stackoverflow.com/questions/10711395/spearman-correlation-and-ties)
#an example of tie corrected spearman is found in "Cureton, Edward E. The average spearman rank criterion correlation when ties are present. Psychometrika 23, no. 3 (September 1958): 271-272.
import csv
import pandas as pd
import scipy.stats
import sys
from  sklearn.isotonic import check_increasing
from  scipy.stats import spearmanr

measures = ["lenDelta", "DepthMaxDelta", "DepthMinDelta", "LabelLengthSumDelta", "LabelLengthMaxDelta",
            "LabelLengthAvgDelta", "LabelLengthMinDelta", "MaxDistanceDelta", "MinDepthLCSDelta", "PageRankMaxDelta",
            "PageRankMinDelta", "PageRankAvgDelta", "ConfDelta", "SuppDelta", "LitImpMaxDelta", "LitImpMinDelta",
            "LitImpAvgDelta", "LitImpSumDelta", "AttImpSumDelta", "AttImpMaxDelta", "AttImpMinDelta", "AttImpAvgDelta"]

if len(sys.argv) > 1:
    infile = sys.argv[1]
else:
    infile = "stats/datafiles/V2-e8-quality.csv"
df = pd.read_csv(infile, delimiter=",", quoting=csv.QUOTE_ALL, index_col=False)

print "variable & rho & p \\\\"
for measure in measures:
    # check_increasing(df.LitImpAvgDelta,df.target)
    if measure in df.columns:
    # Spearman would produce a result even if all variable values  for all rows are null
        if sum(df[measure].notnull()) == 0:
            print measure, "data not available"
        else:
            sr = spearmanr(df[measure], df.target)
            coef = str(sr[0])
            pvalue = str(sr[1])
            print measure, "&", sr[0], "&", sr[1], "\\\\"
            with open('summary.csv', 'a') as file:
                file.write(infile + "," + measure + "," + coef + "," + pvalue + ",," + str(len(df)) + ",Spearman\n")
    else:
        print measure, "data not available"
