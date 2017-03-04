import pandas as pd
import csv
infile="crowdflower_output/linda/f858990.csv"
dfAll=pd.read_csv(infile, delimiter=",", quoting=csv.QUOTE_ALL,index_col=False)
print dfAll["which_of_the_rules_do_you_find_as_more_plausible"].value_counts()
