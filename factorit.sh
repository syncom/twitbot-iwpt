#!/bin/sh
# Script returns 0 on success, 1 on failure

# Check existence of first command line argument
# It needs to be a positive integer for the script to work properly
if [ "$#" -ne 1 ] || [ -z "$1" ]
  then
    echo "Usage: $0 POSITIVE_INTEGER (e.g., 20170918)"
    exit 1
fi

# Call the pari-gp script 
(echo "p=$1;"; echo "print(factor(p))") | gp -q
