from flask import Flask, render_template, request, g
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import urlparse
import re

app = Flask(__name__)


@app.route('/home')
def home():
    
    return render_template('index.html')


@app.route('/sentiment')
def sentiment():
    # IG Sentiment
    ig_usd_jpy = get_ig_sentiment('usd-jpy')
    ig_eur_usd = get_ig_sentiment('eur-usd')
    ig_gbp_usd = get_ig_sentiment('gbp-usd')
    ig_aud_usd = get_ig_sentiment('aud-usd')

    ig_usd_jpy_long = ig_usd_jpy[0]['long']
    ig_usd_jpy_short = 100 - int(ig_usd_jpy_long)

    ig_eur_usd_long = ig_eur_usd[0]['long']
    ig_eur_usd_short = 100 - int(ig_eur_usd_long)

    ig_gbp_usd_long = ig_gbp_usd[0]['long']
    ig_gbp_usd_short = 100 - int(ig_gbp_usd_long)
    
    ig_aud_usd_long = ig_aud_usd[0]['long']
    ig_aud_usd_short = 100 - int(ig_aud_usd_long)
    
    # DAILY FX Sentiment
    results = get_dailyfx_sentiment()
    dy_eur_usd_long = results[0]['dy_eur_usd_long']
    dy_eur_usd_short = results[1]['dy_eur_usd_short']

    return render_template('sentiment.html', \
            ig_usd_jpy_long=ig_usd_jpy_long, ig_usd_jpy_short=ig_usd_jpy_short, \
            ig_eur_usd_long=ig_eur_usd_long, ig_eur_usd_short=ig_eur_usd_short, \
            ig_gbp_usd_long=ig_gbp_usd_long, ig_gbp_usd_short=ig_gbp_usd_short, \
            ig_aud_usd_long=ig_aud_usd_long, ig_aud_usd_short=ig_aud_usd_short, \
            dy_eur_usd_long=dy_eur_usd_long, dy_eur_usd_short=dy_eur_usd_short) 


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


def get_dailyfx_sentiment(): 
    # Had to use PhantomJS to get Javascript on page
    url = 'http://www.dailyfx.com/sentiment'
    browser = webdriver.PhantomJS()
    browser.get(url) 
    html = browser.page_source
    soup = bs(html, 'html.parser')
    
    # Store results
    result =[]
    
    # Find results in html using bs4
    sentiment = soup.find('div', {'class': 'sentiment-panel'})
    sentiment = soup.find_all('div', {'class': 'col-xs-6'})

    # EUR/USD
    eur_usd = sentiment[1].find('span', {'class': 'bullish-color'})
    eur_usd = eur_usd.get_text() 
    dy_eur_usd_long = re.search('[0-9]*', eur_usd).group(0)
    dy_eur_usd_short = 100 - int(dy_eur_usd_long)
    
    result.append({'dy_eur_usd_long': dy_eur_usd_long})
    result.append({'dy_eur_usd_short': dy_eur_usd_short})
    
    # USD/JPY
    usd_jpy = sentiment[2].find('span', {'class': 'bullishcolor'})
    usd_jpy = usd_jpy.get_text()
    dy_usd_jpy_long = re.search('[0-9]*', usd_jpy).group(0)
    dy_usd_jpy_short = 100 - int(dy_usd_jpy_long)

    result.append({'dy_usd_jpy_long': dy_usd_jpy_long})
    result.append({'dy_usd_jpy_short': dy_usd_jpy_short})

    # GBP/USD
    gbp_usd = sentiment[3].find('span', {'class': 'bullishcolor'})
    gbp_usd = usd_jpy.get_text()
    dy_gbp_usd_long = re.search('[0-9]*', gbp_usd).group(0)
    dy_gbp_usd_short = 100 - int(dy_gbp_usd_long)

    result.append({'dy_gbp_usd_long': dy_gbp_usd_long})
    result.append({'dy_gbp_usd_short': dy_gbp_usd_short})
    
    # AUD/USD
    aud_usd = sentiment[4].find('span', {'class': 'bullishcolor'})
    aud_usd = usd_jpy.get_text()
    dy_aud_usd_long = re.search('[0-9]*', aud_usd).group(0)
    dy_aud_usd_short = 100 - int(dy_aud_usd_long)

    result.append({'dy_aud_usd_long': dy_aud_usd_long})
    result.append({'dy_aud_usd_short': dy_aud_usd_short})

    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)
