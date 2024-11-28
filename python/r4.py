#! /usr/bin/python3
import requests
import json
import logging

# Configure logging
# This sets up basic configuration for logging. Messages at INFO level and above will be logged to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SaltAPIClient:
    def __init__(self, salt_url, username, password, eauth='pam'):
        """
        Initialize the SaltAPIClient with necessary credentials and settings.

        :param salt_url: The base URL for the Salt API
        :param username: The username for authentication
        :param password: The password for authentication
        :param eauth: The authentication mechanism to use (default is 'pam')
        """
        self.salt_url = salt_url
        self.username = username
        self.password = password
        self.eauth = eauth
        self.auth_token = None  # This will hold our authentication token once we log in

    def login(self):
        """
        Authenticate against the Salt API to retrieve an authentication token.

        :return: Boolean indicating if authentication was successful
        """
        try:
            # Prepare the payload for authentication
            payload = {
                'username': self.username,
                'password': self.password,
                'eauth': self.eauth
            }
            headers = {'Accept': 'application/json'}  # We expect JSON response
            # Attempt to login
            response = requests.post(f'{self.salt_url}/login', data=payload, headers=headers)
            
            # Check for HTTP errors
            response.raise_for_status()  

            # Parse the JSON response
            data = response.json()
            if data and 'token' in data['return'][0]:
                # If authentication was successful, store the token
                self.auth_token = data['return'][0]['token']
                logger.info("Successfully authenticated and token received.")
                return True
            else:
                # Log error if token is not found
                logger.error("Authentication failed: Token not found in response.")
                return False
        except requests.exceptions.RequestException as e:
            # Log network or request related errors
            logger.error(f"Login failed due to a network error: {e}")
            return False

    def run_command(self, tgt, fun, arg=None, expr_form='glob'):
        """
        Execute a command on the specified Salt targets.

        :param tgt: The target specification (e.g., '*' for all minions)
        :param fun: The function to run (e.g., 'test.ping')
        :param arg: Optional arguments for the function
        :param expr_form: The expression form for targeting, default is 'glob'
        :return: JSON response from Salt API or None if an error occurred
        """
        if not self.auth_token:
            if not self.login():
                raise Exception("Failed to authenticate")

        # Prepare the payload for the command execution
        payload = {
            'client': 'local',
            'tgt': tgt,
            'fun': fun,
            'expr_form': expr_form
        }
        if arg:
            payload['arg'] = arg  # Add arguments if provided

        headers = {'Accept': 'application/json', 'X-Auth-Token': self.auth_token}
        try:
            # Send the command to the Salt master
            response = requests.post(f'{self.salt_url}', data=payload, headers=headers)
            response.raise_for_status()  # Will raise an exception if HTTP error
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error occurred while running command: {err}")
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while making the request to run command: {e}")
        return None

    def handle_and_log_errors(self, error):
        """
        A utility method to handle and log errors in a consistent manner.

        :param error: The error object to log
        """
        logger.error(f"An unexpected error occurred: {str(error)}")

# Example usage:
if __name__ == "__main__":
    try:
        # Instantiate the SaltAPIClient with credentials
        salt_api = SaltAPIClient('http://localhost:8001', 'saltdev', 'saltdev')
        
        # Try to login
        if salt_api.login():
            # If login successful, run a command
            results = salt_api.run_command('*', 'test.ping')
            if results:
                print(json.dumps(results, indent=2))
        else:
            logger.error("Authentication failed.")
    except Exception as e:
        # Catch and log any unhandled exceptions during the main execution
        salt_api.handle_and_log_errors(e)
