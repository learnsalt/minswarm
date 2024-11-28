curl -sSk http://localhost:8001/login \
  -H "Accept: application/x-yaml" \
  -d username=saltdev \
  -d password=saltdev \
  -d eauth=pam 
