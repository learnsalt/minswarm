apache:
  pkg.installed:
    - name: {{ pillar['pkgs']('pkgs:apache', 'httpd') }}