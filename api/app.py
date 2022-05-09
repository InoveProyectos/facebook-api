#!/usr/bin/env python

import os
from flask import Flask, Response, request, render_template, redirect, url_for, jsonify

# Config imports
from cfg.config import config

# Routes imports
from routes.webhook import webhook
from routes.feed import feed

# Tools imports
from tools.colors import *

### Path and configuration parameters ###
script_path = os.path.dirname(os.path.realpath(__file__))
config_path_name = os.path.join(script_path + '/cfg', 'config.ini')
server_config = config('server', config_path_name)


app = Flask(__name__)


### Routes ###
app.register_blueprint(webhook)
app.register_blueprint(feed)


@app.route('/docs', methods = ['GET'])
def docs():
    return render_template('docs.html')


@app.route('/home', methods = ['GET'])
def index():
    cookies = request.cookies.to_dict()
    return render_template('home.html')


@app.route('/get_cookies', methods = ['GET'])
def get_cookies():
    # Return browser cookies
    return jsonify(request.cookies.to_dict())


if __name__ == '__main__':
    print(OKGREEN + 'webhook listening')
    # app.run()

    # Configuracion para usar la api desde host:
    app.run(debug = True,
            port = server_config['port'],
            host = server_config['host'],
            ssl_context='adhoc')
