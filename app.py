from flask import Flask, request
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

@app.route('/add', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # content = request.get_json(force=True)
        return  request.get_json(force=True)
    else:
        return 'get url'

# @app.route('/api/add-clair-result/<uuid>', methods=['GET', 'POST'])
# def addClairResult(uuid):
#     content = request.get_json(force=True)
#     print content
#     return uuid

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)