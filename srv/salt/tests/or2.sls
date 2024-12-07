# /srv/salt/orchestrate/grain_and_pillar.sls

# Example of using grains via a runner to get a grain from a minion
get_grain_data:
  salt.runner:
    - name: grains.get
    - tgt: 'rocky9t01a'  # Replace with your minion's ID or use a pattern
    - arg:
      - fqdn_ip4
    - tgt_type: glob

# Store the result in a variable for later use (assuming Salt version supports this)

{% set minion_grain = salt['runner.grains.get']('rocky9t01a', 'fqdn_ip4', tgt_type='glob')[0] %}

# Use the grain directly in your orchestration
use_grain:
  salt.function:
    - name: cmd.run
    - tgt: 'rocky9t01a'
    - arg:
      - echo {{ minion_grain }}
    - require:
      - salt: get_grain_data

### Example for pillar data remains the same since it involves running a state on a minion
##get_pillar_data:
##  salt.state:
##    - tgt: 'minion_id*'  # Replace with your minion's ID or use a pattern
##    - sls: pillar_fetch
##    - tgt_type: glob
##
### ... rest of your orchestration for pillar usage