from flask import Flask, render_template, request, send_file, redirect, url_for
from typing import Callable
import csv
import praw
import pandas as pd
import hashlib
from twitter_keyword import tweet_extraction
import tweepy
from reddit import reddit_crawler
from twitter_keyword import tweet_extraction
from linkedin import scrape_linkedin
from instagram import Instagram


app = Flask(__name__, static_folder='static')




reddit_client_id = 'Th7P7pEu76iII0P4BNDpwQ'
reddit_client_secret = 'jb2FHNH7YBuLNK6lVGPqNvDuCEoEdQ'
reddit_user_agent = 'Social app'

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)
# create a dictionary of users with hashed passwords
passwords = "password"


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        print(email)
        password = request.form['password']
        print(password)

        if password == passwords:
            # Redirect to the home page
            return redirect(url_for('home'))
        else:
            # Render the login template with JavaScript code
            return render_template('login.html', error="Invalid password", run_js=True)

    return render_template('login.html', run_js=False)

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    try:
        # Redirect to the registration confirmation page
        return redirect(url_for('register_confirmation'))
    except Exception as e:
        # Handle any registration errors
        error = str(e)
        return render_template('register.html', error=error)


# Register confirmation route
@app.route('/register-confirmation')
def register_confirmation():
    return render_template('register.html')




@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/createaccount')
def createaccount():
    return render_template('createaccount.html')


consumer_key = "QwIUrhUcRJXQfXzBcxZbdAFjn"
consumer_secret = "bkjd0Wm3bGUaxZeW1T4Z8teFPeclKquMmO51O19UbNaREH6jFK"
access_key = "1590364288673538050-UtvTI0R7o4acaVS0ZSYPz3VV9yGLT4"
access_secret = "EnvzvkBpTBfCMpSGq1CjvQsTpw4Lnm0XKI6d90HH3Y5wx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)





# Update the home route
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'twitter' in request.form:
            # Handle Twitter keyword
            keyword_twi = request.form['keyword']
            print("Keyword (Twitter):", keyword_twi)
            # Call the tweet_extraction function and pass the keyword and api object
            tweet_data = tweet_extraction(api, keyword_twi)
            print(tweet_data)
            return render_template('twitter.html', tweets=tweet_data)
        elif 'reddit' in request.form:
            # Handle Reddit keyword
            keyword = request.form['keyword']
            print("Keyword (Reddit):", keyword)
            # Call the reddit_crawler function and pass the keyword
            posts_data = reddit_crawler(keyword)
            print(posts_data)
            return render_template('reddit.html', posts=posts_data.values.tolist())
        elif 'linkedin' in request.form:
            # Handle LinkedIn keyword
            keyword = request.form['keyword']
            print("Keyword (LinkedIn):", keyword)
            # Call the scrape_linkedin function and pass the keyword
            data = scrape_linkedin(keyword)
            print(data)
            return render_template('linkedin.html', data=data)
        elif 'instagram' in request.form:
            # Handle Instagram keyword
            username = request.form['keyword']
            print("Username (Instagram):", username)
            # Call the scrape_instagram function and pass the username
            data = Instagram.scrape(username)
            print(data)
            return render_template('instagram.html', data=data)
        else:
            error = 'Invalid form input'
            return render_template('home.html', error=error)
    else:
        return render_template('home.html')


@app.route('/linkedin', methods=['POST'])
def linkedin():
    if 'card3' in request.form:
        keyword = request.form['card3']
        print("Keyword (LinkedIn):", keyword)
        # Call the scrape_linkedin function and pass the keyword as an argument
        data = scrape_linkedin(keyword)
        print(data)

        return render_template('linkedin.html', data=data)

    else:
        print("Error")
        error = 'Invalid form input'
        return render_template('home.html', error=error)





@app.route('/twitter', methods=['POST'])
def twitter():
    if 'card1' in request.form:
        keyword = request.form['card1']
        print("Keyword (Twitter):", keyword)
        # Call the tweet_extraction function and pass the keyword and api object
        tweet_data = tweet_extraction(api, keyword)
        print(tweet_data)
        return render_template('twitter.html', tweets=tweet_data)
    else:
        print("Error")
        error = 'Invalid form input'
        return render_template('home.html', error=error)




@app.route('/reddit', methods=['GET', 'POST'])
def reddit():
    if request.method == 'POST':
        keyword = request.form['card2']
        print("Keyword (Reddit):", keyword)
        # Call the reddit_crawler function and pass the keyword
        posts_data = reddit_crawler(keyword)
        print(posts_data)  
        
        # Verify that data is fetched correctly

        # Render the template and pass the DataFrame to it
        return render_template('reddit.html', posts=posts_data.values.tolist())
    else:
        print("Error")
        error = 'Invalid form input'
        return render_template('home.html', error=error)

@app.route('/download_csv')
def download_csv():
    keyword = request.args.get('keyword')
    filename = f'scraped_tweets_{keyword}.csv'

    return send_file(filename, as_attachment=True)

@app.route('/instagram', methods=['POST'])
def instagram_route():
    if 'username' in request.form:
        # Get the username from the form
        username = request.form['username']
        print(username)
        # Call the Instagram.scrap method to retrieve the profile data
        profile_data = Instagram.scrape(username)

        # Check if the profile data is retrieved successfully
        if profile_data is not None:
            # Pass the profile data as a context variable to the template
            return render_template('instagram.html', profile_data=profile_data)
        else:
            error = 'Failed to retrieve Instagram profile data.'
            return render_template('home.html', error=error)
    else:
        error = 'Invalid form input'
        return render_template('home.html', error=error)


@app.route('/facebook', methods=['POST'])
def facebook_route():
    if 'card5' in request.form:
        return render_template('facebook.html')
    else:
        error = 'Invalid form input'
        return render_template('home.html', error=error)


@app.route('/download')
def download():
    keyword = 'your_keyword'
    language = 'english'
    format = 'csv'
    return reddit_crawler(keyword, language, format)


if __name__ == '__main__':
    app.run(port=8000)

