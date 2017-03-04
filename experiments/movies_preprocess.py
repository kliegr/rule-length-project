import csv
import pandas as pd
import datetime
import re
df=pd.read_csv('input/movies_metacritic_types_onlyyago.csv', delimiter=";", quoting=csv.QUOTE_ALL)
#df["Release_year"]=pd.DatetimeIndex(df["Release date"]).year
#df["Release_month"]=pd.DatetimeIndex(df["Release date"]).month
#df["Release_day_of_week"]=pd.DatetimeIndex(df["Release date"]).dayofweek
#df["Release_day_of_week"]=df["Release_day_of_week"].map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})

for column in df.columns:
 df.rename(columns={column: column.replace("DBpedia_URI_type_http://dbpedia.org/class/yago/","")}, inplace=True)
for column in df.columns:
 df.rename(columns={column: column.replace("-","")}, inplace=True)
 #Variables are not allowed to start with a digit in python and R
for column in df.columns:
 df.rename(columns={column: column.replace(".","")}, inplace=True)
 #Variables are not allowed to start with a digit in python and R

for column in df.columns: 
 if re.match('^[0-9].*', column): 
  print "renaming", column
  df.rename(columns={column: "X"+column}, inplace=True)
 #Variables are not allowed to contain dash
 

df=df.drop("DBpedia_URI",1)    
df=df.drop("YagoPermanentlyLocatedEntity",1)    
#df=df.drop("YagoLegalActorGeo",1)
#df=df.drop("YagoLegalActor",1)
df=df.drop("Release date",1)

df.to_csv('output/movies_shortened.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)