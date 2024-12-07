apache_conf:
  file.managed:
    - name: /etc/httpd/conf/httpd.conf
    - source: salt://apache/files/httpd.conf
#    - require:
#      - pkg: httpd