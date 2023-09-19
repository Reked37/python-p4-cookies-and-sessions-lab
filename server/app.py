#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    number_of_views= session.get('page_views',0)
    print(number_of_views)
    if number_of_views >=3:
        number_of_views += 1
        session['page_views']=number_of_views
        response_body={"message":"Maximum pageview limit reached"}
        response=make_response(
            response_body,
            401
        )
        return response
    else:
        number_of_views += 1
        session['page_views']=number_of_views
        article= Article.query.filter_by(id=id).first()
        article_dict=article.to_dict()
        response=make_response(
            article_dict,
            200
        )
        return response


if __name__ == '__main__':
    app.run(port=5555)
