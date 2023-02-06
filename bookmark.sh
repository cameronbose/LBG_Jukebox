#!/bin/bash 

dxEngineNonProd=$1
shift 
templateReference=$1
shift
templateBranch=$1

current_date_time="$(date +'%Y-%m-%d %H:%M:%S')"

response=$(curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/selfservice/bookmark \
-b "cookies.txt" -H "Content-Type: application/json"<<EOF
{
    "type": "JSBookmarkCreateParameters",
    "bookmark": {
        "type": "JSBookmark",
        "name": "${current_date_time}",
        "branch": "${templateBranch}"
    },
    "timelinePointParameters": {
        "type": "JSTimelinePointLatestTimeInput",
        "sourceDataLayout": "${templateReference}"
    }
}
EOF)

echo "${response}" > response.txt