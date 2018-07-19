import csv
import pandas as pd
import hashlib

def stringToInt(text):
  #return int(hashlib.md5(text).hexdigest(), 16)
  return str(int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16))[0:5]

def fixIDs(df):
 #the following three lines are needed only for TA
 df_ = pd.DataFrame()
 df_["r1id"]=df[df.r1id.isnull()].r1.apply(stringToInt)
 df_["r2id"]=df[df.r2id.isnull()].r2.apply(stringToInt) 
 df.update(df_)
 df.r1id=df.r1id.astype(str).replace("\.0","",regex=True)
 df.r2id=df.r2id.astype(str).replace("\.0","",regex=True)
 #the following two lines are not needed for TA
 df.r1id=df.r1id.str[0:5]
 df.r2id=df.r2id.str[0:5]
 return df

def read_crowdflower_full_export(datasets,extrafields=[]):
  df_all=pd.DataFrame()
  for dataset in datasets:
    df_stats=pd.read_csv(dataset["statfile"], delimiter=",", quoting=csv.QUOTE_ALL,dtype={"r1id":"str","r2id":"str"})    
    print(dataset["statfile"])
    print(dataset["name"])
    df_full_all=pd.DataFrame()
    for file in dataset["files"]:
      print (file)
      df_full=pd.read_csv(file, delimiter=",", quoting=csv.QUOTE_ALL,index_col=False,dtype={"r1id":"str","r2id":"str"},usecols=["r1id","r2id","r1","r2","which_of_the_rules_do_you_find_as_more_plausible"] + extrafields)
      df_full_all=pd.concat([df_full_all,df_full],ignore_index=True)
    df_full_all=fixIDs(df_full_all)
    orig_size=len(df_full_all)
    df_full_all=df_full_all.merge(df_stats, on=["r1id","r2id"],how="inner")
    if len(df_full_all)!=orig_size:
      if dataset["name"] == "MUSHROOMS" and len(df_full_all)==300:
        print ("Intentionaly omitting "+ str(orig_size-len(df_full_all)) + " rows for MUSHROOM dataset")
      else:
        print ("Something wrong after joining statistics. Original rows: " + str(orig_size) + " New rows:" + str(len(df_full_all)))
    print(len(df_full_all))
    df_full_all["dataset"]=dataset["name"]
    df_all=pd.concat([df_all,df_full_all])
  return df_all

def get_table_with_derived_metrics(df):  

  #applicable to mushroom dataset
  df.which_of_the_rules_do_you_find_as_more_plausible.replace("rule_1_strong_preference","Rule 1 (strong preference)", inplace=True)
  df.which_of_the_rules_do_you_find_as_more_plausible.replace("rule_1_weak_preference","Rule 1 (weak preference)", inplace=True)
  df.which_of_the_rules_do_you_find_as_more_plausible.replace("rule_2_strong_preference","Rule 2 (strong preference)", inplace=True)
  df.which_of_the_rules_do_you_find_as_more_plausible.replace("rule_2_weak_preference","Rule 2 (weak preference)", inplace=True)
  df.which_of_the_rules_do_you_find_as_more_plausible.replace("no_preference","No preference", inplace=True)

  df_export=df[["r1id","r2id","algorithm","rulerelation","dataset","which_of_the_rules_do_you_find_as_more_plausible","tag"]]

  df_export["target"]=df["which_of_the_rules_do_you_find_as_more_plausible"].map({'No preference':0, 'Rule 1 (weak preference)':1, 'Rule 2 (weak preference)':-1, 'Rule 1 (strong preference)':2,'Rule 2 (strong preference)':-2})
  
  #!!! All min metrics are of "COST" type: the lower the value of the metric, the better
  # this means that the rule 1 and rule 2 values are reversed:
  # rule 2 value is substracted from rule 1 for these metrics 
  metrics=[("r1len","r2len","lenDelta","lenRatio"),("r1DepthMax","r2DepthMax","DepthMaxDelta","DepthMaxRatio"),("r2DepthMin","r1DepthMin","DepthMinDelta","DepthMinRatio"),("r1LabelLengthSum","r2LabelLengthSum","LabelLengthSumDelta","LabelLengthSumRatio"),("r1LabelLengthMax","r2LabelLengthMax","LabelLengthMaxDelta","LabelLengthMaxRatio"),("r1LabelLengthAvg","r2LabelLengthAvg","LabelLengthAvgDelta","LabelLengthAvgRatio"),("r2LabelLengthMin","r1LabelLengthMin","LabelLengthMinDelta","LabelLengthMinRatio"),("r1minDistance","r2minDistance","MinDistanceDelta","MinDistanceRatio"),("r1maxDistance","r1maxDistance","MaxDistanceDelta","MaxDistanceRatio"),("r21mindepthLCS","r1mindepthLCS","MinDepthLCSDelta","MinDepthLCSRatio"),("r1PageRankMax","r2PageRankMax","PageRankMaxDelta","PageRankMaxRatio"),("r2PageRankMin","r1PageRankMin","PageRankMinDelta","PageRankMinRatio"),("r1PageRankAvg","r2PageRankAvg","PageRankAvgDelta","PageRankAvgRatio"),("r1conf","r2conf","ConfDelta","ConfRatio"),("r1supp","r2supp","SuppDelta","SuppRatio"),("r1LitImpMax","r2LitImpMax","LitImpMaxDelta","LitImpMaxRatio"),("r2LitImpMin","r1LitImpMin","LitImpMinDelta","LitImpMinRatio"),("r1LitImpAvg","r2LitImpAvg","LitImpAvgDelta","LitImpAvgRatio"),("r1AttImpMax","r2AttImpMax","AttImpMaxDelta","AttImpMaxRatio"),("r2AttImpMin","r1AttImpMin","AttImpMinDelta","AttImpMinRatio"),("r1AttImpAvg","r2AttImpAvg","AttImpAvgDelta","AttImpAvgRatio"),("r1AttImpSum","r2AttImpSum","AttImpSumDelta","AttImpSumRatio"),("r1LitImpSum","r2LitImpSum","LitImpSumDelta","LitImpSumRatio")]  
  for (r1_metric,r2_metric, delta_name,ratio_name) in metrics:
    if not (r1_metric in df.columns):
      print ("omitting " + r1_metric + " not found")
      continue
    df_export[r1_metric]=df[r1_metric]
    df_export[r2_metric]=df[r2_metric]
    df_export[delta_name]= df[r1_metric]-df[r2_metric]
    df_export[ratio_name]= df[r1_metric]/df[r2_metric]
    df_export[ratio_name]=df_export[ratio_name].replace("inf","")
  return df_export
