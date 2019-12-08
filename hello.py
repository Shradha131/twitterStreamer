from flask import Flask, render_template, request

import configparser
import tweepy

app = Flask(__name__)

config = configparser.RawConfigParser()
config.read('private.properties')
TWITTER_APP_KEY=config.get('SecretKeys', 'TWITTER_APP_KEY');
TWITTER_APP_SECRET=config.get('SecretKeys', 'TWITTER_APP_SECRET');
TWITTER_KEY=config.get('SecretKeys', 'TWITTER_KEY');
TWITTER_SECRET=config.get('SecretKeys', 'TWITTER_SECRET');

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/tweet' , methods=['GET', 'POST'])
def tweets():
	text=request.form.get('name')
	print(text)
	return render_template("tweets.html", tweets=get_tweets(text))

def get_tweets(username):
	tweets = api.search(q=username,
                           lang="en")
	return [{'tweet': t.text,
    'created_at': t.created_at,
    'username': username,
    'headshot_url': t.user.profile_image_url}
    for t in tweets]

@app.route('/backk', methods=['GET'])
def backk():
    return render_template('index.html')

if __name__ == "__main__":
	app.run(debug = True)