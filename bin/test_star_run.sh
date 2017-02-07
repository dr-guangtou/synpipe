#!/usr/bin/env bash
#################
#test script for stars
#
# this adds 100 stars of magnitude 22 to a given visit and CCD
# at random positions
# it then extracts the fake sources to the output source catalog
# based on the pixel positions, which are listed in the header
# of the output, calibrated exposure
# finally, it output diagnostic plots, in addition to the matched fake sources catalog
#################

rootDir=$1
rerunDir=$2
visit=1236
ccd=50

configFile=$FAKES_DIR/test/stars/config_star_test

hscProcessCcd.py $rootDir --rerun=$rerunDir --id visit=$visit ccd=$ccd -C $configFile
runMatchFakes.py $rootDir/rerun/$rerunDir $visit --ccd $ccd -o star_test
#put plotting here
