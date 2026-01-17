#!/bin/bash

XML_GZ_URLS="$1"
XML_GZ_FOLDER="$2"
XML_FOLDER="$3"
WIKIPEDIA_URLS_FILE="$4"
RAW_TEXT="$5"

python xml_processor.py --xml_gz_urls "$XML_GZ_URLS" \
                    --xml_gz_folder "$XML_GZ_FOLDER" \
                    --xml_folder "$XML_FOLDER" \
                    --wikipedia_urls "$WIKIPEDIA_URLS_FILE"
    