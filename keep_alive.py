from flask import Flask
from threading import Thread
import logging
from pytz import timezone
from datetime import datetime

logging.basicConfig(
    filename='runtimelog.log',
    level=logging.INFO,
    format=
    f'%(asctime)s UTC+05:30 %(levelname)s %(name)s %(threadName)s : %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')


def timetz(*args):
    return datetime.now(tz).timetuple()


app = Flask('')
tz = timezone('Asia/Kolkata')
logging.Formatter.converter = timetz


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
