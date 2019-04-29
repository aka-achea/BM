

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

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(15), unique=True)

    def __repr__(self):
        return f'<{self.name} : {self.email}>'


class Article(db.Model): # duo
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), index=True)
    title = db.Column(db.String(64), index=True)
    link = db.Column(db.String(1000), index=True)
    tag_id = db.Column(db.String(20),db.ForeignKey('tags.id'),nullable=False)
    tag = db.relationship('Tag',backref='articles')
    src_id = db.Column(db.String(20),db.ForeignKey('sources.id'),nullable=False)
    src = db.relationship('Source',backref='articles')
    user_id = db.Column(db.String(20),db.ForeignKey('users.id'),nullable=False) 
    user = db.relationship('User',backref='articles')

    def __repr__(self):
        return f'<{self.title} : {self.tag.name} : {self.user.name}>'


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Tag=Tag, Source=Source, Article=Article)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


class NameForm(FlaskForm):
    tags = Tag.query.all()
    choice = [] #(data,displayname)
    for t in tags:
        choice.append((str(t.id),t.name))
    keyword = StringField('请输入关键字查询', validators=[Optional()])
    tag = SelectField('标签',validators=[Optional()], choices=choice)
    submit = SubmitField('搜')


@app.route('/', methods=['GET', 'POST'])
def index():
    # keyword = None
    # tag = None
    form = NameForm()
    if request.method == 'POST' and form.validate_on_submit():     
        tag = Tag.query.filter_by(id=int(form.tag.data)).first()
        result = []
        for a in tag.articles:
            if form.keyword.data in a.title:
                result.append(a)

        session['keyword'] = form.keyword.data
        session['tag'] = form.tag.data
        session['result'] = result

        form.keyword.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, \
        keyword=session.get('keyword'), \
        tag=session.get('tag'), \
        # result = session.get('result') 
        )

