sudo salt-run state.orchestrate orchestrate.upgrade_reboot pillar='{"minions_to_upgrade": ["minion1", "minion2", "minion3"]}'
