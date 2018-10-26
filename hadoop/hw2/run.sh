hadoop dfs -rm -r out
git pull
gradle jar
hadoop jar build/libs/hw2.jar UrlsToFile "$@" "$@"
