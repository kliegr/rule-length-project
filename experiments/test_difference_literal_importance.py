import pandas as pd
import csv
import numpy as np
from scipy import stats
### Analysis of raw judgments ##

dfContingency = pd.DataFrame(columns=["strong","weak","no_influence"])
#traffic
f="842634"
df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfContingency.loc["traffic","weak"]=len(df[df.rating.str.contains("weak")].rating)
dfContingency.loc["traffic","strong"]=len(df[df.rating.str.contains("strong")].rating)
dfContingency.loc["traffic","no_influence"]=len(df[df.rating.str.contains("no_influence")].rating)
#mercer
f="842668"
df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfContingency.loc["quality","weak"]=len(df[df.rating.str.contains("weak")].rating)
dfContingency.loc["quality","strong"]=len(df[df.rating.str.contains("strong")].rating)
dfContingency.loc["quality","no_influence"]=len(df[df.rating.str.contains("no_influence")].rating)

#movies
f="842577"
df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfContingency.loc["movies","weak"]=len(df[df.rating.str.contains("weak")].rating)
dfContingency.loc["movies","strong"]=len(df[df.rating.str.contains("strong")].rating)
dfContingency.loc["movies","no_influence"]=len(df[df.rating.str.contains("no_influence")].rating)

#mushrooms
f="855714"
df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
#contains small  part of data which was omitted from the original experiment
df2=pd.read_csv('crowdflower_output/literalimportance/f859005.csv', delimiter=",", quoting=csv.QUOTE_ALL)
df=pd.concat([df,df2])

df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
dfContingency.loc["mushrooms","weak"]=len(df[df.rating.str.contains("weak")].rating)
dfContingency.loc["mushrooms","strong"]=len(df[df.rating.str.contains("strong")].rating)
dfContingency.loc["mushrooms","no_influence"]=len(df[df.rating.str.contains("no_influence")].rating)

print dfContingency  
chi2, p, dof, expected = stats.chi2_contingency(dfContingency)
print  "p value", str(p)

### Analysis of aggregated judgments ##
#traffic
f="842634"
traffic=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg'+f+'_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)
(abs(traffic.rating)).mean()
#mercer
f="842668"
mercer=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg'+f+'_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)
(abs(mercer.rating)).mean()
#movies
f="842577"
movies=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg'+f+'_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)
(abs(movies.rating)).mean()
#mushrooms
f="855714"
mushroom=pd.read_csv('postprocessed_crowdflower_output/literalimportance/customAgg'+f+'_positive.csv', delimiter=",", quoting=csv.QUOTE_ALL)
(abs(mushroom.rating)).mean()