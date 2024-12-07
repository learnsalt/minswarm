# File: /srv/salt/orchestrate/upgrade_reboot.sls

{% set minions = salt['pillar.get']('minions_to_upgrade', []) %}

upgrade_and_reboot:
  salt.state:
    - tgt: {{ minions | join(',') }}
    - sls:
      - system.upgrade
      - system.reboot
    - fail_hard: True
    - fail_function: 'handle_errors'

handle_errors:
  module.run:
    - name: event.send
    - args:
      - 'salt/orchestrate/error'
      - {
          'message': 'Error occurred during upgrade or reboot',
          'minions': {{ minions }},
          'time': {{ salt['grains.get']('time') }}
        }
    - onfail:
      - salt: upgrade_and_reboot
