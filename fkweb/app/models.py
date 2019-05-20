
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from flask import jsonify

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


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(15), unique=True)
    password_hash = db.Column(db.String(128))
    # taglist = db.Column()


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<{self.name} : {self.email}>'


class Article(db.Model): # duo
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), index=True)
    title = db.Column(db.String(64), index=True)
    link = db.Column(db.String(1000), index=True)
    author = db.Column(db.String(20),index=True)
    tag_id = db.Column(db.String(20),db.ForeignKey('tags.id'),nullable=False)
    tag = db.relationship('Tag',backref='articles')
    src_id = db.Column(db.String(20),db.ForeignKey('sources.id'),nullable=False)
    src = db.relationship('Source',backref='articles')
    user_id = db.Column(db.String(20),db.ForeignKey('users.id'),nullable=False) 
    user = db.relationship('User',backref='articles')


    def to_json(self):
        d_article = {
            'title':self.title,
            'link':self.link,
            'author':self.author,
            'tag':self.tag.name,
            'source':self.src.name,
            'user':self.user.name
        }
        return jsonify(d_article)


    def __repr__(self):
        return f'<{self.title} : {self.tag.name} : {self.user.name} : {self.src.name}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))