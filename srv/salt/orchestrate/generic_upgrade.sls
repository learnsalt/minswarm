generic_upgrade:
  salt.state:
    - tgt: 'G@os_family:Debian or G@os_family:RedHat'
    - sls: generic.upgrade_and_reboot
    - failhard: True
    - onfail:
      - salt.function: notify_orchestrate_fail

notify_orchestrate_fail:
  salt.function:
    - name: cmd.run
    - tgt: 'salt-master'
    - arg:
      - echo "Orchestration failed for generic upgrade" | mail -s "Orchestration Failure Notification" admin@example.com