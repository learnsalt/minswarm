system.reboot:
  cmd.run:
    - name: 'shutdown -r now'
    - onlyif: 'test -f /var/run/reboot-required'
    - order: last
    - failhard: True
