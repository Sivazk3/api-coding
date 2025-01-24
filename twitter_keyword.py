
# Python Script to Extract tweets of a
# particular Hashtag using Tweepy and Pandas

import pandas as pd
import tweepy

# Function to display data of each tweet
def print_tweet_data(n, ith_tweet):
    tweet_data = {
        'timestamp': ith_tweet.created_at,
        'username': ith_tweet.user.screen_name,
        'description': ith_tweet.user.description,
        'location': ith_tweet.user.location,
        'following': ith_tweet.user.friends_count,
        'followers': ith_tweet.user.followers_count,
        'totaltweets': ith_tweet.user.statuses_count,
        'retweetcount': ith_tweet.retweet_count,
        'text': ith_tweet.full_text,
        'hashtags': [tag['text'] for tag in ith_tweet.entities['hashtags']],
        'url': f"https://twitter.com/{ith_tweet.user.screen_name}/status/{ith_tweet.id}"
    }
    return tweet_data

# Function to perform data extraction
def tweet_extraction(api, keyword, date_since=None, num_tweets=100):
    # Creating DataFrame using pandas
    tweet_data = []

    # Cursor to search through Twitter for the required tweets
    tweets = tweepy.Cursor(api.search_tweets,
                           q=keyword, lang="en",
                           since_id=date_since,
                           tweet_mode='extended').items(num_tweets)

    # Iterate over each tweet and extract information
    for tweet in tweets:
        tweet_data.append(print_tweet_data(len(tweet_data) + 1, tweet))

    return tweet_data

if __name__ == '__main__':
    # Enter your own credentials obtained
    # from your developer account
    consumer_key = "QwIUrhUcRJXQfXzBcxZbdAFjn"
    consumer_secret = "bkjd0Wm3bGUaxZeW1T4Z8teFPeclKquMmO51O19UbNaREH6jFK"
    access_key = "1590364288673538050-UtvTI0R7o4acaVS0ZSYPz3VV9yGLT4"
    access_secret = "EnvzvkBpTBfCMpSGq1CjvQsTpw4Lnm0XKI6d90HH3Y5wx"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Enter the hashtag
    print("Enter Twitter Hashtag to search for:")
    keyword = input()

    # Perform data extraction
    tweet_data = tweet_extraction(api, keyword)

    if not tweet_data:
        print(f"No tweets found for keyword '{keyword}'")
    else:
        # Create DataFrame from the extracted tweet data
        df = pd.DataFrame(tweet_data)

        # Save the DataFrame as a CSV file
        filename = f'scraped_tweets_{keyword}.csv'
        df.to_csv(filename, index=False)

        print(f"Data saved to '{filename}'")
