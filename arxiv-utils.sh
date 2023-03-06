action=$1
ROOT=`dirname "$0"`
ROOT=`(cd "$ROOT" && pwd )`
if [[ $action == "stream" ]];
then
    python "$ROOT"/arxiv-utils/stream.py ${@:2}
    exit 0
elif [[ $action == "search" ]];
then
    python "$ROOT"/arxiv-utils/search.py ${@:2}
    exit 0
elif [[ $action == "logs" ]];
then
    python "$ROOT"/arxiv-utils/logs.py ${@:2}
    exit 0
else
    echo "invalid action"
    exit 1
fi
