#!/bin/bash 

visit=$1
ccdlis=$2
nstar=$3
mag=$4

for i in `cat $2`; do 

    ccd=$i
    config="config_"$ccd

    cp config_stars $config
    sed -i "s/NSTARS/$nstar/g" $config
    sed -i "s/MAGSTARS/$mag/g" $config;
    
    hscProcessCcd.py /lustre/Subaru/SSP/ --rerun=song/random_stars --id visit=$visit ccd=$ccd -C $config --clobber-config 

done
