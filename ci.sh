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

function run_geometry_gemc_target {
	local dir=projects/clas12/targets
	local script=targets.py
	local gcard=target.jcard
	local variation="$1"
	echo "Testing dir: $dir"
	cd "$dir"
	echo "Building geometry with $script (variation: $variation)"
	./"$script" "$variation"
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
	run_geometry_gemc examples/geometry/dosimeter example.py example.json
	run_geometry_gemc examples/geometry/simple_flux example.py example.json
	run_geometry_gemc projects/clas12/targets targets.py target_lh2.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_c12.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_lh2e.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_ld2.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_pol_targ.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_bonus.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_pb_test.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_nd3.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_sn118.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_pb208.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_cu63.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_al27.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_hdice.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_longitudinal.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_transverse.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_apollo_nh3.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_apollo_nd3.jcard
}

function run_targets {
	run_geometry_gemc projects/clas12/targets targets.py target_lh2.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_c12.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_lh2e.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_ld2.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_pol_targ.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_bonus.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_pb_test.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_nd3.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_sn118.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_pb208.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_cu63.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_al27.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_hdice.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_longitudinal.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_transverse.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_apollo_nh3.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_apollo_nd3.jcard
	run_targets_comparison
}

function run_targets_comparison {
	local _gemc2_git_url="https://github.com/gemc/clas12Tags"
	local _gemc2_clone_dir="/tmp/gemc2-to-compare"
	local _gemc2_files_dir="$_gemc2_clone_dir/5.0/experiments/clas12/targets"
	local _gemc3_files_dir="./projects/clas12/targets"
	echo "Cloning GEMC2 repository $_gemc2_git_url to get GEMC2 files in $_gemc2_files_dir to use for comparison"

	git clone "$_gemc2_git_url" "$_gemc2_clone_dir"
	./compare_geometry.py --gemc2-path-template "$_gemc2_files_dir/target__geometry_{}.txt" --gemc3-path-template "$_gemc3_files_dir/clas12Target__geometry_{}.txt"
}

echo
echo "SCI-G Validation"
echo
time=$(date)
echo "::set-output name=time::$time"

if [ $# -eq 3 ]; then
	echo "Running individual check" "$1" "$2" "$3"
	run_geometry_gemc "$1" "$2" "$3"
elif [ "$1" = "targets" ]; then
	echo "Running all target checks"
	run_targets
else
	echo "Running all checks"
	run_all
fi
