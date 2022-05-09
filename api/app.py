#!/usr/bin/env python

import os
from flask import Flask, request, render_template, jsonify, redirect, url_for

# Config imports
from cfg.config import config

# Routes imports
from routes.webhook import webhook
from routes.feed import feed

### Path and configuration parameters ###
script_path = os.path.dirname(os.path.realpath(__file__))
config_path_name = os.path.join(script_path + '/cfg', 'config.ini')
server_config = config('server', config_path_name)

app = Flask(__name__)

''' Blueprints/Routes '''
app.register_blueprint(webhook)
app.register_blueprint(feed)


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print('\033[92m' + 'webhook listening')
    # app.run()

    # Configuracion para usar la api desde host:
    app.run(debug = True,
            port = server_config['port'],
            host = server_config['host'],
            ssl_context='adhoc')
