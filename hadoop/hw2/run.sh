hadoop dfs -rm -r out
git pull
gradle jar
hadoop jar build/libs/hw2.jar Run /data/hw4/soc-LiveJournal1.txt.gz out
