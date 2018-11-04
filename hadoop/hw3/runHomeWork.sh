#!/usr/bin/env bash

#help set
#set -e # Exit immediately if a command exits with a non-zero status.
        #Set -e stops the execution of a script if a command or pipeline has an error

#set -o pipefail #the return value of a pipeline is the status of
                #the last command to exit with a non-zero status,
                #or zero if no command exited with a non-zero status


git pull


#echo test 2> afile.txt    #redirect stderr
#echo test 1> afile.txt    #redirects stdout to afile.txt

#echo test 1>&2 # or echo test >&2   #redirect stdout to stderr


Log() {

    echo "[$( date +%c )] $*" >&2
}

NUMREDUCERS = 4
MINCLICKS  = 2


Log "BUILDING"
./gradlew jar

Log "REMOVING PREVIOUS DIRECTORY"
hadoop fs -rm -r -f SeoSortJobOutput

Log "RUNNING JOB"
hadoop jar ./build/libs/hw3.jar SeoSortJob -Dmapreduce.job.reduces=NUMREDUCERS -Dminclicks=MINCLICKS

Log "SUCCESS. RESULT in SeoSortJobOutput"