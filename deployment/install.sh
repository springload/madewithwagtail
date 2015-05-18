#!/bin/bash
# Only used for deployment

REQUIREMENTS_FILE=$1

# Install pip dependencies, recursively and in order
filename="$REQUIREMENTS_FILE"

install_reqs()
{
    while read -r line || [[ -n $line ]]
    do
        if [[ -n "$line" && "$line" =~ ^\-r ]];then
            for word in $line; do
                echo $word
            done
            echo "INSTALLING file $word"
            install_reqs "requirements/$word"
        elif [[ -n "$line" && "$line" != [[:blank:]#]* ]];then
            echo "INSTALLING package $line"
            pip install $line
        fi
    done < "$1"
}

install_reqs $filename
