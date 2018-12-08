#!/bin/sh
echo "Running requirements"
pip install -r requirements.txt
# echo "installing Solr"
# curl -LO https://archive.apache.org/dist/lucene/solr/6.5.0/solr-6.5.0.tgz
# mkdir solr
# tar -C solr -xf solr-6.5.0.tgz --strip-components=1
# cd solr
# ./bin/solr start                                    # start solr
# ./bin/solr create -c tester -n basic_config         # create core named 'tester'