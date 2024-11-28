curl -sSk http://localhost:8001 \
  -H "Accept: application/x-yaml" \
  -H "X-Auth-Token: your_auth_token" \
  -d client=wheel \
  -d fun=key.delete \
  -d match=minion_id
