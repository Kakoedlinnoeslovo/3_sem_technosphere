#!/usr/bin/env bash

set -e
set -o pipefail

Log(){
    echo "[$( date + %c)] $*" >&2
}

OUTDIR = hw3/out
RESFILE = temps.kml
NREDUCERS = 4

Lof "BUILDING"
./gradlew jar

Log "REMOVING previous directory"

hadoop fs -rm -r -f $OUTDIR


Log "RUNNING JOB"

hadoop jar ./build/libs/hw3.jar SecondarySortDemo \
            -Dmapreduce.job.reduces  = $NREDUCRERS \
            /data/seminar2/meteo/*.gz $OUTDIR

hadoop fs -text "$OUTDIR/part-r*" | fgrep "$( date + %d.%m)" | .ids2coords.py > temps.csv
gpsbabel -i csv -f temps.csv -o km; -F $RESFILE

Log "SUCCESS. Result in temps.kml"



