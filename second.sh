#!/bin/bash 

dxEngineNonProd=$1
shift 
templateID=$1
shift
templateLatestSnap=$1
shift 
major=$1
shift
minor=$1
shift 
micro=$1 
shift 
templateReference=$1
shift
templateBranch=$1

curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/session \
   -c "cookies.txt" -H "Content-Type: application/json" <<EOF
{
   "type": "APISession",
   "version": {
       "type": "APIVersion",
       "major": ${major},
       "minor": ${minor},
       "micro": ${micro}
  }
}
EOF

curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/login \
-b "cookies.txt" -c "cookies.txt" -H "Content-Type: application/json" <<EOF
{
"type": "LoginRequest",
"username": "admin",
"password": "Fwdview01!"
}
EOF

curl -s -X POST -k --data @- http://${dxEngineNonProd}/resources/json/delphix/database/${templateID}/refresh -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"timeflowPointParameters":{"snapshot":"${templateLatestSnap}","type":"TimeflowPointSnapshot"},"type":"RefreshParameters"}
EOF

sleep 100 

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
