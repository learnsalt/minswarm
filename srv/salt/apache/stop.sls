#apache:
#  pkg.installed:
#    - name: httpd  # Ensure the package is installed
#
#apache_service_enabled:
#  service.enabled:
#    - name: httpd
#    - require:
#      - pkg: apache  # Enable the service only after package installation

#apache_service_stop:
#  service.dead:
#    - name: httpd

apache_service_stop:
  service.dead:
    - name: httpd  # Make sure this matches your service name
    - enable: False # Optional: disable the service from starting at boot
