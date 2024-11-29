#! /usr/bin/python3

#####! /opt/saltstack/salt/bin/python3
import requests
import json


class SaltAPIClient:
    def __init__(self, salt_url, username, password, eauth='pam'):
        self.salt_url = salt_url
        self.username = username
        self.password = password
        self.eauth = eauth
        self.auth_token = None

    def login(self):
        """Authenticate to get an auth token."""
        payload = {
            'username': self.username,
            'password': self.password,
            'eauth': self.eauth
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(f'{self.salt_url}/login', data=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data and 'token' in data['return'][0]:
                self.auth_token = data['return'][0]['token']
                return True
        return False

    def run_command(self, tgt, fun, arg=None, expr_form='glob'):
        """Execute a command on the specified targets."""
        if not self.auth_token:
            if not self.login():
                raise Exception("Failed to authenticate")

        payload = {
            'client': 'local',
            'tgt': tgt,
            'fun': fun,
            'expr_form': expr_form
        }
        if arg:
            payload['arg'] = arg

        headers = {'Accept': 'application/json', 'X-Auth-Token': self.auth_token}
        response = requests.post(f'{self.salt_url}', data=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

# Example usage:
if __name__ == "__main__":
    #salt_api = SaltAPIClient('https://your-salt-master-url:8000', 'your_username', 'your_password')    
    salt_api = SaltAPIClient('http://localhost:8001', 'saltdev', 'saltdev')
    
    # Login to get an auth token
    if salt_api.login():
        # Execute a command (e.g., ping all minions)
        results = salt_api.run_command('*', 'test.ping')
        if results:
            print(json.dumps(results, indent=2))
    else:
        print("Authentication failed.")
