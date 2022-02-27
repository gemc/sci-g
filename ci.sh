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

GEMC2_DATA_CLONE_URL="https://github.com/gemc/clas12Tags"
GEMC2_DATA_CLONE_DIR="/tmp/gemc2-to-compare"

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
	run_examples
	run_targets
	run_forward_carriage
}

function run_examples {
	run_geometry_gemc examples/geometry/dosimeter example.py example.json
	run_geometry_gemc examples/geometry/simple_flux example.py example.json
}

function run_targets {
	run_geometry_gemc projects/clas12/targets targets.py target_lh2.jcard
	run_geometry_gemc projects/clas12/targets targets.py target_c12.jcard
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

function run_forward_carriage {
	run_geometry_gemc projects/clas12/forward_carriage forward_carriage.py forward_carriage_original.jcard
	run_geometry_gemc projects/clas12/forward_carriage forward_carriage.py forward_carriage_fast_field.jcard
	run_geometry_gemc projects/clas12/forward_carriage forward_carriage.py forward_carriage_torus_symmetric.jcard
	run_forward_carriage_comparison
}

function get_gemc2_data_for_comparison {

	echo "Cloning GEMC2 repository $GEMC2_DATA_CLONE_URL to $GEMC2_DATA_CLONE_DIR to use for comparison"

	git clone --quiet "$GEMC2_DATA_CLONE_URL" "$GEMC2_DATA_CLONE_DIR"
}

function run_targets_comparison {

	local _gemc2_files_dir="$GEMC2_DATA_CLONE_DIR/5.0/experiments/clas12/targets"
	local _gemc3_files_dir="./projects/clas12/targets"

	./compare_geometry.py --template-subsystem "target" --gemc2-path "$_gemc2_files_dir/target__geometry_{}.txt" --gemc3-path "$_gemc3_files_dir/clas12Target__geometry_{}.txt"
}

function run_forward_carriage_comparison {

	local _gemc2_files_dir="$GEMC2_DATA_CLONE_DIR/5.0/experiments/clas12/fc"
	local _gemc3_files_dir="./projects/clas12/forward_carriage"

	./compare_geometry.py --template-subsystem "forward_carriage" --gemc2-path "$_gemc2_files_dir/forwardCarriage__geometry_{}.txt" --gemc3-path "$_gemc3_files_dir/clas12ForwardCarriage__geometry_{}.txt"
}

function run_ftof_comparison {

	local _gemc2_files_dir="$GEMC2_DATA_CLONE_DIR/5.0/experiments/clas12/ftof"
	local _gemc3_files_dir="./projects/clas12/ftof"

	./compare_geometry.py --template-subsystem "ftof" --gemc2-path "$_gemc2_files_dir/ftof__geometry_{}.txt" --gemc3-path "$_gemc3_files_dir/FTOF__geometry_{}.txt"
}

function run_volumes_geometry {
	# using this sci-g for the api
	echo "Adding $PWD to PYTHONPATH"
	export PYTHONPATH="$PWD:$PYTHONPATH"

	local dir="$1"
	local script="$2"
	local volumes_files_dir="$3"

	echo "Testing dir: $dir"
	cd "$dir"
	echo "Copying volumes files from $volumes_files_dir"
	cp "$volumes_files_dir"/*__volumes_*.txt . && ls -lh
	echo "Building geometry with $script"
	./"$script"
	cd -
}

function run_volumes_geometry_services {
	local volumes_files_base_dir="$GEMC2_DATA_CLONE_DIR/5.0/experiments/clas12"
	run_volumes_geometry projects/clas12/ftof ftof.py "$volumes_files_base_dir/ftof"
	run_ftof_comparison
}

echo
echo "SCI-G Validation"
echo
time=$(date)
echo "::set-output name=time::$time"

get_gemc2_data_for_comparison

if [ $# -eq 3 ]; then
	echo "Running individual check" "$1" "$2" "$3"
	run_geometry_gemc "$1" "$2" "$3"
elif [ "$1" = "examples" ]; then
	echo "Running all examples checks"
	run_examples
elif [ "$1" = "targets" ]; then
	echo "Running all target checks"
	run_targets
elif [ "$1" = "forward_carriage" ]; then
	echo "Running all forward_carriage checks"
	run_forward_carriage
elif [ "$1" = "volumes_geometry" ]; then
	echo "Running all volumes_geometry_services checks"
	run_volumes_geometry_services
else
	echo "Running all checks"
	run_all
fi
