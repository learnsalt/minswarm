install_apache:
  salt.state:
    - tgt: 'rocky9t01a'  # Target minions with roles matching 'rocky9t01a'
    - sls: apache.install

configure_apache:
  salt.state:
    - tgt: 'rocky9t01a'
    - sls: apache.configure
    - require:
      - salt: install_apache  # This state will only run after install_apache has completed

startup_apache:
  salt.state:
    - tgt: 'rocky9t01a'
    - sls: apache.startup
    - require:
      - salt: configure_apache  # This state will only run after install_apache has completed