import argparse
import json
import requests
from fake_headers import Headers


class Instagram:
    @staticmethod
    def build_param(username):
        params = {
            'username': username,
        }
        return params

    @staticmethod
    def build_headers(username):
        return {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'https://www.instagram.com/{username}/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': Headers().generate()['User-Agent'],
            'x-asbd-id': '198387',
            'x-csrftoken': 'VUm8uVUz0h2Y2CO1SwGgVAG3jQixNBmg',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest',
        }

    @staticmethod
    def make_request(url, params, headers, proxy=None):
        response = None
        if proxy:
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            response = requests.get(
                url, headers=headers, params=params, proxies=proxy_dict)
        else:
            response = requests.get(
                url, headers=headers, params=params)
        return response

    @staticmethod
    def scrape(username, proxy=None):
        try:
            headers = Instagram.build_headers(username)
            params = Instagram.build_param(username)
            response = Instagram.make_request(
                'https://www.instagram.com/api/v1/users/web_profile_info/',
                headers=headers, params=params, proxy=proxy
            )
            if response.status_code == 200:
                profile_data = response.json()['data']['user']
                return profile_data
            else:
                print('Error:', response.status_code, response.text)
        except Exception as ex:
            print(ex)

    @staticmethod
    def search_hashtag(hashtag, proxy=None):
        try:
            headers = Instagram.build_headers('')
            params = {
                'context': 'blended',
                'query': hashtag,
                'rank_token': '0.28835121715987904',
                'include_reel': 'true',
            }
            response = Instagram.make_request(
                'https://www.instagram.com/web/search/topsearch/',
                headers=headers, params=params, proxy=proxy
            )
            if response.status_code == 200:
                search_data = response.json()
                if 'hashtags' in search_data:
                    hashtag_data = search_data['hashtags']
                    return hashtag_data
                elif 'places' in search_data:
                    place_data = search_data['places']
                    return place_data
                else:
                    print('No hashtags or places found.')
            else:
                print('Error:', response.status_code, response.text)
        except Exception as ex:
            print(ex)


# Usage example
if __name__ == "__main__":
    # Scrape user profile data
    username = 'example_username'
    profile_data = Instagram.scrape(username)
    if profile_data:
        print(f"Profile Data for {username}:")
        print(json.dumps(profile_data, indent=2))
    
    # Search for a hashtag
    hashtag = 'example_hashtag'
    hashtag_data = Instagram.search_hashtag(hashtag)
    if hashtag_data:
        print(f"Hashtag Data for {hashtag}:")
        print(json.dumps(hashtag_data, indent=2))
