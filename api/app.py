#!/usr/bin/env python

import os
from flask import Flask, Response, request, render_template, redirect, url_for

# Config imports
from cfg.config import config

# Routes imports
from routes.webhook import webhook
from routes.feed import feed
from routes.facebook_login import fb_login

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
app.register_blueprint(fb_login)

@app.route('/', methods = ['GET'])
def index():
    return redirect(url_for('feed.feed_get'))


@app.route('/docs', methods = ['GET'])
def docs():
    return render_template('docs.html')


if __name__ == '__main__':
    print(OKGREEN + 'webhook listening')
    # app.run()

    # Configuracion para usar la api desde host:
    app.run(debug = False,
            port = server_config['port'],
            host = server_config['host'],
            ssl_context='adhoc')
