#! /usr/bin/python3
import ssl
import urllib.request
import time

max_retries = 2
retry_delay = 3  # seconds
context = ssl._create_unverified_context()

for attempt in range(max_retries):
    try:
        #response = urllib.request.urlopen('https://localhost:8001',context=context)
        response = urllib.request.urlopen('http://localhost:8001',context=context)
        # Process the response here
        break
    except urllib.error.URLError as e:
        if attempt < max_retries - 1:
            print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed after {max_retries} attempts. Error: {e}")
