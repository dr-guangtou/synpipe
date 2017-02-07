#!/usr/bin/env bash
#################
#test script for galaxies
#
# this adds fifty galaxies to a given visit and CCD
# at random positions
# the galaxies are from test_exp_data.fits
# and all have exponential profiles
# it then matches the fake sources to the output source catalog
# based on the pixel positions, which are listed in the header
# of the output, calibrated exposure
# finally, it output diagnostic plots, in addition to the matched fake sources catalog
#################

rootDir=$1
rerunDir=$2
visit=1236
ccd=50

configFile=$FAKES_DIR/test/galaxies/config_gal_test

hscProcessCcd.py $rootDir --rerun=$rerunDir --id visit=$visit ccd=$ccd -C $configFile
runMatchFakes.py $rootDir/rerun/$rerunDir $visit --ccd $ccd -o gal_test -c $FAKES_DIR/test/galaxies/test_exp_data.fits -p 
#put plotting here
