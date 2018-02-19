#!/bin/bash

# copy executable js to a location in arg
rsync -arv --exclude-from=`echo "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"`'/exclusions.txt' `echo "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"`/../static/* $1
