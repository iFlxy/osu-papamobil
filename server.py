from flask import Flask, render_template, request, send_file
import papamobilosu
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
osuweb = papamobilosu.PapamobilOsu()
limiter = Limiter(app=app, key_func=get_remote_address)

@app.route('/')
@limiter.limit("15/minute")
def index():
    try:
        return osuweb.getLatestMap()
    except:
        return 'ratelimit_osuweb'
@app.errorhandler(429)
def ratelimit_handler(e):
    return "ratelimit_api"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)