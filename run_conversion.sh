#!/bin/bash

# Check if enough arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <conversion_type> <input_file_path>"
    echo "Conversion types: bell, capitalgroup, cbcc, wex"
    echo "Example: $0 wex input/some_file.csv"
    exit 1
fi

CONVERSION_TYPE=$1
INPUT_FILE=$2

# Map the type to the actual python script name in src/
case "$CONVERSION_TYPE" in
    "bell")
        SCRIPT="convert-bell.py"
        ;;
    "capitalgroup")
        SCRIPT="convert-capitalgroup.py"
        ;;
    "cbcc")
        SCRIPT="convert-cbcc-statement.py"
        ;;
    "wex")
        SCRIPT="convert-wex.py"
        ;;
    *)
        echo "Error: Unknown conversion type '$CONVERSION_TYPE'"
        echo "Allowed: bell, capitalgroup, cbcc, wex"
        exit 1
        ;;
esac

echo "Running conversion for $CONVERSION_TYPE using src/$SCRIPT"

# Run the docker container
# We removed the extra "python" argument from the command line
# because the Dockerfile ENTRYPOINT is already ["python"]
docker run --rm \
  -v "$(pwd):/app" \
  -w /app \
  csv-to-qif:latest \
  src/$SCRIPT "$INPUT_FILE"

