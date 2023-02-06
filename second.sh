#!/bin/bash 

dxEngineNonProd=$1
shift 
templateID=$1
shift 
templateReference=$1
shift
templateBranch=$1

curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/database/${templateID}/refresh -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"type":"RefreshParameters","timeflowPointParameters":{"type":"TimeflowPointSemantic"}}
EOF

sleep 280 

current_date_time="$(date +'%Y-%m-%d %H:%M:%S')"

curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/selfservice/bookmark -b "cookies.txt" -H "Content-Type: application/json"<<EOF
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
EOF
