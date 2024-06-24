from flask import Flask
from ntscraper import Nitter

app = Flask(__name__)
scraper = Nitter()

@app.route('/')
def hello_world():
    return 'Nexis Twitter Faucet v1'

@app.route('/search/<value>')
def search(value):
    tweets = scraper.get_tweets(str(value),mode='user',number=5)
    print(tweets)
    return f'You searched for: {value}'

if __name__ == '__main__':
    app.run(debug=True)