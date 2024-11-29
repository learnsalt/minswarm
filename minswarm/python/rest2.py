#! /usr/bin/python3
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SaltAPIClient:
    def __init__(self, salt_url, username, password, eauth='pam'):
        self.salt_url = salt_url
        self.username = username
        self.password = password
        self.eauth = eauth
        self.auth_token = None

    def login(self):
        """Authenticate to get an auth token."""
        try:
            payload = {
                'username': self.username,
                'password': self.password,
                'eauth': self.eauth
            }
            headers = {'Accept': 'application/json'}
            response = requests.post(f'{self.salt_url}/login', data=payload, headers=headers)
            response.raise_for_status()  # This will raise an HTTPError for bad responses

            data = response.json()
            if data and 'token' in data['return'][0]:
                self.auth_token = data['return'][0]['token']
                logger.info("Successfully authenticated and token received.")
                return True
            else:
                logger.error("Authentication failed: Token not found in response.")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Login failed due to a network error: {e}")
            return False

    def run_command(self, tgt, fun, arg=None, expr_form='glob'):
        """Execute a command on the specified targets."""
        if not self.auth_token:
            if not self.login():
                raise Exception("Failed to authenticate")

            #            'client': 'local',
        payload = {
            'client': 'wheel',
            'tgt': tgt,
            'fun': fun,
            'expr_form': expr_form
        }
        if arg:
            payload['arg'] = arg

        headers = {'Accept': 'application/json', 'X-Auth-Token': self.auth_token}
        try:
            response = requests.post(f'{self.salt_url}', data=payload, headers=headers)
            response.raise_for_status()  # This will raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error occurred: {err}")
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request: {e}")
        return None

    def handle_and_log_errors(self, error):
        """Generic error handling and logging method."""
        logger.error(f"An error occurred: {str(error)}")

# Example usage:
if __name__ == "__main__":
    try:
        # salt_api = SaltAPIClient('https://your-salt-master-url:8000', 'your_username', 'your_password')
        salt_api = SaltAPIClient('http://localhost:8001', 'saltdev', 'saltdev')        
        if salt_api.login():
            # Execute a command (e.g., ping all minions)
            results = salt_api.run_command('*', 'test.ping')
            if results:
                print(json.dumps(results, indent=2))
        else:
            logger.error("Authentication failed.")
    except Exception as e:
        salt_api.handle_and_log_errors(e)
