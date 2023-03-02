action=$1
if [[ $action == "stream" ]];
then
    python `basename "${0%/*}"`/arxiv-utils/stream.py ${@:2}
    exit 0
else
    echo "invalid action"
    exit 1
fi