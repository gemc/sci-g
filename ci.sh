#!/usr/bin/bash

# SCI-G Continuous Integration
# ----------------------------
#
# Original Instructions:
# https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
# The steps on "main" are done on the Github page under "Actions"

echo
echo "SCI-G Validation: $1"
echo
time=$(date)
echo "::set-output name=time::$time"


ls -l /jlab/
