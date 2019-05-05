from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from ..models import Tag

 

class QueryForm(FlaskForm):
    # tags = Tag.query.all()
    # choice = [] #(data,displayname)
    # for t in tags:
    #     choice.append((str(t.id),t.name))

    # choice = [('1','t'),('2','g')]
    def __init__(self,choice):
        self.keyword = StringField('请输入关键字查询', validators=[Optional()])
        self.tag = SelectField('标签',validators=[Optional()], choices=choice)
        submit = SubmitField('搜')
