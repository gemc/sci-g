#!/usr/bin/bash -e

# SCI-G Continuous Integration
# ----------------------------
#
# Original Instructions:
# https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
# The steps on "main" are done on the Github page under "Actions"

# load environment
source /etc/profile.d/jlab.sh

echo
echo "SCI-G Validation: $1"
echo
time=$(date)
echo "::set-output name=time::$time"

cd $GEMC/sci-g
git pull

echo
echo Running Examples
for example in 1_Simple_detector/ex1_1_simple_det 1_Simple_detector/ex1_2_dosimeter
do
	echo
	cd examples/$example
	echo Building Geometry for $example
	./example.py
	echo Running gemc for $example
	gemc example.jcard
	cd -
done
