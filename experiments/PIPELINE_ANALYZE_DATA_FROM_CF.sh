rm "summary.csv"
rm -r "stats"
mkdir "stats"
rm -r "postprocessed_crowdflower_output"
unzip literal_linked_stats/literal_linked_stats.zip  -d literal_linked_stats
mkdir "postprocessed_crowdflower_output"
mkdir "stats/datafiles"
mkdir "postprocessed_crowdflower_output/literalimportance"
mkdir "postprocessed_crowdflower_output/attributeimportance"
echo "file,variable,test/corr coeff,p-value,note,size,algorithm" > "summary.csv"
#applied to V1 files
python "aggregate_literal_importance.py"
python "aggregate_attribute_importance.py"
python "mushrooms_compute_stats_for_rulepairs.py"
python "mercer_compute_stats_for_rulepairs.py"
python "traffic_compute_stats_for_rulepairs.py"
python "movies_compute_stats_for_rulepairs.py"

python "evaluate_V1_guidelines.py"
python "evaluate_V2_guidelines.py"
python "evaluate_V1_guidelines_mushrooms.py"
python "evaluate_V2_guidelines_mushrooms.py"
python "evaluate_V3_guidelines.py"

python "lindaV1.py"
python "lindaV2.py"
python "lindaV3.py"
python "lindaV3b.py"

python "test_difference_attribute_importance.py"
python "test_difference_literal_importance.py"
rm literal_linked_stats/*.csv


