import pandas as pd
import csv
import re
from columndef import *
import hashlib
dfMap = pd.read_csv('input/mushroom.name.map', delimiter=",", quoting=csv.QUOTE_ALL)

flagMark=True
def stringToInt(text):
 return str(int(hashlib.md5(text).hexdigest(), 16))[0:5]

def generateText(column):
    return column.replace([" => {label=p"," => {label=e", "}$", "{", "}", ",", "=1.0"], ["then the mushroom is poisonous<b>","then the mushroom is edible<b>", "</b>",
                                                                         "if the mushroom has the following properties (simultaneously) <ul><li>",
                                                                         "&nbsp;</li></ul>",
                                                                         "&nbsp;<b>and</b> </li><li>", ""], regex=True)

def friendly(rule):
  literals=re.findall("(?<=\<li>).*?(?=&nbsp;)",rule)
  for literal in literals :
    hit=dfMap[dfMap.orig==literal]
    if len(hit)>0:
        translation =hit.iloc[0].friendly
        rule=rule.replace(literal,translation)
        if flagMark:
            dfMap.loc[dfMap.orig==literal,"used"]=True
    else:
        print "Not found " + str(literal)
  return rule
dfMap["used"]=False
dfData = pd.read_csv('crowdflower_input/mushrooms.raw.csv', delimiter=",", quoting=csv.QUOTE_ALL)

dfData["r1id"]=dfData.r1.apply(stringToInt)
dfData["r2id"]=dfData.r2.apply(stringToInt)

dfData.r1 = generateText(dfData.r1)
dfData.r2 = generateText(dfData.r2)

#does not marks literals as used for test questions
flagMark=True
dfData.loc[dfData.tag != "TEST","r1"]=dfData[dfData.tag != "TEST"].r1.apply(friendly)
dfData.loc[dfData.tag != "TEST","r2"]=dfData[dfData.tag != "TEST"].r2.apply(friendly)
#this flag is used by the friendly function
flagMark=False
dfData.loc[dfData.tag == "TEST","r1"]=dfData[dfData.tag == "TEST"].r1.apply(friendly)
dfData.loc[dfData.tag == "TEST","r2"]=dfData[dfData.tag == "TEST"].r2.apply(friendly)

# all column names need to be lower case
columns.append("which_of_the_rules_do_you_find_as_more_plausible_gold")
columns.append("which_of_the_rules_do_you_find_as_more_plausible_gold_reason")
columns.append("_golden")

dfData["which_of_the_rules_do_you_find_as_more_plausible_gold"] = ""
dfData["which_of_the_rules_do_you_find_as_more_plausible_gold_reason"] = ""
dfData["_golden"] = ""

dfData.loc[dfData.tag == "TEST", "_golden"] = "TRUE"
dfData.loc[
    dfData.tag == "TEST", ["r1len", "r2len", "r1conf", "r2conf", "r1sup", "r2sup"]] = ""

dfData[dfData.tag != "TEST"].to_csv("crowdflower_input/mushrooms.csv", columns=columns,
                                    quoting=csv.QUOTE_NONNUMERIC, index_label="id")
#needs to be manually edited afterwards
dfData[dfData.tag == "TEST"].to_csv("testquestions/mushrooms.test", columns=columns, quoting=csv.QUOTE_NONNUMERIC,
                                    index_label="id")
dfMap[dfMap.used==True].to_csv('crowdflower_input_literal_importance/mushrooms.LiteralImportance.csv', delimiter=",", quoting=csv.QUOTE_ALL)
