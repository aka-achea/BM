
def test():
    # test case
    db = NoteDataBase(dbfile)
    for x in ['t1','t2','t3']:
        db.insert_tag(x)
    for s in ['wx','mm']:
        db.insert_src(s)
    for u in [('u1@h.com','u1'),('u2@h.com','u2')]:
        db.insert_user(email=u[0],username=u[1])

    t = db.session.query(Tag).all()
    print(t)
    u = db.session.query(User).all()
    print(u)
    s = db.session.query(Source).all()
    print(s)

    a1 = {'timestamp':func.now(),'title':'testtitle','tag':'t1','user':'u2','link':'aaaaa','source':'mm'}
    db.insert_article(a1)
    a = db.query_userarticle_bytitle('u2','test')
    print(a)

    for x in a:
        print(x.link)