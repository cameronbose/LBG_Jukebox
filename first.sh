#!/bin/bash 

dxEngineProd=$1 
shift
vdbID=$1
shift
latestSnap=$1
shift 
specID=$1

curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/database/${vdbID}/refresh -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{"timeflowPointParameters":{"snapshot":"${latestSnap}","type":"TimeflowPointSnapshot"},"type":"RefreshParameters"}
EOF 

sleep 280

curl -s -X POST -k --data @- http://${dxEngineProd}/resources/json/delphix/replication/spec/${specID}/execute -b "cookies.txt" -H "Content-Type: application/json"<<EOF
{}
EOF 
