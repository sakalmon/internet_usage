from internet_usage import get_usage
from flask import Flask, render_template, Response
import time


app = Flask(__name__)

@app.route('/')
def home():
    global usage
    usage = get_usage()

    return render_template('home.html', usage=usage)

@app.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= usage['used_perc']:
            yield "data:" + str(x) + "\n\n"
            x = x + 1
            time.sleep(0.1)

    return Response(generate(), mimetype= 'text/event-stream')