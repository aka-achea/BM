from flask import render_template, session, request, redirect, url_for, current_app
from .. import db
from ..models import Tag, User, Article
from . import main
from .forms import QueryForm
from flask_login import login_required,current_user


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():

    # ml = myfilelog(logfile,get_funcname()) 
    tags = Tag.query.all()
    choice = [] #(data,displayname)
    for t in tags:
        choice.append((str(t.id),t.name))
    
    form = QueryForm()
    form.tag.choices = choice
    print(choice)
    if request.method == 'POST' and form.validate_on_submit():  
        print(current_user)

        
        # ua = Article.query.filter_by(user_id=current_user.id)
        # # tag = Tag.query.filter_by(id=int(form.tag.data)).first()
        # result = []
        # for a in ua:
        #     if a.tag.id == int(form.tag.data) and form.keyword.data in a.title:
        #         print(a)
        #         # result.append(a.title)
        #         result.append(a.to_json())
        # # j_result = json.dumps(result, indent=2)        
        # print(result)     
        # session['result'] = result

        ua = Article.query.filter_by(user_id=current_user.id)
        # ua = ua.filter_by(tag=)


        session['keyword'] = form.keyword.data
        session['tag'] = tag.name

        form.keyword.data = ''
        return redirect(url_for('.index'))


    return render_template('index.html', form=form, a=ua,
        keyword=session.get('keyword'), 
        tag=session.get('tag')
        # result = session.get('result') 
        )


@main.route('/secrete')
@login_required
def s():
    return 'login pls'