cleanall_apache_test:
  cmd.run:
    - name: systemctl is-active httpd  # Replace with your system's command if different
    - onlyif:
      - fun: service.status
        name: httpd
    - unless:
      - test -z "$(systemctl is-active httpd)"
    - failhard: True