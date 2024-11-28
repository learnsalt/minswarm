curl -sSk http://localhost:8001 \
  -H "Accept: application/x-yaml" \
  -H "X-Auth-Token:db38511573423052e8a3d46c93f547f6f7edc0be" \
  -d username=saltdev \
  -d password=saltdev \
  -d eauth=pam \
  -d client=wheel \
  -d fun=key.list_all
