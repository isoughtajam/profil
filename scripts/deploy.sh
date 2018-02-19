#!/bin/bash

# copy executable js to a directory
rsync -arv --exclude-from='exclusions.txt' ../static/* $1