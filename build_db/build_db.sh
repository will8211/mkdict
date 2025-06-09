#!/bin/bash

./build_database.py
./build_database_moe.py

echo "Enter password for indexing:" 
sudo /usr/bin/indexer --rotate --config /etc/sphinxsearch/sphinx.conf --all

