from flask import render_template, session, request, redirect, url_for, current_app, jsonify
from .. import db
from ..models import Tag
from . import main
from .forms import QueryForm
from flask_login import login_required,current_user

import json
from mylog import myfilelog,get_funcname
from config import logfile

@main.route('/', methods=['GET', 'POST'])
@login_required

def index():

    # ml = myfilelog(logfile,get_funcname()) 
    tags = Tag.query.all()
    choice = [] #(data,displayname)
    for t in tags:
        choice.append((str(t.id),t.name))
    # ml.debug(choice)
    form = QueryForm()
    form.tag.choices = choice

    if request.method == 'POST' and form.validate_on_submit():     
        tag = Tag.query.filter_by(id=int(form.tag.data)).first()
        result = []
        for a in tag.articles:
            if form.keyword.data in a.title:
                result.append(a.to_dict())

        j_result = json.dumps(result, indent=2)        
        # ml.debug(j_result)
        
        session['keyword'] = form.keyword.data
        session['tag'] = tag.name
        session['result'] = j_result

        form.keyword.data = ''
        return redirect(url_for('.index'))


    return render_template('index.html', form=form, 
        keyword=session.get('keyword'), 
        tag=session.get('tag'), 
        result = session.get('j_result') 
        )


@main.route('/secrete')
@login_required
def s():
    return 'login pls'