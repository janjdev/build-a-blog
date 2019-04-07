from flask import Flask, request, redirect, render_template, session, escape, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql


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
        return context.current_parameters.get(column_name)
    return default_function

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_status = db.Column(db.String(10), nullable=False, default='draft')
    # categories = db.Column(db.String(100), db.ForeignKey('category.id'), nullable=True)
    # tags = db.Column(db.String(100), db.ForeignKey('tag.id'), nullable=True)

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
    
    class Published_Post(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
         published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
         published_by = db.Column(db.String(255), db.ForeignKey('post.author', default=same_as(post.author) nullable=False))

         def __init__(self):
             return
    
    class Terms(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        slug = db.Column(db.String(255), default='', nullable=False)

        def __init__(self):
            return

    class Term_Taxonomy(db.Model):
        term_taxonomy_id = db.Column(db.Integer, primary_key=True)
        term_id = db.Column(db.Integer, db.ForeignKey('terms.id', nullable=False))
        taxonomy = db.Column(db.String(255), db.ForeignKey('term.name', nullable=False))
        description = db.Column(db.String, nullable=True)

        def __init__(self):
            return
    
                  
    



@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/login')
def login():
    return render_template('index.html', title='Home')

@app.route('/register')
def register():
    return

@app.route('/logout')
def logout():
    return

@app.route('/blog.html')
def blog():
    return render_template('blog.html', title="Blog")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return

@app.route('/admin')
def admin():
    if 'user' in session:
        return
@app.route('admin/posts')
def make_posts():
    if 'user' in session:
        new_post=Post(title, author, content, date, categorey, tags, post_type)
        return

if (__name__) == '__main__':
    app.run()
