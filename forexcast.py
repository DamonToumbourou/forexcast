from flask import Flask, render_template, request, g
from bs4 import BeautifulSoup as bs
import requests 

app = Flask(__name__)

@app.route('/')
def greeting():
    return render_template('greeting.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

def get_sentiment():
    return None


if __name__ == "__main__":
    app.run(debug=True, port=5001)

