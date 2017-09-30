import pandas as pd
import os
import crowdflower
import csv
experiment1=[{"name":"TRAFFIC", "version":1, "statfile":'postprocessed_crowdflower_output/traffic_accidents_types.arules.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f791490.csv"]},{"name":"QUALITY","version":1,"statfile":'postprocessed_crowdflower_output/mercer.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f834875.csv"]},{"name":"MOVIES","version":1,"statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f836187.csv"]},{"name":"MUSHROOMS", "version":1,"statfile":'postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv',"files":["crowdflower_output/V1Guidelines/f956290.csv","crowdflower_output/V1Guidelines/f956954.csv"]},{"name":"MUSHROOMS", "version":2,"statfile":'postprocessed_crowdflower_output/mushrooms.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f855702.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f860274.csv"]},{"name":"TRAFFIC", "version":2, "statfile":'postprocessed_crowdflower_output/traffic_accidents_types.arules.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f843991.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f857983.csv"]},{"name":"QUALITY","version":2,"statfile":'postprocessed_crowdflower_output/mercer.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f843982.csv","crowdflower_output/V2guidelines_without_hard_test_questions/f857955.csv"]},{"name":"MOVIES","version":2,"statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V2guidelines_without_hard_test_questions/f843002.csv"]},{"name":"MOVIES", "version":3, "statfile":'postprocessed_crowdflower_output/movies.pairs.with_stats.csv',"files":["crowdflower_output/V3guidelines_with_explicit_frequency/f843916.csv"]}]
experiment2=[{"version":"1", "file":'crowdflower_output/linda/f854177.csv'}, {"version":"2", "file":'crowdflower_output/linda/f857928.csv' },{"version":"3a", "file":'crowdflower_output/linda/f858990.csv' },{"version":"3b", "file":'crowdflower_output/linda/f860282.csv' }]


df_ = pd.DataFrame(columns=["dataset","v","judg","workers","usa","gbr","can","avg dur","reasons"])

for i in range(0,len(experiment1)):
    inputCSVFile = experiment1[i:i+1]
    df=crowdflower.read_crowdflower_full_export(inputCSVFile,extrafields=["_worker_id","_country","_started_at","_created_at","what_is_the_rationale_for_your_choice"])
    durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
    df_.loc[i] = [experiment1[i]["name"], str(experiment1[i]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)), len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]

for i in range(0,len(experiment2)):
    df=pd.read_csv(experiment2[i]["file"], delimiter=",", quoting=csv.QUOTE_ALL,index_col=False)
    durations = pd.to_datetime(df._created_at) - pd.to_datetime(df._started_at)
    df_.loc[i+len(experiment1)] = ["Linda", str(experiment2[i]["version"]),str(len(df)),str(len(df._worker_id.unique())),str(len(df[df._country=="USA"])),str(len(df[df._country=="GBR"])), str(len(df[df._country=="CAN"])), str(durations.mean(axis=0)),len(df[df["what_is_the_rationale_for_your_choice"].str.len()>10])]

df_.to_csv("stats/workers.csv")