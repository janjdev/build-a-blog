from flask import Flask, request, redirect, render_template, session, escape, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, DDL
from sqlalchemy.event import listen
from datetime import datetime
import pymysql
from slugify import slugify

app = Flask(__name__)
app.secret_key = b'1\x19\xca0\\\xe7\x84X\xb3\x03d/tR\x14\x88'
app.config["CACHE_TYPE"] = "null"
app.config['DEBUG'] =True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/lc1012019'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#Create function to get default values from other columns when needed
def same_as(column_name):
    def default_function(context):
        return context.get_current_parameters()[column_name]
    return default_function

def create_username(username):
    if username != '':
        return username
    else:
        return slugify(session.get('user').first_name +' ' + session.get('user').last_name)

def get_author_id(self):
    return session.get('user').id

def get_author(self):
    return session.get('user').first_name + ' ' + session.get('user').last_name

def get_publisher(self):
    return session.get('user').first_name + ' ' + session.get('user').last_name


class Blog_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(140), nullable=False)
    posts = db.relationship('Post', backref='blog_user', lazy=True)
  
    
    def __init__(self, email, password, first_name, last_name, username=''):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = create_username(username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('blog__user.id'), nullable=False)
    author = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    post_status = db.Column(db.String(10), nullable=False, default='draft')
    post_type = db.Column(db.String(100))
    slug = db.Column(db.String(255), nullable=False)
    published_post = db.relationship('Published_Post', backref='post', lazy=True)
    term_relationships = db.relationship('Term_Relationship', backref="post", lazy=True)


    def __init__(self, title, content):
        self.title = title 
        self.author_id = get_author_id()
        self.author = get_author()
        self.content = content
        self.slug = slugify(title)

    


class Published_Post(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),  primary_key=True, nullable=False)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    published_by = db.Column(db.String(255), nullable=False)

    def __init__(self):
        self.published_by = get_publisher()

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    taxonomy_of_term = db.relationship('Term_Taxonomy', backref='term_taxonomy', lazy=True)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)        

class Term_Taxonomy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taxonomy = db.Column(db.String(255), nullable=False)       
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'), nullable=False)
    terms_relationships = db.relationship('Term_Relationship', backref='terms_taxonomy_relationship', lazy=True)

    def __init__(self, taxonomy, term_id):
        self.taxonomy = taxonomy
        self.term_id = term_id

class Term_Relationship(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True, nullable=False)
    term_taxonomy_id = db.Column(db.Integer, db.ForeignKey('term__taxonomy.id'), primary_key=True, nullable=False)
    
    def __init__(self, post_id, term_taxonomy_id):
        self.post_id = post_id
        self.term_taxonomy_id = term_taxonomy_id

event.listen(Term.__table__, 'after_create', DDL(""" INSERT INTO term (id, name, slug) VALUE (1, 'Blog Post', 'blog-post'), (2, 'Event Post', 'event-post'), (3, 'Page', 'page'), (4, 'Post Tag', 'post-tag') """))
event.listen(Term_Taxonomy.__table__, 'after_create', DDL(""" INSERT INTO term__taxonomy (id, taxonomy, term_id)  VALUE (1, 'category', 1), (2, 'category', 2), (3, 'category', 3), (4, 'tag', 4) """))

# @app.before_first_request
# def setup():
#     post = Term('Blog Post')
#     tag = Term('Post Tag')
#     page = Term('Page')
#     event = Term('Event Post')
#     db.session.add(post)
#     db.session.add(tag)
#     db.session.add(page)
#     db.session.add(event)
#     db.session.flush()
#     postTax = Term_Taxonomy('category', post.id)
#     tagTax = Term_Taxonomy('tag', tag.id)
#     pagTax = Term_Taxonomy('category', page.id)
#     eventTax = Term_Taxonomy('category', event.id)
#     db.session.add(postTax)
#     db.session.add(tagTax)
#     db.session.add(pagTax)
#     db.session.add(eventTax)
#     db.session.flush()
#     db.session.commit()

@app.route('/')
def index():
    # terms = db.session.query(Term.name).all()
    # html = '<ul>'
    # for t in terms:
    #     html += '<li>' +str(t) + '</li>'
    # html += '</ul>'
    return render_template('index.html')

if (__name__) == '__main__':
    # db.create_all()
    app.run()
