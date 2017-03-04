echo "This file documents the data generation process"
echo "The resulting rule set is not deterministic - the output rule pairs are not exactly the same as used as input for the experiments"
echo "Execution halted"
exit

./prepare_cf_input_mercer.sh
./prepare_cf_input_movies.sh
./prepare_cf_input_traffic.sh
#the movies/traffic/mercer.test file needs to be manually edited to create test questions
#the final rule pairs are in movies/traffic/mercer.rules.pairs.translated.csv