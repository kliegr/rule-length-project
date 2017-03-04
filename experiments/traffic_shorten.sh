cp -f input/traffic_accidents_types_onlyyago.csv output/traffic_accidents_types.shortened.csv
sed --in-place 's#Dbpedia_URL_type_http://dbpedia.org/class/yago[^;]*/##g' output/traffic_accidents_types.shortened.csv
sed --in-place 's;http://dbpedia.org/resource/;;g' output/traffic_accidents_types.shortened.csv
sed --in-place 's;"label";"Label";g' output/traffic_accidents_types.shortened.csv

sed --in-place 's;_;;g' output/traffic_accidents_types.shortened.csv
sed --in-place 's;-;;g' output/traffic_accidents_types.shortened.csv

