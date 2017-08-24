from flask import Flask, jsonify, current_app, send_file, request, render_template
import redis
import os

REDIS_ENABLED = os.environ.get('REDIS_ENABLED', "false").lower() == 'true'
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT_6379_TCP_PORT') or 6379
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
app = Flask(__name__)

class Counter(object):
    _redis = None

    def __init__(self, redis=None):
        if redis:
            self._redis = redis
            if not self._redis.get('counter'):
                self._redis.set('counter', 0)
        else:
            self._local_counter = 0

    def incr(self):
        if self._redis:
            self._redis.incr('counter')
        else:
            self._local_counter += 1

    def get(self):
        if self._redis:
            return self._redis.get('counter')
        else:
            return self._local_counter

if REDIS_ENABLED:
    app.counter = Counter(redis=redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD))
else:
    app.counter = Counter()

@app.route('/')
def index():
    return render_template('index.html', counter=int(current_app.counter.get()))


@app.route('/counter', methods=["GET", "PUT"])
def get_counter():
    if request.method == 'PUT':
        current_app.counter.incr()
    return jsonify({"counter": int(current_app.counter.get())})

if __name__ == '__main__':
    app.run(debug=True)
