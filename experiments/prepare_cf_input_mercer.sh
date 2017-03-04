# reads: input/mercer2015_dbpedia_types_onlyyago.csv
# writes: output/mercer2015_dbpedia_types_onlyyago_shortened.csv
python mercer_preprocess.py

# reads: output/mercer2015_dbpedia_types_onlyyago_shortened.csv
# writes: output/mercer2015.arules
Rscript mercer_minerules.R

# reads: output/mercer2015_dbpedia_types_onlyyago_shortened.csv',output/mercer2015.arules
# writes: output/mercer.arules.pairs
python mercer_generatepairs.py

# reads: input/mercer2015_dbpedia_types_onlyyago.csv
# writes: output/mercer.name.map
python mercer_translateURIs.py

# reads: output/mercer.name.map,output/mercer.arules.pairs,input/mercer2015_inverted_rule_learner.csv
# writes: output/mercer.arules.pairs.filtered, output/mercer.invertedheuristics.pairs.filtered
python mercer_filterRules.py

# reads:  output/mercer.arules.pairs.filtered, output/mercer.invertedheuristics.pairs.filtered
# writes: output/movies.pairs.selected
python mercer_selectRules.py

# reads:  output/mercer.name.map, output/movies.pairs.selected
# writes: output/mercer.rules.pairs.translated.csv, testquestions/mercer.test
python mercer_translateRules.py
