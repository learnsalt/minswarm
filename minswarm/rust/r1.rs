use reqwest;
use serde::{Deserialize, Serialize};
use std::error::Error;
use std::fmt;

// Struct for deserializing the authentication response
#[derive(Serialize, Deserialize, Debug)]
struct AuthResponse {
    token: String,
}

// Struct for deserializing the command execution response
#[derive(Serialize, Deserialize, Debug)]
struct SaltResult {
    #[serde(rename = "return")]
    return_data: Vec<serde_json::Value>,
}

// Custom error types for better error handling
#[derive(Debug)]
enum SaltAPIError {
    AuthenticationError(String),
    RequestError(String),
    JSONParseError(serde_json::Error),
    NetworkError(reqwest::Error),
}

// Implement Display trait for custom errors to provide detailed error messages
impl fmt::Display for SaltAPIError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            SaltAPIError::AuthenticationError(msg) => write!(f, "Authentication error: {}", msg),
            SaltAPIError::RequestError(msg) => write!(f, "Request error: {}", msg),
            SaltAPIError::JSONParseError(err) => write!(f, "JSON parsing error: {}", err),
            SaltAPIError::NetworkError(err) => write!(f, "Network error: {}", err),
        }
    }
}

// Implement Error trait for SaltAPIError to be used with the ? operator and Result
impl Error for SaltAPIError {}

// Helper function to handle HTTP requests with error checking
async fn send_request(client: &reqwest::Client, url: &str, data: serde_json::Value, token: Option<&str>) -> Result<serde_json::Value, SaltAPIError> {
    // Prepare the request
    let mut req = client.post(url);

    // If a token is provided, add it to the headers
    if let Some(t) = token {
        req = req.header("X-Auth-Token", t);
    }

    // Send the request and handle potential network errors
    let response = req
        .json(&data)
        .send()
        .await
        .map_err(|e| SaltAPIError::NetworkError(e))?;

    // Check if the request was successful
    if !response.status().is_success() {
        return Err(SaltAPIError::RequestError(format!("Request failed with status: {}", response.status())));
    }

    // Parse the JSON response
    let body = response
        .json::<serde_json::Value>()
        .await
        .map_err(|e| SaltAPIError::JSONParseError(e))?;

    // Return the parsed JSON body
    Ok(body)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Create a new HTTP client
    let client = reqwest::Client::new();
    let salt_master_url = "http://your-salt-master-url:8000";
    let username = "your_username";
    let password = "your_password";
    let eauth = "pam";  // Authentication mechanism

    // Authenticate to get a token
    match send_request(
        &client,
        &format!("{}/login", salt_master_url),
        serde_json::json!({
            "username": username,
            "password": password,
            "eauth": eauth
        }),
        None,
    ).await {
        Ok(auth_body) => {
            // Parse the authentication response to extract the token
            let auth_response: AuthResponse = serde_json::from_value(auth_body)
                .map_err(SaltAPIError::JSONParseError)?;

            println!("Authentication Token: {:?}", auth_response.token);

            // Use the token to execute a command (e.g., test.ping all minions)
            match send_request(
                &client,
                salt_master_url,
                serde_json::json!({
                    "client": "local",
                    "tgt": "*",
                    "fun": "test.ping"
                }),
                Some(&auth_response.token),
            ).await {
                Ok(command_body) => {
                    // Parse the command execution result
                    let command_response: SaltResult = serde_json::from_value(command_body)
                        .map_err(SaltAPIError::JSONParseError)?;
                    println!("Command Result: {:?}", command_response.return_data);
                },
                // Handle any errors that occurred during command execution
                Err(e) => eprintln!("Error executing command: {}", e),
            }
        },
        // Handle any errors that occurred during authentication
        Err(e) => eprintln!("Error authenticating: {}", e),
    }

    Ok(())
}