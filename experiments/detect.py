import re
def detectAlgorithm(tag):
  if "dfIn" in tag:
    algorithm="InvertedHeuristics"
  else:
    algorithm="arules"
  return algorithm

def detectType(rule1,rule2):  
  literalsR1=re.sub(r"} => {.*","",rule1).replace("=1.0","").replace("{","").split(",")
  literalsR2=re.sub(r"} => {.*","",rule2).replace("=1.0","").replace("{","").split(",")
  interst=set(literalsR1).intersection(literalsR2)
  if len(literalsR1)==len(literalsR2):
    if len(interst)>0:
      rulerelation="sameLengthRulesNonDisjunctAtt"
    else:
      rulerelation="sameLengthRulesDisjunctAtt"
  else:
    if len(literalsR1)>len(literalsR2) and len(interst)==len(literalsR2):
      rulerelation="differentLengthRulesR1subsumingR2Att"
    if len(literalsR2)>len(literalsR1) and len(interst)==len(literalsR1):
      rulerelation="differentLengthRulesR2subsumingR1Att"
    if len(literalsR1)!=len(literalsR1) and len(interst)==0:
      rulerelation="differentLengthRulesR2subsumingR1Att"
    else:
        rulerelation="differentLengthRulesNeitherDisjunctNorSubsumingAtt"
  return rulerelation
