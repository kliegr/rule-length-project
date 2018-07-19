import pandas as pd
import os
import crowdflower
import csv
experiment1=[{"name":"TRAFFIC", "version":1, "statfile":'postprocessed_crowdflower_output/traffic_accidents_types.arules.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f791490.csv"]},{"name":"QUALITY","version":1,"statfile":'postprocessed_crowdflower_output/mercer.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f834875.csv"]},{"name":"MOVIES","version":1,"statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f836187.csv"]},{"name":"MUSHROOMS", "version":1,"statfile":'postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f956290.csv","crowdflower_output/V1Guidelines/f956954.csv"]},{"name":"MUSHROOMS", "version":2,"statfile":'postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f855702.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f860274.csv"]},{"name":"TRAFFIC", "version":2, "statfile":'postprocessed_crowdflower_output/traffic_accidents_types.arules.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f843991.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f857983.csv"]},{"name":"QUALITY","version":2,"statfile":'postprocessed_crowdflower_output/mercer.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f843982.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f857955.csv"]},{"name":"MOVIES","version":2,"statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f843002.csv"]},{"name":"MOVIES", "version":3, "statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V3guidelines_with_explicit_frequency/f843916.csv"]}]
experiment2=[{"version":"1", "file":'crowdflower_output/linda/f854177.csv'}, {"version":"2", "file":'crowdflower_output/linda/f857928.csv' },{"version":"3a", "file":'crowdflower_output/linda/f858990.csv' },{"version":"3b", "file":'crowdflower_output/linda/f860282.csv' }]
experiment3a=[{"name":"MUSHROOM", "version":"ATTIMP", "files":["crowdflower_output/attributeimportance/f876173.csv","crowdflower_output/attributeimportance/f876832.csv"]}]
experiment3b=[{"name":"TRAFFIC", "version":"ATTIMP", "files":["crowdflower_output/attributeimportance/f876663.csv"]}]
experiment4a=[{"name":"MUSHROOM", "version":"LITIMP", "files":["crowdflower_output/literalimportance/f855714.csv","crowdflower_output/literalimportance/f859005.csv"]}]
experiment4b=[{"name":"MOVIES", "version":"LITIMP", "file":"crowdflower_output/literalimportance/f842577.csv"}]
experiment4c=[{"name":"TRAFFIC", "version":"LITIMP", "file":"crowdflower_output/literalimportance/f842634.csv"}]
experiment4d=[{"name":"QUALITY", "version":"LITIMP", "file":"crowdflower_output/literalimportance/f842668.csv"}]

dfWorkers = set()
dfAll = pd.DataFrame(columns=["test"])

df_ = pd.DataFrame(columns=["dataset","v","judg","workers","usa","gbr","can","avg dur","reasons"])

for i in range(0,len(experiment1)):
    inputCSVFile = experiment1[i:i+1]
    df=crowdflower.read_crowdflower_full_export(inputCSVFile,extrafields=["_worker_id","_country","_started_at","_created_at","what_is_the_rationale_for_your_choice"])
    #drop pairs containing manually input rule
    if experiment1[i]["name"]=="MUSHROOMS":
        # the same as "manualIncorrect"  - one rule was manually added to the discovered rule set and then excluded from subsequent analyses
        df=df.drop(df[df.r1id=="20624"].index)
        df=df.drop(df[df.r2id=="20624"].index)

    durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
    dfWorkers.update(df["_worker_id"].tolist())
    df_.loc[i] = [experiment1[i]["name"], str(experiment1[i]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
    if dfAll.empty:
        dfAll = df
    else:
        dfAll=pd.concat([dfAll,df])
for i in range(0,len(experiment2)):
    df=pd.read_csv(experiment2[i]["file"], delimiter=",", quoting=csv.QUOTE_ALL,index_col=False)
    #drop pairs containing manually input rule
    durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
    df_.loc[i+len(experiment1)] = ["Linda", str(experiment2[i]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)),len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]            
    # workers in experiment 2 are intentionally omitted from the total count of unique workers
#attribute importance
##mushroom
df1=pd.read_csv(experiment3a[0]["files"][0], delimiter=",", quoting=csv.QUOTE_ALL)    
df2=pd.read_csv(experiment3a[0]["files"][1], delimiter=",", quoting=csv.QUOTE_ALL)    
df=pd.concat([df1,df2])

durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
df_.loc[len(df_)+1] = [experiment3a[0]["name"], str(experiment3a[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
df=df[df["what_is_the_rationale_for_your_choice"].str.len()>10]
df_.loc[len(df_)+1] = [experiment3a[0]["name"] + "_onlyused", str(experiment3a[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
dfWorkers.update(df["_worker_id"].tolist())
df_.to_csv("stats/workers.csv")
dfAll=pd.concat([dfAll,df])
##traffic
df=pd.read_csv(experiment3b[0]["files"][0], delimiter=",", quoting=csv.QUOTE_ALL)    

durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
df_.loc[len(df_)+1] = [experiment3b[0]["name"], str(experiment3b[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
df=df[df["what_is_the_rationale_for_your_choice"].str.len()>10]
df_.loc[len(df_)+1] = [experiment3b[0]["name"] + "_onlyused", str(experiment3b[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
dfWorkers.update(df["_worker_id"].tolist())
df_.to_csv("stats/workers.csv")
dfAll=pd.concat([dfAll,df])
    #literal importance"
## mushroom
df1=pd.read_csv(experiment4a[0]["files"][0], delimiter=",", quoting=csv.QUOTE_ALL)    
df2=pd.read_csv(experiment4a[0]["files"][1], delimiter=",", quoting=csv.QUOTE_ALL)    
df=pd.concat([df1,df2])

durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
df_.loc[len(df_)+1] = [experiment4a[0]["name"], str(experiment4a[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
dfAll=pd.concat([dfAll,df])
dfWorkers.update(df["_worker_id"].tolist())
## movies
df=pd.read_csv(experiment4b[0]["file"], delimiter=",", quoting=csv.QUOTE_ALL)    
durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
df_.loc[len(df_)+1] = [experiment4b[0]["name"], str(experiment4b[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
dfAll=pd.concat([dfAll,df])
dfWorkers.update(df["_worker_id"].tolist())
## traffic
df=pd.read_csv(experiment4c[0]["file"], delimiter=",", quoting=csv.QUOTE_ALL)    
durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
df_.loc[len(df_)+1] = [experiment4c[0]["name"], str(experiment4c[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
dfAll=pd.concat([dfAll,df])
dfWorkers.update(df["_worker_id"].tolist())
## quality
df=pd.read_csv(experiment4d[0]["file"], delimiter=",", quoting=csv.QUOTE_ALL)    
durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
df_.loc[len(df_)+1] = [experiment4d[0]["name"], str(experiment4d[0]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]
dfAll=pd.concat([dfAll,df])
dfWorkers.update(df["_worker_id"].tolist())

df_.to_csv("stats/workers.csv")
dfAll.to_csv("stats/all-df-contatenated.csv")
print(dfWorkers)
print("unique workers:" + str(len(dfWorkers)))