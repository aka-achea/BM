

from .. import db


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

