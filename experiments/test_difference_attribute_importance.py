import pandas as pd
import csv
import numpy as np
from scipy import stats

field1={"876173":"what_is_the_relevance_of_the_property_given_above_for_determining_whether_a_mushroom_is_edible_or_poisonous","876663":"what_is_the_relevance_of_the_property_given_above_for_determining_the_risk_of_traffic_accidents_in_a_given_country" }

mushroom=pd.read_csv('crowdflower_output/attributeimportance/f876173.csv', delimiter=",", quoting=csv.QUOTE_ALL)
mushroom_2=pd.read_csv('crowdflower_output/attributeimportance/f876832.csv', delimiter=",", quoting=csv.QUOTE_ALL)        
mushroom=pd.concat([mushroom,mushroom_2])
traffic=pd.read_csv('crowdflower_output/attributeimportance/f876663.csv', delimiter=",", quoting=csv.QUOTE_ALL)
#exclude pairs with given reason shorter than 11 characters
mushroom=mushroom[(mushroom.what_is_the_rationale_for_your_choice.str.len()>10)]
traffic=traffic[(traffic.what_is_the_rationale_for_your_choice.str.len()>10)]

print("Mushroom sample size " + str(len(mushroom)))
print("Traffic sample size " + str(len((traffic))))

print("Mushroom mean " + str(mushroom[field1["876173"]].mean()))
print("Traffic mean " + str(traffic[field1["876663"]].mean()))

print stats.ttest_ind(mushroom[field1["876173"]],traffic[field1["876663"]], equal_var = False)

