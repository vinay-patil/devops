import os
import optparse
import hashlib
import urllib2
import redis

from flask import Flask
from flask import Response
from flask import json

app = Flask(__name__)
app.config.from_object('config')

app.redis = redis.StrictRedis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB']
)


def fetch_random_text():
    req = urllib2.Request(
        url=app.config['TEXT_API'],
        headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    )
    response = urllib2.urlopen(req)
    data = json.loads(response.read())

    return data['text_out']


def save_text_in_redis(text):
    key = hashlib.md5(text).hexdigest()
    try:
        app.redis.set(key, text)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False

    return True


@app.route("/")
def main():
    random_text = fetch_random_text()
    text_saved_ok = save_text_in_redis(random_text)
    response_json = json.dumps({
        'text': random_text,
        'savedOk': text_saved_ok
    })

    app.logger.info(response_json)

    return Response(response_json, status=200, mimetype='application/json')



if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
        help="Hostname of the Flask app [default 127.0.0.1]",
        default="127.0.0.1"
    )
    parser.add_option("-P", "--port",
        help="Port for the Flask app [default 5000]",
        default="5000"
    )
    (options, args) = parser.parse_args()

    app.run(host=options.host, port=int(options.port))
