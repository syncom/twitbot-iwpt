#!/bin/sh
# Script exit status is 0 on success, 1 on failure

# Check existence of first command line argument
# It needs to be a positive integer for the script to work properly
if [ -z "$1" ]
  then
    echo "Usage: $0 POSITIVE_INTEGER (e.g., 20170918)"
    exit 1
fi

# Call the pari-gp script 
ROOTDIR=`dirname $0`
echo "p=$1; if (isprime(p), print(1), print(0))" | gp -q
