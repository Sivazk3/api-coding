import praw
import pandas as pd
from flask import redirect, url_for

reddit_client_id = 'Th7P7pEu76iII0P4BNDpwQ'
reddit_client_secret = 'jb2FHNH7YBuLNK6lVGPqNvDuCEoEdQ'
reddit_user_agent = 'Social app'

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)


def reddit_crawler(keyword):
    reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)
    posts = []
    ml_subreddit = reddit.subreddit(keyword)
    for post in ml_subreddit.hot(limit=20):
        posts.append({
            'title': post.title,
            'score': post.score,
            'id': post.id,
            'subreddit': post.subreddit.display_name,
            'url': post.url,
            'num_comments': post.num_comments,
            'body': post.selftext,
            'created': post.created
        })
    posts_df = pd.DataFrame(posts)
    return posts_df