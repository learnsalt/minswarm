curl -sSk http://localhost:8001 \
  -H "Accept: application/x-yaml" \
  -H "X-Auth-Token:31eed454a960c0ae41a2d1522deab65dc5f4ce4f" \
  -d username=saltdev \
  -d password=saltdev \
  -d eauth=pam \
  -d client=wheel \
  -d fun=key.list_all
