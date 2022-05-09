#!/usr/bin/env python

from src.Facebook import *
from flask import Blueprint, Response, request, jsonify, redirect, url_for, render_template
from dotenv import load_dotenv
import os
import sys
import inspect

# Setear import path en directorio api
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# Cargar variables de entorno (archivo .env)
load_dotenv()

feed = Blueprint('feed', __name__)


@feed.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return redirect(url_for('index'))

    body = request.form.to_dict()
    access_token = body.get('accessToken')
    user_id = body.get('userId')

    # Page that the user owns
    accounts = requests.get(
        f'https://graph.facebook.com/{user_id}/accounts?access_token={access_token}')
    accounts = accounts.json().get('data')

    pages = [dict(id=account.get('id'), name=account.get('name'), access_token=account.get('access_token'))
             for account in accounts]

    return render_template('feed.html', pages=pages)


@feed.route('/get-feed', methods=['POST'])
def get_feed():
    body = request.form.to_dict()
    access_token = body.get('access_token')
    page_id = body.get('page_id')

    if not(access_token and page_id):
        print('No se enviaron los parámetros necesarios')
        print(access_token)
        print(page_id)
        return redirect(url_for('index'))

    fb = Facebook(access_token, page_id)

    feed = fb.get_feed()

    return(jsonify(feed))


@feed.route('/get-unanswered-comments', methods=['POST'])
def get_unanswered_comments():
    body = request.form.to_dict()
    access_token = body.get('access_token')
    page_id = body.get('page_id')

    fb = Facebook(access_token, page_id)
    feed = fb.get_feed()

    for post in feed.get('data'):
        for comment in post.get('comments'):
            if fb.already_liked(comment):
                post['comments'].remove(comment)

    return render_template('unanswered_comments.html', context=feed, access_token=access_token, page_id=page_id)


@feed.route('/answer-comment', methods = ['POST'])
def answer_comment():
    access_token = str(request.form.get('access_token'))
    page_id = str(request.form.get('page_id'))
    comment_id = str(request.form.get('comment_id'))
    public_answer = str(request.form.get('public_answer'))
    private_answer = str(request.form.get('private_answer'))

    if not (access_token and page_id and comment_id and public_answer):
        print('No se enviaron los parámetros necesarios')
        return Response(status = 400) 
    
    fb = Facebook(access_token, page_id)

    fb.put_like(comment_id)
    fb.comment(comment_id, public_answer)
    
    if private_answer:
        fb.private_reply(comment_id, private_answer)
    
    return redirect(url_for('index'))