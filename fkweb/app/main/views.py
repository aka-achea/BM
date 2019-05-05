from flask import render_template, session, request, redirect, url_for, current_app
from .. import db
from ..models import Tag
from . import main
from .forms import QueryForm
from flask_login import login_required

@main.route('/', methods=['GET', 'POST'])
def index():
    # keyword = None
    # tag = None

    tags = Tag.query.all()
    choice = [] #(data,displayname)
    for t in tags:
        choice.append((str(t.id),t.name))

    form = QueryForm(choice)
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
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, 
        keyword=session.get('keyword'), 
        tag=session.get('tag'), 
        # result = session.get('result') 
        )


@main.route('/secrete')
@login_required
def s():
    return 'login pls'