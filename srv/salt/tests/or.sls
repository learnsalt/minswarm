# /srv/salt/orchestrate/grain_and_pillar.sls

# Example of using grains_cache to get a grain from a minion
get_grain_data:
  salt.function:
    - name: grains.item
    - tgt: 'rocky9t01a'  # Replace with your minion's ID or use a pattern
    - arg:
      - fqdn_ip4  # Example grain to fetch
    - tgt_type: glob

# Storing the result in a grain on the master
store_grain:
  grains.present:
    - name: minion_ip
    - value: {{ salt['cache.grains']('rocky9t01a', 'fqdn_ip4')[0] }}
    - require:
      - salt: get_grain_data

## Example of using pillar data, we need to run a state on the minion to fetch pillar data
#get_pillar_data:
#  salt.state:
#    - tgt: 'minion_id*'  # Replace with your minion's ID or use a pattern
#    - sls: pillar_fetch
#    - tgt_type: glob
#
## A separate state file to fetch pillar data
## /srv/salt/pillar_fetch.sls
#retrieve_pillar:
#  pillar.item:
#    - name: some_pillar_key
#
## Back in the orchestrate file, you can now use this pillar data
#use_pillar_data:
#  salt.function:
#    - name: cmd.run
#    - tgt: 'minion_id*'
#    - arg:
#      - echo {{ salt['cache.pillar']('minion_id', 'some_pillar_key')[0] }}
#    - require:
#      - salt: get_pillar_data
      