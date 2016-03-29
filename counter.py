from flask import Flask, jsonify, current_app, send_file, request
import redis
import os

REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT_6379_TCP_PORT') or 6379
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
app = Flask(__name__)
app.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


@app.before_first_request
def init_redis():
    if not current_app.redis.get('counter'):
        current_app.redis.set('counter', 0)


@app.route('/')
def index():
    return send_file('static/index.html')


@app.route('/counter', methods=["GET", "PUT"])
def get_counter():
    if request.method == 'PUT':
        current_app.redis.incr('counter')
    return jsonify({"counter": int(current_app.redis.get('counter'))})

if __name__ == '__main__':
    app.run(debug=True)
