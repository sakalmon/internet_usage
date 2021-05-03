from internet_usage import get_usage
from flask import Flask, render_template, Response
import time


app = Flask(__name__)

@app.route('/')
def home():
    global usage
    usage = get_usage()

    return render_template('home.html', usage=usage)
