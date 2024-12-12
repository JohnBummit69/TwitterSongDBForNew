import os

import requests
csv_path = 'musicresponses.csv'

# Twitter API Bearer Token
BEARER_TOKEN = "bearer token"

def check_twitter_user_exists(username):
    """
    Check if a Twitter username exists.
    Args:
        username (str): The Twitter username to check.
    Returns:
        dict: User profile data if valid, else an error message.
    """
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return {
            "exists": True,
            "username": username,
            "user_id": user_data['data']['id'],
            "name": user_data['data']['name'],
            "profile_url": f"https://twitter.com/{username}"
        }
    elif response.status_code == 404:
        return {
            "exists": False,
            "username": username,
            "error": "User not found."
        }
    else:
        return {
            "exists": False,
            "username": username,
            "error": f"API returned an error: {response.status_code} {response.text}"
        }


username = "username"  # Replace with the username you want to check
result = check_twitter_user_exists(username)
print(result)
