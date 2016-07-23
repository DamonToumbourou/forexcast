from flask import Flask, render_template, request, g
from bs4 import BeautifulSoup as bs
import requests 

app = Flask(__name__)

@app.route('/')
def 
