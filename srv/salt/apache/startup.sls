apache:
  pkg.installed:
    - name: httpd  # Ensure the package is installed

apache_service_enabled:
  service.enabled:
    - name: httpd
    - require:
      - pkg: apache  # Enable the service only after package installation

apache_service_running:
  service.running:
    - name: httpd
    - enable: True  # This will also ensure the service is enabled on boot
    - require:
      - pkg: httpd
      - service: apache_service_enabled  # Start the service after it's enabled
    - watch:
      - pkg: httpd  # Restart if the package is updated