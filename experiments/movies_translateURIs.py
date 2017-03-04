import pandas as pd
import csv
import itertools
import re
import requests

def getLink(link):  
  try:
    r = requests.get(link)
    if r.status_code==200:      
      pattern= re.compile('http://yago-knowledge.org/resource/wikicategory_([^"]+)"')
      match=pattern.search(r.text)
      if match:	
        link="https://en.wikipedia.org/wiki/Category:" + match.group(1)
        r = requests.head(link)
        if r.status_code==200:      
          print ("200 for " + link)
          return (link)
        else:
          print (str(r.status_code) + " for " + link)
          return ("")
      else:
        return ("")
    else:
      print (str(r.status_code) + " for " + link)
      return ""
  except requests.ConnectionError:
      print ("ConnectionError for " + link)
      return ""
  
 

dfData=pd.read_csv('input/movies_metacritic_types_onlyyago.csv', delimiter=";", quoting=csv.QUOTE_ALL)

df=pd.DataFrame(columns=["orig","uri","friendly"])
df.orig=list(filter(lambda x:  str.startswith(x,"DBpedia_URI_type"), dfData.columns))
df.dbpediauri = df.orig.replace(["DBpedia_URI_type_"],[""],regex=True)
df.uri=df.dbpediauri.apply(getLink)

df.friendly=df.orig.replace(["DBpedia_URI_type_http://dbpedia.org/class/yago[^;]*/","-","[.]","^(?=\d)"],["","","","X"],regex=True)

  
df.to_csv("crowdflower_input_literal_importance/movies.name.map",quoting=csv.QUOTE_NONNUMERIC,encoding='utf-8')
