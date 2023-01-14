#!/bin/bash

set -e
echo "${0}: creating movie index and starting ETL."

sh es_schema.txt
python3 main_process.py
