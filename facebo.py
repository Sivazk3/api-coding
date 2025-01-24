import argparse
import json
import requests
from fake_headers import Headers


class Instagram:
    @staticmethod
    def build_param(hashtag):
        params = {
            'query': hashtag,
            'rank_token': '0.28835121715987904',
        }
        return params

    @staticmethod
    def build_headers():
        return {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': Headers().generate()['User-Agent'],
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
                url, headers=headers, params=params, proxies=proxy_dict
            )
        else:
            response = requests.get(url, headers=headers, params=params)
        return response

    @staticmethod
    def scrape_hashtag(hashtag, proxy=None):
        try:
            headers = Instagram.build_headers()
            params = Instagram.build_param(hashtag)
            response = Instagram.make_request(
                'https://www.instagram.com/web/search/topsearch/',
                headers=headers, params=params, proxy=proxy
            )
            if response.status_code == 200:
                search_data = response.json()
                if 'hashtags' in search_data:
                    hashtag_data = search_data['hashtags']
                    return hashtag_data
                else:
                    print(f"No hashtag data found for #{hashtag}")
            else:
                print('Error:', response.status_code, response.text)
        except Exception as ex:
            print(ex)


# Usage example
if __name__ == "__main__":
    # Scrape hashtag data
    hashtag = 'anime'
    hashtag_data = Instagram.scrape_hashtag(hashtag)
    if hashtag_data:
        print(f"Hashtag Data for #{hashtag}:")
        print(json.dumps(hashtag_data, indent=2))
