action=$1
machine=$2
message=$3
if [[ $machine == "--igp" ]]; 
then 
    repos=("/scratch/ewalt/ewtils" "/scratch/ewalt/euler-utils" "/scratch/ewalt/pdm/literature" "/scratch/ewalt/pdm/rs-uncertainty")
elif [[ $machine == "--private" ]]; 
then 
    repos=("/home/eliot/ewtils" "/home/eliot/igp/euler-utils" "/home/eliot/igp/pdm/literature" "/home/eliot/igp/pdm/rs-uncertainty")
else 
    echo "invalid machine $machine"; exit 1
fi
if [[ $action == "pull" ]]; 
then 
    for repo in "${repos[@]}"
    do
        echo "Pulling $repo..."
        cd $repo
        git pull
    done
elif [[ $action == "push" ]]; 
then 
    if [[ -z ${message} ]];
    then
        echo "Using default commit message: 'autocommit'"
        message="autocommmit"
    else
        echo "Using commit message $message"        
    fi
    for repo in "${repos[@]}"
    do
        echo "Pulling $repo..."
        cd $repo
        git add . && git commit -m "$message" && git push
    done
else 
    echo "invalid action $action"; exit 1
fi
exit 0