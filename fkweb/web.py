from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500

a = [('史','history'),('food','食'),('geography','地')]

class NameForm(FlaskForm):
    keyword = StringField('请输入关键字查询', validators=[Optional()])
    tag = SelectField('标签', choices=a)
    submit = SubmitField('搜')


@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = None
    tag = None
    form = NameForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        form.keyword.data = ''
        tag = form.tag.data

    return render_template('index.html', form=form, keyword=keyword, tag=tag)

