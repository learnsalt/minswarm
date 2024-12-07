ubuntu_upgrade:
  pkg.uptodate:
    - refresh: True
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
    - name: shutdown -r now
    - bg: True
    - onlyif: salt-call --local pkg.list_upgrades | grep -q .
    - onfail:
      - cmd: notify_reboot_fail

notify_reboot_fail:
  cmd.run:
    - name: echo "Reboot failed on $(hostname)" | mail -s "Reboot Failure Notification" admin@example.com

#ubuntu_upgrade:
#  pkg.uptodate:
#    - refresh: True
#    - require_in:
#      - cmd: reboot_host
#
#reboot_host:
#  cmd.run:
#    - name: shutdown -r now
#    - bg: True
#    - onlyif: salt-call --local pkg.list_upgrades | grep -q .
