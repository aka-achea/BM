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
        session['keyword'] = form.keyword.data
        session['tagid'] = form.tag.data
        form.keyword.data = ''     
        return redirect(url_for('.index'))
        
    print(session.get('keyword'))  
    print(session.get('tagid'))
    tagid = session.get('tagid')
    keyword = session.get('keyword')
    fs = Article.query.filter_by(user_id=current_user.id,tag_id=int(tagid))
    if keyword != '':
        posts = fs.filter(Article.title.like(f'%{keyword}%')).all()
        print(posts)

    else:
        print('no keyword')
        posts = fs.all()
        print(posts)

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


        # ua = Article.query.filter_by(user_id=current_user.id).all()
        # print(ua)
        # ua = ua.filter_by(tag=)

 
    return render_template('index.html', form=form,posts=posts,
        keyword=session.get('keyword'),
        tag=session.get('tagid')
        # result = session.get('result') 
        )


@main.route('/secrete')
@login_required
def s():
    return 'login pls'