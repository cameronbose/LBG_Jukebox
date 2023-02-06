#!/bin/bash 

dxEngineProd=$1 
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

curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/database/${vdbID}/refresh -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"timeflowPointParameters":{"snapshot":"${latestSnap}","type":"TimeflowPointSnapshot"},"type":"RefreshParameters"}
EOF

sleep 100

curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/replication/spec/${specID}/execute -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{}
EOF
