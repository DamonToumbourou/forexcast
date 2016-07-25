from flask import Flask, render_template, request, g
from bs4 import BeautifulSoup as bs
import requests 
import re

app = Flask(__name__)


@app.route('/home')
def home():
    
    return render_template('index.html')


@app.route('/sentiment')
def sentiment():
    usd_jpy = get_ig_sentiment('usd-jpy')
    eur_usd = get_ig_sentiment('eur-usd')
    gbp_usd = get_ig_sentiment('gbp-usd')
    aud_usd = get_ig_sentiment('aud-usd')

    usd_jpy_long = usd_jpy[0]['long']
    usd_jpy_short = 100 - int(usd_jpy_long)

    eur_usd_long = eur_usd[0]['long']
    eur_usd_short = 100 - int(eur_usd_long)

    gbp_usd_long = gbp_usd[0]['long']
    gbp_usd_short = 100 - int(gbp_usd_long)
    
    aud_usd_long = aud_usd[0]['long']
    aud_usd_short = 100 - int(aud_usd_long)

    return render_template('sentiment.html', \
            usd_jpy_long=usd_jpy_long, usd_jpy_short=usd_jpy_short, \
            eur_usd_long=eur_usd_long, eur_usd_short=eur_usd_short, \
            gbp_usd_long=gbp_usd_long, gbp_usd_short=gbp_usd_short, \
            aud_usd_long=aud_usd_long, aud_usd_short=aud_usd_short) 

def get_ig_sentiment(trading_pair):
    url = 'http://www.ig.com/au/ig-forex/' + trading_pair
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    
    result = []
    long_ = soup.find('span', {'class': 'long-percent'})
    long_ = long_.get_text()
    long_ = re.search('[0-9]*', long_).group(0)

    result.append({'long': long_})

    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)
