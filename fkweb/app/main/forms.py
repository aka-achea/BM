from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
# from ..models import Tag

 

class QueryForm(FlaskForm):
    keyword = StringField('请输入关键字', validators=[Optional()])
    tag = SelectField('标签',validators=[Optional()])
    submit = SubmitField('搜')
        
