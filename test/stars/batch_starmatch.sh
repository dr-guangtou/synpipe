#!/bin/bash 

for i in `cat $1`; do 

    datadir='/lustre/Subaru/SSP/rerun/song/random_stars'

    visit=1236
    ccd=$i 

    output=$1"_"$visit"_"$ccd".dat"

    ./matchFakeStars.py $datadir $visit $ccd > $output ; 

done
