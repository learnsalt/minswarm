stop_apache:
  salt.state:
    - tgt: 'rocky9t01a'  # Target minions with roles matching 'rocky9t01a'
    - sls: apache.stop

apache_pkg_remove:
  salt.state:
    - tgt: 'rocky9t01a'
    - sls: apache.apache_pkg_remove
    - require:
      - salt: stop_apache  # This state will only run after stop_apache has completed

apache_configure_cleanall:
  salt.state:
    - tgt: 'rocky9t01a'
    - sls: apache.apache_configure_cleanall
    - require:
      - salt: apache_pkg_remove  # This state will only run after

cleanall_apache_test:
  salt.state:
    - tgt: 'rocky9t01a'
    - sls: apache.apache_configure_cleanall
    - require:
      - salt: apache_configure_cleanall  # This state will only run after