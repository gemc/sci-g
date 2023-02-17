#!/usr/bin/env zsh

# Purpose:
# Runs gemc using the jcards inside 'tests' and 'overlaps' directory (if existing)
#   inside each example subdirs
# Assumptions: the names of the tests and overlaps directories.

# Container run:
# docker run -it --rm jeffersonlab/gemc3:1.0 sh
# git clone http://github.com/gemc/sci-g         /root/sci-g && cd /root/sci-g
# git clone http://github.com/maureeungaro/sci-g /root/sci-g && cd /root/sci-g
# ./ci/tests.sh -e examples/simple_flux -o

# if we are in github actions, we need to define the environment
if [[ -z "${GITHUB_WORKSPACE}" ]]; then
    echo "Not in github actions"
else
    echo "In github actions"
fi

source /usr/share/Modules/init/sh
source ceInstall/modules/setup.sh
module load gemc3/1.0
if [[ $? != 0 ]]; then
    echo "Error loading gemc3 module"
	exit 1
fi

Help()
{
	# Display Help
	echo
	echo "Syntax: tests.sh [-h|t|o|e]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-t: runs example test. 'tests' directory must contain jcards."
	echo "-o: runs overlaps test. 'overlaps' directory must contain jcards."
	echo "-e <Example>: build geometry and plugin for <Example>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

while getopts ":htoe:" option; do
   case $option in
      h)
         Help
         exit
         ;;
      t)
         testType=tests
         ;;
      o)
         testType=overlaps
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

TestTypeNotDefined() {
	echo "Test type is not set. Exiting"
	Help
	exit 2
}

TestTypeDirNotExisting() {
	echo Test Type dir: $example/$testType not existing
	Help
	exit 3
}

JcardsToRun () {
	test -d $example/$testType && echo Test Type dir: $example/$testType || TestTypeDirNotExisting

	jcards=`ls $example/$testType/*.jcard`

	echo
	echo List of jcards in $testType: $=jcards
}

[[ -v testType ]] && echo Running $testType tests || TestTypeNotDefined

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
jcards=no

./ci/build.sh -e $example
if [ $? -ne 0 ]; then
	echo building system $example failed
	exit 1
fi



cp $GLIBRARY/lib/gstreamer*.gplugin                $GPLUGIN_PATH
cp -r $GLIBRARY/gdynamicDigitization/dosimeterData $GPLUGIN_PATH

# sets the list of jcards to run
JcardsToRun

# for some reason DYLD_LIBRARY_PATH is not passed to this script
export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH

# location of database
export GEMCDB_ENV=systemsTxtDB

for jc in $=jcards
do
	echo Running gemc for $jc
	gemc $jc
	exitCode=$?
	echo
	echo exitCode: $exitCode
	echo

	if [[ $exitCode != 0 ]]; then
		exit $exitCode
	fi
done
