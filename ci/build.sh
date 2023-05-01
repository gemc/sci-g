#!/usr/bin/env zsh

# Purpose: runs the geometry building scripts for the selected example
# Assumptions:
# 1. The python sci-g main python filename and jcard must match the containing dir name
# 2. The plugin directory, if existing, must be named 'plugin'

# Container run:
# docker run -it --rm jeffersonlab/gemc3:1.0 sh
# git clone http://github.com/gemc/sci-g         /root/sci-g && cd /root/sci-g
# git clone http://github.com/maureeungaro/sci-g /root/sci-g && cd /root/sci-g
# ./ci/build.sh -e examples/simple_flux
# ./ci/build.sh -e examples/dosimeter

# if we are in the docker container, we need to load the modules
if [[ -z "${DISTTAG}" ]]; then
    echo "\nNot in container"
else
    echo "\nIn container: ${DISTTAG}"
    source  /app/localSetup.sh
fi

Help()
{
	# Display Help
	echo
	echo "Syntax: build.sh [-h|e]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-e <example>: build geometry and plugin for <example>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

while getopts ":he:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      e)
         example=$OPTARG
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit 1
         ;;
   esac
done

ExampleNotDefined () {
	echo "Example is not set."
	Help
	exit 2
}

# exit if detector var is not defined
[[ -v example ]] && echo "Building $example" || ExampleNotDefined

DefineScriptName() {
	subDir=$(basename $example)
	script="./"$subDir".py"
}

CopyCadDir() {
	cdir=$1
	echo "Copying $cdir to $GEMCDB_ENV"
	cp -r $cdir $GEMCDB_ENV
}

CreateAndCopyExampleDBs() {
	ls -ltrh ./
	echo
	echo "Running $script"
	$script
	ls -ltrh ./
	subDir=$(basename $example)
	filesToCopy=$(find ./ -name \*.txt -o -name \*.sqlite)
	echo
	echo "Moving $=filesToCopy to $GEMCDB_ENV"
	mkdir -p $GEMCDB_ENV
	mv $=filesToCopy $=sqlite_filesToCopy $GEMCDB_ENV/

	dirToCopy=$(find . -name \*.stl | awk -F\/ '{print $2}' | sort -u)
	for cadDir in $=dirToCopy
	do
		test -d $cadDir && CopyCadDir $cadDir
	done

	# cleaning up
	echo "Cleaning up..."
	test -d __pycache__ && rm -rf __pycache__
	echo "GEMCDB_ENV is $GEMCDB_ENV. Content:"
	ls -ltrh $GEMCDB_ENV/
	echo
}

CompileAndCopyPlugin() {
	echo "Compiling plugin for $example"
	echo
	cd plugin
	scons -j4 OPT=1
	if [ $? -ne 0 ]; then
	    echo "Building plugin for $example failed"
	    exit 1
    fi
	echo "Moving plugins to $GPLUGIN_PATH"
	mv *.gplugin $GPLUGIN_PATH
	scons -c
	# cleaning up
	rm -rf .sconsign.dblite
	cd -
	echo "GPLUGIN_PATH is $GPLUGIN_PATH. Content:"
	ls -ltrh $GPLUGIN_PATH/
}

script=no

# location of geometry database
export GEMCDB_ENV="$(pwd)/systemsTxtDB"
echo "BUILD.SH: GLIBRARY is $GLIBRARY, GPLUGIN_PATH is $GPLUGIN_PATH, GEMCDB_ENV is $GEMCDB_ENV"

DefineScriptName $example

echo
echo "Building geometry for $example"
echo
cd $example
CreateAndCopyExampleDBs

if [[ -d plugin ]]; then
    CompileAndCopyPlugin
else
    echo "No plugin to build."
fi

echo "Done - Success"