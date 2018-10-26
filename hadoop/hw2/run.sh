hadoop dfs -rm -r out
git pull
gradle jar
<<<<<<< HEAD
hadoop jar build/libs/hw2.jar "$@" "$@" "$@"
=======
hadoop jar build/libs/hw2.jar UrlsToFile "$@" "$@"
>>>>>>> 92a25a0735fed5b30d65172b11018a8b47a61cfd
