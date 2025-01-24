import requests

def collect_facebook_data(username, access_token):
    api_version = 'v13.0'
    base_url = f'https://graph.facebook.com/{api_version}'
    
    # Step 1: Get the user ID
    user_id_response = requests.get(f'{base_url}/{username}?access_token={access_token}')
    user_id_data = user_id_response.json()
    user_id = user_id_data['id']
    
    # Step 2: Get user profile data
    profile_response = requests.get(f'{base_url}/{user_id}?fields=name,email,gender,location&access_token={access_token}')
    profile_data = profile_response.json()
    
    # Step 3: Print the collected data
    print("========== Facebook Data Collection ==========")
    print(f"Username: {username}")
    print("Profile Data:")
    print(f"Name: {profile_data['name']}")
    print(f"Email: {profile_data.get('email', 'N/A')}")
    print(f"Gender: {profile_data.get('gender', 'N/A')}")
    print(f"Location: {profile_data.get('location', {}).get('name', 'N/A')}")


# Usage example
if __name__ == "__main__":
    username = 'sandy'
    access_token = 'EAAD3IjkVC1cBAKtjRpXz4A1SF09aI6hjP3JBnwu8jH2af7yZCQO5DafdAVdUMoS2noyNHUphaXxLv1sWZCelZBRNFZBjSlqJDNICHORy9i3UbgUn7BLU2Xt9PweOv2G7wZAxKLW8pEa8PIipe3c8swLk9Ih4WCj4ZBZB1djQiZBXtA3IFa6dc7q4UZCdgFZCrpCLPl70CW1l9RsAZDZD'
    collect_facebook_data(username, access_token)
