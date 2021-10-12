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

# need to add this dir to PYTHONPATH in case the api changed
cd /root
git clone http://github.com/gemc/sci-g
cd sci-g
export PYTHONPATH=/root/sci-g:${PYTHONPATH}

echo
echo Testing Examples
for example in 1_Simple_detector/ex1_1_simple_det 1_Simple_detector/ex1_2_dosimeter
do
	echo
	cd examples/$example
	echo Building Geometry for $example
	./example.py
	echo Running gemc for $example
	gemc example.jcard
	overlaps=`grep G4Exception-START MasterGeant4.log | wc | awk '{print $1}'`
	if (( "$overlaps" == "0" ))
	then
		echo "$overlaps" overlaps detected
	else
		echo "$overlaps" overlaps detected for $example, exiting
		exit 1
	fi
	cd -
done

echo Testing Projects

declare -A projectDir
declare -A gcard

# project directory and jcard. They key itself is the python script used to build the geometry
projectDir["targets.py"]="projects/clas12/targets"
gcard["targets.py"]="target.jcard"

for project in ${!projectDir[@]}
do
	echo
	cd "${projectDir[$project]}"
	echo "Running $project inside ${projectDir[$project]}"
	./$project
	echo Running gemc using jcard "${gcard[$project]}"
	gemc "${gcard[$project]}"
	overlaps=`grep G4Exception-START MasterGeant4.log | wc | awk '{print $1}'`
	if (( "$overlaps" == "0" ))
	then
		echo "$overlaps" overlaps detected
	else
		echo "$overlaps" overlaps detected for $example, exiting
		exit 1
	fi
	cd -
done
