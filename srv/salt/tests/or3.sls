# /srv/salt/orchestrate/or2.sls

# Example of fetching grains via manage runner
get_grain_data:
  salt.runner:
    - name: manage.status
    - args:
      - 'rocky9t01a'  # Replace with your minion's ID or use a pattern like 'minion_*'
    - kwarg:
        grains: True
        grain: fqdn_ip4  # Specify the grain you want to fetch

# Assuming you want to use this grain in another state or command:
{% set minion_grain = salt['runner.manage.status']('rocky9t01a', grains=True, grain='fqdn_ip4')[0]['return'][0]['grains']['fqdn_ip4'] %}

use_grain:pwd
  salt.function:
    - name: cmd.run
    - tgt: 'rocky9t01a'
    - arg:
      - echo {{ minion_grain }}
    - require:
      - salt: get_grain_data