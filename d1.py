#! /opt/saltstack/salt/bin/python3

import salt.wheel
import salt.config
master_opts = salt.config.client_config('/etc/salt/master')
wheel = salt.wheel.WheelClient(master_opts)
wheel.cmd('key.delete', kwarg={'match': 'jerry'})


#from pepper import SaltAPI
#import json
#
## Configuration
#salt_url = 'http://localhost:8001'  # Use 'http' if SSL is disabled
#username = 'saltdev'  # User configured with necessary permissions
#password = 'saltdev'  # PAM, LDAP, etc.
#eauth = 'pam'  # Or 'ldap', depending on your setup
#minion_id_to_delete = 'minion_id_here'  # The ID of the minion whose key you want to delete
#
#def delete_minion(minion_id):
#    try:
#        # Initialize the SaltAPI client
#        client = SaltAPI(
#            url=salt_url,
#            username=username,
#            password=password,
#            eauth=eauth
#        )
#        
#        # Authenticate
#        token = client.login()
#        print(f"Authentication successful. Token: {token}")
#
#        # Use the wheel client to delete the minion key
#        result = client.run(
#            client='wheel',
#            fun='key.delete',
#            match=minion_id
#        )
#
#        if result:
#            print(json.dumps(result, indent=2))
#            print(f"Minion key for {minion_id} has been deleted.")
#        else:
#            print(f"Failed to delete key for minion: {minion_id}")
#
#    except Exception as e:
#        print(f"An error occurred: {e}")
#    finally:
#        # Logout should be called to invalidate the token
#        if client:
#            client.logout()
#
## Call the function with the minion ID
#delete_minion(minion_id_to_delete)
#
