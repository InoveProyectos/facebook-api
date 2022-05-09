#!/usr/bin/env python

from flask import Blueprint, Response, request, jsonify, render_template, redirect, url_for
import traceback
from src.Facebook import *


# Blueprint que va a contener el endpoint para obtener los mensajes del feed
home = Blueprint('home', __name__, template_folder = '../templates')

@home.route('/', methods = ['GET'])
def index():
    cookies = request.cookies
    print(cookies)
    return jsonify({'cookies': cookies})