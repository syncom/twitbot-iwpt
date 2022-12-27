#!/usr/bin/env bash
#
# Script returns 0 on success, 1 on failure
set -euo pipefail

# Check existence of first command line argument
# It needs to be a positive integer for the script to work properly
if [ "$#" -ne 1 ] || [ -z "$1" ]
  then
    echo "Usage: $0 POSITIVE_INTEGER (e.g., 2017)"
    exit 1
fi

SCRIPT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
readonly SCRIPT_DIR

# Call the pari-gp script 
(cat "${SCRIPT_DIR}"/prime_classes/prime_classes.gp; \
echo "p=$1;"; \
echo "iswhatprime(p)") \
| gp -q
