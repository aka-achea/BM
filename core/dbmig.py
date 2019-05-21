
from notedb import NoteDataBase, User, Article, Tag, Source


taglist = [
    ('食','食物'),('玩','玩乐'),('旅','旅行'),('计','计算机'),
    ('史','历史'),('笑','笑话'),('地','地理'),('生','生活'),
    ('艺','艺术'),('健','健康'),('科','科学'),('经','经济'),
    ('文','文化'),('杂','杂谈'),('p','python'),('测','测试')
]

sourcelist = [
    ('wx','微信公众号'),('mn','MONO')
]

ulist = [
    ('CJYRB@hotmail.com','Jason','123')
]

def import_article_csv(csv,dbfile):
    db = NoteDataBase(dbfile)
    with open(csv,'r', encoding='utf-8') as f:
        contents = f.readlines()
        for line in contents:
            entry = line.split(',')
            adict = {
                'timestamp':entry[0],
                'title':entry[1],
                'tag':entry[2],
                'author':entry[3],
                'source':entry[4],
                'link':entry[5],
                'email':entry[6].split()[0].upper()
            }
            # print(adict)
            db.insert_article(adict)


def import_tag(taglist,dbfile):
    db = NoteDataBase(dbfile)
    for t in taglist:
        db.insert_tag(t[0],t[1])


def import_user(ulist,dbfile):
    db = NoteDataBase(dbfile)
    for u in ulist:
        db.insert_user(u[0].upper(),u[1].upper(),u[2])


def import_source(sourcelist,dbfile):
    db = NoteDataBase(dbfile)
    for s in sourcelist:
        db.insert_src(s[0],s[1])



if __name__ == "__main__":
    csv = r'M:\MyProject\BM\mig.csv'
    dbfile = r'M:\MyProject\BM\note-prd.sqlite'
    db = NoteDataBase(dbfile)
    # db.reset_db()

    # import_tag(taglist,dbfile)
    # import_source(sourcelist,dbfile)
    # import_user(ulist,dbfile)
    # import_article_csv(csv,dbfile)

    # db = DataBase(dbfile)
    # t = db.session.query(Tag).all()
    # print(t)
    # u = db.session.query(User).all()
    # print(u)
    ar = db.session.query(Article).all()
    for a in ar:
        print(a.timestamp,a.tag.fullname,a.title)

