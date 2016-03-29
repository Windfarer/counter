from flask import Flask, jsonify, current_app
import redis

app = Flask(__name__)
app.redis = redis.Redis(host='localhost')


@app.before_first_request
def init_redis():
    if not current_app.redis.get('counter'):
        current_app.redis.set('counter', 0)


@app.route('/counter')
def counter():
    current_app.redis.incr('counter')
    return jsonify({"counter": int(current_app.redis.get('counter'))})


if __name__ == '__main__':
    app.run(debug=True)
