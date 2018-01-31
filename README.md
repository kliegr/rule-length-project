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

## License
The code used to prepare experiments and analyze crowdsourcing data is published under GPL-3 license.

Three of the input datasets (Cities /also referred to as Mercer/, Traffic and Metacritic Movies)  were adapted from datasets published in:
```
Ristoski, Petar, Gerben Klaas Dirk de Vries, and Heiko Paulheim. "A collection of benchmark datasets for systematic evaluations of machine learning on the semantic web." International Semantic Web Conference. Springer International Publishing, 2016.
```
The current state of the licensing information for these datasets can be found at the [LOD dataset website](http://w3id.org/sw4ml-datasets). As of January 2018, these licenses are:
 * Traffic: [open](http://www.who.int/about/licensing/extracts/en/)
 * Metacritic Movies: pending
 * Cities: pending

The values of PageRank were sourced from  [Andreas Thalhammer's project](http://people.aifb.kit.edu/ath/).  The license is
 *Creative Commons Attribution-ShareAlike License*.
 
## Further documentation
The excel file `experiment_summary_digest.xlsx` provides further documentation on the analysis scripts as well as annotation guidelines. It also presents overview of the statistical analysis of the results.
