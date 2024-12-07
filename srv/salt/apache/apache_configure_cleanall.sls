apache_configure_cleanall:
  file.absent:
    - name: /var/log/httpd

'Remove /etc/httpd':
  file.absent:
    - name: /etc/httpd