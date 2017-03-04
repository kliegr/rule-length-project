import pandas as pd
import csv
import numpy as np
from scipy import stats

#mushroom

field1={"876173":"what_is_the_relevance_of_the_property_given_above_for_determining_whether_a_mushroom_is_edible_or_poisonous","876663":"what_is_the_relevance_of_the_property_given_above_for_determining_the_risk_of_traffic_accidents_in_a_given_country" }
field2={"876173":"orig","876663":"friendly" }

field3={"876173":"values","876663":"machine_readable_values" }


for f in ["876173","876663"]:
    print f
    df=pd.read_csv('crowdflower_output/attributeimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)    
    if f=="876173":
    	print "merging " + f+ " with " + "876832"
    	df2=pd.read_csv('crowdflower_output/attributeimportance/f876832.csv', delimiter=",", quoting=csv.QUOTE_ALL)        
    	df=pd.concat([df,df2])
    #exclude pairs with given reason shorter than 11 characters
    df=df[(df.what_is_the_rationale_for_your_choice.str.len()>10)]
    dfAgg1= df.groupby([field2[f]],as_index=False).agg({field1[f] : np.mean})
    dfAgg2= df.groupby([field2[f],field3[f]],as_index=False).agg({field1[f] : "count"})
    dfAgg1.columns=[field2[f],"rating"]
    dfAgg2.columns=[field2[f],field3[f],"count"]
    dfAgg=pd.merge(dfAgg1,dfAgg2,on=[field2[f]], how="inner")
    dfAgg.to_csv("postprocessed_crowdflower_output/attributeimportance/customAgg"+f+".csv",quoting=csv.QUOTE_NONNUMERIC,index_label=["id"])    

