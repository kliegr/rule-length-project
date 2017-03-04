import csv
import pandas as pd
df=pd.read_csv('input/mercer2015_dbpedia_types_onlyyago.csv', delimiter=";", quoting=csv.QUOTE_ALL)

for column in df.columns:
 df.rename(columns={column: column.replace("city_uri_type_http://dbpedia.org/class/yago/","")}, inplace=True)

df=df.drop("city_uri",1)
for i in xrange(len(df)):
  if df["rank"].iloc[i] <46:    
    df.set_value(i,"Label","highest")
  elif df["rank"].iloc[i] <92:    
    df.set_value(i,"Label","high")
  elif df["rank"].iloc[i] <138:    
    df.set_value(i,"Label","medium")
  elif df["rank"].iloc[i] <184:    
    df.set_value(i,"Label","low")    
  else:    
    df.set_value(i,"Label","lowest")   
df=df.drop("rank",1)    
df=df.drop("YagoPermanentlyLocatedEntity",1)    
df=df.drop("YagoLegalActorGeo",1)
df=df.drop("YagoLegalActor",1)
df=df.drop("YagoGeoEntity",1)    

df.to_csv('output/mercer2015_dbpedia_types_onlyyago_shortened.csv', delimiter=",", quoting=csv.QUOTE_ALL,index=False)