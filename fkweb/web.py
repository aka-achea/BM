

import os
from app import db, create_app
from app.models import Tag,Source,User,Article


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Tag=Tag, Source=Source, Article=Article)





