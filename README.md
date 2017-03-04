# rule-length-project

This repository contains files for replicating the experiments with the impact of cognitive biases on the plausibility of inductively learned rules depending on their length.

## Data Preparation
The data used on the input of crowdsourcing (definition of the crowdsourcing tasks) is documented in scripts referred from ```experiments/PIPELINE_PREPARE_DATA_FOR_CF.sh```. The input data are in folder
```
experiments/input
```
This folder contains the input datasets: movies, mushroom, traffic, mercer (quality) as well as pre-discovered rules with the inverted rules learner provided by the KE Group.

This script is not intended for running mainly due to several manual interventions related mainly to the Traffic dataset, which resulted in  excessive number rules. 

The result of data preparation is in folders:
 ```
 experiments/crowdflower_input
 experiments/crowdflower_input_attribute_importance
 experiments/crowdflower_input_literal_importance
 ```

## Crowdsourcing Output
The human judgments collected via crowdsourcing are stored in folder
```
experiments/crowdflower_output
```

## Analysis of results
The analysis of results from crowdflower is performed using script ```experiments/PIPELINE_ANALYZE_DATA_FROM_CF.sh```. This script is runnable and should produce the same results as reported.
This script processes the files output by crowdsourcing (see above) and additionally linked data statistics on literals appearing in the rules provided by Heiko Paulheim, which are contained in folder `experiments/literal_linked_stats`.

The output of this script is
```
experiments/postprocessed_crowdflower_output # enriched and transformed crowdsourcing output
experiments/stats                            # result of statistical analysis on various subsets of the data
experiments/summary.csv                      # the final overview of the results
```
