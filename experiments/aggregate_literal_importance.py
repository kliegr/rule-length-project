import pandas as pd
import csv
import numpy as np

for targetClass in ["positive","negative"]:
    if targetClass == "positive":
        correction=1
    else:
        correction=-1

    #traffic
    f="842634"
    df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
    df.rating.replace("low_strong_influence",correction*2, inplace=True)    
    df.rating.replace("Low (weak influence)",correction*1, inplace=True)
    df.rating.replace("low_weak_influence",correction*1, inplace=True)  
    df.rating.replace("no_influence",0, inplace=True)
    df.rating.replace("high_weak_influence",correction*-1, inplace=True)    
    df.rating.replace("high_strong_influence",correction*-2, inplace=True)
    dfAgg= df.groupby(["uri","friendly"]).agg({"rating" : np.mean})
    dfAgg.to_csv("postprocessed_crowdflower_output/literalimportance/customAgg"+f+"_" +targetClass+".csv",quoting=csv.QUOTE_NONNUMERIC,index_label=["uri","friendly"])    
    #mercer
    f="842668"
    df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
    df.rating.replace("high_strong_influence",correction*2, inplace=True)
    df.rating.replace("high_weak_influence",correction*1, inplace=True)    
    df.rating.replace("no_influence",0, inplace=True)
    df.rating.replace("low_strong_influence",correction*-2, inplace=True)    
    df.rating.replace("Low (weak influence)",correction*-1, inplace=True)
    df.rating.replace("low_weak_influence",correction*-1, inplace=True)  
    dfAgg= df.groupby(["uri","friendly"]).agg({"rating" : np.mean})
    dfAgg.to_csv("postprocessed_crowdflower_output/literalimportance/customAgg"+f+"_" +targetClass+".csv",quoting=csv.QUOTE_NONNUMERIC,index_label=["uri","friendly"])
    #movies
    f="842577"
    df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
    df.rating.replace("good_strong_influence",correction*2, inplace=True)
    df.rating.replace("Good (weak influence)",correction*1, inplace=True)
    df.rating.replace("no_influence",0, inplace=True)
    df.rating.replace("Bad (weak influence)",correction*-1, inplace=True)
    df.rating.replace("Bad (strong influence)",correction*-2, inplace=True)
    dfAgg= df.groupby(["uri","friendly"]).agg({"rating" : np.mean})
    dfAgg.to_csv("postprocessed_crowdflower_output/literalimportance/customAgg"+f+"_" +targetClass+".csv",quoting=csv.QUOTE_NONNUMERIC,index_label=["uri","friendly"])
    #mushrooms
    f="855714"
    df=pd.read_csv('crowdflower_output/literalimportance/f'+f+'.csv', delimiter=",", quoting=csv.QUOTE_ALL)
    #contains small  part of data which was omitted from the original experiment
    df2=pd.read_csv('crowdflower_output/literalimportance/f859005.csv', delimiter=",", quoting=csv.QUOTE_ALL)
    df=pd.concat([df,df2])
    df.rating.replace("edible_strong_influence",correction*2, inplace=True)  
    df.rating.replace("edible_weak_influence",correction*1, inplace=True)
    df.rating.replace("no_influence",0, inplace=True)
    df.rating.replace("poisonous_weak_influence",correction*-1, inplace=True)
    df.rating.replace("poisonous_strong_influence",correction*-2, inplace=True)
    dfAgg= df.groupby(["orig"]).agg({"rating" : np.mean})
    dfAgg.to_csv("postprocessed_crowdflower_output/literalimportance/customAgg"+f+"_" +targetClass+".csv",quoting=csv.QUOTE_NONNUMERIC,index_label=["orig"])
