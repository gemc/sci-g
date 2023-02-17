#!/usr/bin/env zsh

# Purpose: runs the geometry building scripts for the selected example
# Assumptions:
# 1. The python sci-g main python filename and jcard must match the containing dir name
# 2. The plugin directory, if existing, must be named 'plugin'

# Container run:
# docker run -it --rm jeffersonlab/gemc3:1.0 sh
# git clone http://github.com/gemc/sci-g /root/sci-g && cd /root/sci-g
# git clone http://github.com/maureeungaro/sci-g /root/sci-g && cd /root/sci-g
# ./ci/build.sh -e examples/simple_flux

# if we are in github actions, we need to define the environment
if [[ -z "${GITHUB_WORKSPACE}" ]]; then
    echo "Not in github actions"
else
    echo "In github actions"
    source /usr/share/Modules/init/sh
    source /work/ceInstall/modules/setup.sh
    module load gemc3/1.0
    if [[ $? != 0 ]]; then
        echo "Error loading gemc3 module"
	    exit 1
    fi
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
	echo "Copying $cdir to $GPLUGIN_PATH"
	cp -r $cdir $GPLUGIN_PATH

}

CreateAndCopyExampleTXTs() {
	ls -ltrh ./
	echo
	echo "Running $script"
	$script
	ls -ltrh ./
	subDir=$(basename $example)
	filesToCopy=$(ls | grep \.txt | grep "$subdir")
	echo
	echo "Moving $=filesToCopy to $GPLUGIN_PATH"
	mv $=filesToCopy  $GPLUGIN_PATH

	dirToCopy=$(find . -name \*.stl | awk -F\/ '{print $2}' | sort -u)
	for cadDir in $=dirToCopy
	do
		test -d $cadDir && CopyCadDir $cadDir
	done

	# cleaning up
	echo "Cleaning up..."
	test -d __pycache__ && rm -rf __pycache__
	ls -ltrh ./
	echo
	echo "$GPLUGIN_PATH content:"
	ls -ltrh $GPLUGIN_PATH
}

CompileAndCopyPlugin() {
	echo "Compiling plugin for $example"
	echo
	cd plugin
	scons -j4 OPT=1
	echo "Moving plugins to $GPLUGIN_PATH"
	mv *.gplugin $GPLUGIN_PATH
	scons -c
	# cleaning up
	rm -rf .sconsign.dblite
	cd -
}

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
mkdir -p $GPLUGIN_PATH
script=no

DefineScriptName $example

echo
echo "Building geometry for $example. GPLUGIN_PATH is $GPLUGIN_PATH"
echo
cd $example
CreateAndCopyExampleTXTs

if [[test -d plugin]]; then
    CompileAndCopyPlugin
else
    echo "No plugin to build."
fi
