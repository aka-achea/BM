

from flask import Flask, render_template, request, session, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = 'note.sqlite'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, dbfile)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)


db = SQLAlchemy(app)



class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True)
    # article = db.relationship('Article', backref='tag', lazy='dynamic')
    # users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<{self.id} = {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(15), unique=True, index=True)
    article = db.relationship('Article', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name} Email address is {self.email}>'


class Article(db.Model): # duo
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), index=True)
    title = db.Column(db.String(64), index=True)
    link = db.Column(db.String(1000), index=True)
    source = db.Column(db.String(64), index=True)
    # tag = db.Column(db.Integer, db.ForeignKey('tags.name'))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    email = db.Column(db.Integer, db.ForeignKey('users.email'))

    def __repr__(self):
        return f'<Article {self.title} user is {self.email}>'



# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500

a = [('history','史'),('food','食'),('geography','地')]


class NameForm(FlaskForm):
    keyword = StringField('请输入关键字查询', validators=[Optional()])
    tag = SelectField('标签',validators=[Optional()], choices=a)
    submit = SubmitField('搜')


@app.route('/', methods=['GET', 'POST'])
def index():
    # keyword = None
    # tag = None
    form = NameForm()
    if request.method == 'POST' and form.validate_on_submit():        
        session['keyword'] = form.keyword.data
        form.keyword.data = ''
        session['tag'] = form.tag.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, \
        keyword=session.get('keyword'), tag=session.get('tag') )

