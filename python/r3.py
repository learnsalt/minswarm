import requests
import json
import logging

# Configure logging settings
# - Level INFO means messages of INFO and above (WARNING, ERROR, CRITICAL) will be logged.
# - Format specifies how each log entry should look like with timestamp, log level, and message.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a logger for this module, which will use the configuration above.
logger = logging.getLogger(__name__)

class SaltAPIClient:
    def __init__(self, salt_url, username, password, eauth='pam'):
        """
        Initialize the SaltAPIClient with connection details.

        :param salt_url: URL of the Salt API endpoint.
        :param username: Username for authentication.
        :param password: Password for authentication.
        :param eauth: External authentication method (default is 'pam').
        """
        self.salt_url = salt_url
        self.username = username
        self.password = password
        self.eauth = eauth
        self.auth_token = None

    def login(self):
        """
        Authenticate with the Salt API to get an authentication token.

        :return: Boolean indicating if authentication was successful.
        """
        try:
            # Prepare the payload for the login request
            payload = {
                'username': self.username,
                'password': self.password,
                'eauth': self.eauth
            }
            headers = {'Accept': 'application/json'}  # We expect JSON response
            
            # Perform the POST request to the login endpoint
            response = requests.post(f'{self.salt_url}/login', data=payload, headers=headers)
            
            # Check if the response was successful
            response.raise_for_status()  # Raises HTTPError for bad status codes

            # Parse the JSON response
            data = response.json()
            if data and 'token' in data['return'][0]:
                # Extract the token if present
                self.auth_token = data['return'][0]['token']
                logger.info("Successfully authenticated and token received.")
                return True
            else:
                logger.error("Authentication failed: Token not found in response.")
                return False

        except requests.exceptions.RequestException as e:
            # Log any request-related errors (e.g., connection errors, timeouts)
            logger.error(f"Login failed due to a network error: {e}")
            return False

    def run_command(self, tgt, fun, arg=None, expr_form='glob'):
        """
        Execute a command via Salt API.

        :param tgt: Target specification for Salt minions.
        :param fun: The function to execute on the minions.
        :param arg: Arguments for the function (optional).
        :param expr_form: Expression form for targeting (default is 'glob').
        :return: JSON response from the API or None if an error occurred.
        """
        # Ensure we have an auth token before making a request; if not, try to login
        if not self.auth_token:
            if not self.login():
                raise Exception("Failed to authenticate")

        payload = {
            'client': 'local',  # Local client for direct execution on minions
            'tgt': tgt,         # Target matches for the command
            'fun': fun,         # Function to execute
            'expr_form': expr_form  # How to interpret the target expression
        }
        if arg:
            payload['arg'] = arg  # Add arguments to the payload if provided

        headers = {'Accept': 'application/json', 'X-Auth-Token': self.auth_token}
        try:
            # Make the POST request to execute the command
            response = requests.post(f'{self.salt_url}', data=payload, headers=headers)
            response.raise_for_status()  # Ensure we got a 2xx response
            
            # Return the JSON response if successful
            return response.json()
        except requests.exceptions.HTTPError as err:
            # Log HTTP errors (like 4xx or 5xx status codes)
            logger.error(f"HTTP error occurred: {err}")
        except requests.exceptions.RequestException as e:
            # Log any other request-related errors
            logger.error(f"An error occurred while making the request: {e}")
        return None

    def handle_and_log_errors(self, error):
        """
        Handle and log any errors that occur.

        :param error: The error object to be logged.
