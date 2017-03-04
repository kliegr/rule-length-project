# reads: 'input/movies_metacritic_types_onlyyago.csv'
# writes: 'output/movies_shortened.csv'
python movies_preprocess.py

# reads: 'output/movies_shortened.csv'
# writes: "output/movies.arules"
Rscript movies_minerules.R

# reads: 'output/movies_shortened.csv',output/movies.arules
# writes: "output/movies.arules.pairs"
python movies_generatepairs.py

# reads: 'input/movies_metacritic_types_onlyyago.csv'
# writes: "output/movies.name.map"
python movies_translateURIs.py

# reads: output/movies.name.map,output/movies.arules.pairs,input/movies_inverted_rule_learner.csv
# writes: output/movies.arules.pairs.filtered, movies.invertedheuristics.pairs.filtered
python movies_filterRules.py

# reads:  output/movies.arules.pairs.filtered, output/movies.invertedheuristics.pairs.filtered
# writes: output/movies.pairs.selected
python movies_selectRules.py

# reads: "output/movies.name.map, output/movies.pairs.selected
# writes: output/movies.rules.pairs.translated.csv, testquestions/movies.test, output/movies.name.map
python movies_translateRules.py
