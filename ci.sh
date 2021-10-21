#!/usr/bin/env bash
set -e

# SCI-G Continuous Integration
# ----------------------------
#
# To debug this on the container:
#
# docker run -it --rm jeffersonlab/gemc:3.0 bash
# git clone http://github.com/gemc/sci-g /root/sci-g && cd /root/sci-g
# ./ci.sh

# load environment if we're on the container
FILE=/etc/profile.d/jlab.sh
if test -f "$FILE"; then
    source "$FILE"
fi


function run_geometry_gemc {
	# using this sci-g for the api
	echo "Adding $PWD to PYTHONPATH"
	export PYTHONPATH="$PWD:$PYTHONPATH"

	local dir="$1"
	local script="$2"
	local gcard="$3"

	echo "Testing dir: $dir"
	cd "$dir"
	echo "Building geometry with $script"
	./"$script"
	echo "Running gemc for $gcard"
	gemc "$gcard"
	check_overlaps
	cd -
}

function check_overlaps {
	overlaps=`grep G4Exception-START MasterGeant4.log | wc | awk '{print $1}'`
	if (( "$overlaps" == "0" ))
	then
		echo "$overlaps overlaps detected"
	else
		echo "ERROR! $overlaps overlaps detected. Exiting."
		exit 1
	fi
}

function run_all {
	run_geometry_gemc examples/geometry/dosimeter   example.py example.jcard
	run_geometry_gemc examples/geometry/simple_flux example.py example.jcard
	run_geometry_gemc projects/clas12/targets       targets.py target.jcard
}

echo
echo "SCI-G Validation"
echo
time=$(date)
echo "::set-output name=time::$time"

if [ $# -eq 3 ]; then
	echo "Running individual check"
	run_geometry_gemc "$1" "$2" "$3"
else
	echo "Running all checks"
	run_all
fi
