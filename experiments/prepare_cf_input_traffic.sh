bash ./traffic_shorten.sh
Rscript traffic_minerules.R
rm output/traffic_accidents_types.arules.pairs10per*
echo "this may run 10 days"
#total combinations=41146056
python3 traffic_matchingRules.py -s 0 -e 10000000 -o output/traffic_accidents_types.arules.pairs10per.0 & 
python3 traffic_matchingRules.py -s 10000001 -e 20000000 -o output/traffic_accidents_types.arules.pairs10per.1 & 
python3 traffic_matchingRules.py -s 20000001 -e 30000000 -o output/traffic_accidents_types.arules.pairs10per.2 & 
python3 traffic_matchingRules.py -s 30000001 -e 40000000 -o output/traffic_accidents_types.arules.pairs10per.3 & 
python3 traffic_matchingRules.py -s 40000001 -e 41146055 -o output/traffic_accidents_types.arules.pairs10per.4 & 

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done
echo "all jobs finished"
cp output/traffic_accidents_types.arules.pairs10per.0 output/traffic_accidents_types.arules.pairs10per
tail -n+2 output/traffic_accidents_types.arules.pairs10per.1 >> output/traffic_accidents_types.arules.pairs10per
tail -n+2 output/traffic_accidents_types.arules.pairs10per.2 >> output/traffic_accidents_types.arules.pairs10per
tail -n+2 output/traffic_accidents_types.arules.pairs10per.3 >> output/traffic_accidents_types.arules.pairs10per
tail -n+2 output/traffic_accidents_types.arules.pairs10per.4 >> output/traffic_accidents_types.arules.pairs10per

python3 traffic_translateURIs.py
python3 traffic_filterRules.py
python3 traffic_selectRules.py
python3 traffic_translateRules.py
