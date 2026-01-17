#!/bin/bash

URL_FILE="$1"

OUTPUT_FOLDER_PATH="$2"

global_counter=0

batch_number=$(expr $global_counter / 1200 + 2)

while IFS= read -r url
do
    echo "Processing URL: $url"
    echo "Global Counter: $global_counter"
    
    batch_number=$(expr $global_counter / 1200 + 2) 

    batch_output_file="${OUTPUT_FOLDER_PATH}/wikipedia_${batch_number}_token.txt"
    echo "Writing to: $batch_output_file"
    
    python url_reader.py --url "${url}" --output_file_path "${batch_output_file}"

    ((global_counter++))
done < "$URL_FILE"

echo "Text retrieval completed. Results saved to ${OUTPUT_FILE_PATH}_batch_*.txt"