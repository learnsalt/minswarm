{% if grains['os_family'] == 'Debian' %}
  {% set upgrade_cmd = 'apt-get upgrade -y' %}
  {% set reboot_cmd = 'shutdown -r now' %}
{% elif grains['os_family'] == 'RedHat' %}
  {% if grains['osmajorrelease']|int >= 8 %}
    {% set upgrade_cmd = 'dnf upgrade -y' %}
  {% else %}
    {% set upgrade_cmd = 'yum update -y' %}
  {% endif %}
  {% set reboot_cmd = 'shutdown -r now' %}
{% endif %}

generic_upgrade:
  cmd.run:
    - name: {{ upgrade_cmd }}
    - failhard: True
    - onfail:
      - cmd: notify_upgrade_fail
    - require_in:
      - cmd: reboot_host

notify_upgrade_fail:
  cmd.run:
    - name: echo "Package upgrade failed on $(hostname)" | mail -s "Upgrade Failure Notification" admin@example.com
    - onlyif: test $? -ne 0  # Run only if the previous command failed

reboot_host:
  cmd.run:
    - name: {{ reboot_cmd }}
    - bg: True
    - onlyif: salt-call --local pkg.list_upgrades | grep -q .
    - onfail:
      - cmd: notify_reboot_fail

notify_reboot_fail:
  cmd.run:
    - name: echo "Reboot failed on $(hostname)" | mail -s "Reboot Failure Notification" admin@example.com
    - onlyif: test $? -ne 0  # Run only if the previous command failed