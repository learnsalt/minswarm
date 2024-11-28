curl -sSKi http://localhost:8001/ \
  -H 'Accept: application/x-yaml' \
  -H "X-Auth-Token:eebc918aa62d5bd706807df7ed94098ffa067e8a" \     
  -d client='runner' \
  -d fun='test.ping' \
  -d arg='rocky9t01a' \
  -d username=saltdev \
  -d password=saltdev \
  -d eauth='pam'



#  curl -sSk http://localhost:8001 \
#  -H "Accept: application/x-yaml" \
#  -H "X-Auth-Token:31eed454a960c0ae41a2d1522deab65dc5f4ce4f" \
#  -d username=saltdev \
#  -d password=saltdev \
#  -d eauth=pam \
#  -d client=wheel \
#  -d fun=key.list_all
