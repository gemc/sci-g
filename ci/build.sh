#!/usr/bin/env zsh

# Purpose: runs the geometry building scripts for the selected example
# Assumptions:
# 1. The python sci-g main python filename and jcard must match the containing dir name
# 2. The plugin directory, if existing, must be named 'plugin'

# Container run example:
# docker run -it --rm jeffersonlab/gemc:3.0 bash
# git clone http://github.com/gemc/sci-g /root/sci-g && cd /root/sci-g
# ./ci/build.sh -e examples/geometry/simple_flux

# load environment if we're on the container
# notice the extra argument to the source command
TERM=xterm # source script use tput for colors, TERM needs to be specified
FILE=/etc/profile.d/jlab.sh
test -f $FILE && source $FILE keepmine

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

[[ -v $example ]] && echo "Building $example" || ExampleNotDefined

DefineScriptName() {
	subDir=$(basename $example)
	script="./"$subDir".py"
}


CreateAndCopyExampleTXTs() {
	ls -ltrh ./
	echo
	echo Running $script
	$script
	ls -ltrh ./
	filesToCopy=$(git status -s | grep \? | awk '{print $2}' | grep -v \/ | grep \.txt)
	echo
	echo Moving $=filesToCopy to $GPLUGIN_PATH and cleaning up
	echo
	mv $=filesToCopy $GPLUGIN_PATH
	# cleaning up
	test -d __pycache__ && rm -rf __pycache__
	ls -ltrh ./
	echo
}

CompileAndCopyPlugin() {
	echo "Compiling plugin for "$example
	echo
	cd plugin
	scons -j4 OPT=1
	echo Moving plugins to $GPLUGIN_PATH
	mv *.gplugin $GPLUGIN_PATH
	scons -c
	# cleaning up
	rm -rf .sconsign.dblite
	cd -
}

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
script=no

DefineScriptName $example

echo
echo Building geometry for $example. GPLUGIN_PATH is $GPLUGIN_PATH
echo
cd $example
CreateAndCopyExampleTXTs
test -d plugin && CompileAndCopyPlugin || echo "No plugin to build."

