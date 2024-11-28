curl -sSki http://localhost:8001  -H 'Content-type: application/json' \
    -H "X-Auth-Token:0a9a3e6a273df16e2026cff1f6f270312862f662" \
     -d '[{
        "client": "local",
        "tgt": "*",
        "fun": "test.ping"
    }]'
