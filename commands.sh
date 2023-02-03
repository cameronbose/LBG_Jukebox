#!/bin/bash 

dxEngineProd=$1 
shift
dxEngineNonProd=$1
shift
sourceID=$1
shift 
vdbID=$1
shift
latestSnap=$1
shift 
specID=$1
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

curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/database/${vdbID}/refresh -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"timeflowPointParameters":{"snapshot":"${latestSnap}","type":"TimeflowPointSnapshot"},"type":"RefreshParameters"}
EOF

curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/replication/spec/${specID}/execute -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{}
EOF

sleep 200 

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
