from flask import Flask, render_template, request
from pycorenlp import StanfordCoreNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import configparser
import tweepy

app = Flask(__name__)

cnt=1

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
	return render_template("tweets.html", tweets=get_tweets(text),search=text)

def get_tweets(username):
	tweets = api.search(q=username,
                           lang="en")
	return [{'tweet': t.text,
    'created_at': t.created_at,
    'username': username,
    'headshot_url': t.user.profile_image_url}
    for t in tweets]

@app.route('/wordcloud' , methods=['GET', 'POST'])
def wordCloud():
    global cnt
    text=request.form['resultWord']
    word=request.form['search']
    cloud = WordCloud(background_color="white").generate(text)
    img_src="static/images/"+str(cnt)+"cloud.png"
    cloud.to_file(img_src)
    cnt = cnt+1
    return render_template("cloud.html",src=img_src)

@app.route('/sentiment' , methods=['GET', 'POST'])
def sentiments():
    text=request.form['result']
    return render_template("sentiment.html", sentiments=get_sentiments(text))

def get_sentiments(tweet):
    text= tweet
    nlp = StanfordCoreNLP('http://localhost:9000')
    result = nlp.annotate(text,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })
    print(result)
    for s in result["sentences"]:
        print("{}: '{}': {} (Sentiment Value) {} (Sentiment)".format(
            s["index"],
            " ".join([t["word"] for t in s["tokens"]]),
            s["sentimentValue"], s["sentiment"]))
    return [{
            " ".join([t["word"] for t in s["tokens"]]),
            s["sentiment"]}
    for s in result["sentences"]]
@app.route('/backk', methods=['GET'])
def backk():
    return render_template('index.html')

if __name__ == "__main__":
	app.run(debug = True)