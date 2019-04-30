from flask import Flask, request, redirect, render_template, session, escape, url_for, flash, jsonify, json
from flask_sqlalchemy import SQLAlchemy, Pagination
from sqlalchemy import event, DDL, extract
from sqlalchemy.event import listen
from datetime import datetime
import os, pymysql, jsonpickle, io, collections, calendar
from hashutils import make_pw_hash, check_pw_hash
from slugify import slugify
from mimetypes import MimeTypes
from werkzeug.utils import secure_filename
from collections import defaultdict
#from urllib import request



app = Flask(__name__)
app.secret_key = b'1\x19\xca0\\\xe7\x84X\xb3\x03d/tR\x14\x88'
app.config["CACHE_TYPE"] = "null"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/lc1012019'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SITE_UPLOADS'] = 'D:/Courses/Development/Programming/Python/LaunchCode/LC101/unit2/build-a-blog/static/site/uploads/'
app.config['ADMIN_UPLOADS'] = 'D:/Courses/Development/Programming/Python/LaunchCode/LC101/unit2/build-a-blog/static/admin/uploads/'    
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'SVG', 'GIF']
app.config['DATA_FILES'] = 'D:/Courses/Development/Programming/Python/LaunchCode/LC101/unit2/build-a-blog/data/'
app.config['RELATIVE_PATH_SITE'] = '../static/site/uploads/'
app.config['RELATIVE_PATH_ADMIN'] = '/static/admin/uploads/'
db = SQLAlchemy(app)

#Create function to get default values from other columns when needed
def same_as(column_name):
    def default_function(context):
        return context.get_current_parameters()[column_name]
    return default_function

#Helper Functions
def allowed_image(mime):
    if mime not in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return False    

def create_username(username, first_name, last_name):
    if username != '':
        return username
    else:
        return slugify(first_name + last_name)

def get_author_id():
    return session.get('user')['id']

def get_author():
    return session.get('user')['first_name'] + ' ' + session.get('user')['last_name']

def get_publisher():
    return session.get('user')['first_name'] + ' ' + session.get('user')['last_name']

def get_uploads():
    list_images = os.listdir(app.config['ADMIN_UPLOADS'])
    images = []
    i =0
    length = len(list_images)
    while i < length:
        img = {}
        img['name'] = list_images[i]
        img['url'] = os.path.join(app.config['RELATIVE_PATH_ADMIN'], list_images[i])
        images.append(img)
        i+=1 
    return images

def get_archive():
    p = db.session.query(Published_Post.published_date).all()
    d = defaultdict(list)
    for i in p:
         d[i.published_date.year].append(i.published_date.month)
    # create dict for archives convert month numbers to names
    adict = {}
    for k  in d:
        adict['year'] = k
        adict['months'] = list(dict.fromkeys(d.get(k)))
    for m in range( len(adict['months'])):
        adict['months'][m] = calendar.month_name[adict['months'][m]]
        
    return adict

def get_tags():
    tax = Term_Taxonomy.query.filter_by(taxonomy='tag').all()
    tags=[]
    for t in tax:
        term = Term.query.filter_by(id=t.term_id).first()
        tags.append(term.slug)
    return tags

def get_mime_type(media):
#get media file from the form input
    url = urllib.pathname2url('media[0]')
    return MimeTypes.guess_type(url)
    

#Get Json File
def getJSON(file):
    with io.open(file, 'r', encoding='utf-8', errors='ignore') as fp:
        return json.load(fp, strict=False)


def recent_posts():
    fp = Post.query.order_by(Post.date_created.desc()).limit(3).all()
    footerPosts =[]
    for p in fp:
        post = {}
        if Post_Meta.query.filter_by(post_id=p.id).all():
           post['meta'] = Post_Meta.query.filter((Post_Meta.post_id==p.id) & (Post_Meta.meta_key=='attachment')).first().meta_value
        post['post'] = p
        footerPosts.append(post)
    return footerPosts

def get_post_and_postmeta(result):
    post = []
    for p in result:
        postmeta = {}
        if Post_Meta.query.filter_by(post_id=p.id).all():
           postmeta['meta'] = Post_Meta.query.filter_by(post_id=p.id).all()
        postmeta['author'] = Blog_User.query.filter_by(id=p.author_id).first()
        postmeta['post'] = p
        post.append(postmeta)
    return post

#===================================================================================================================================#
#===================================================================================================================================#

class Blog_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='blog_user', lazy=True)
    role = db.relationship('UserRoles', backref='user_roles')
  
    def __init__(self, email, password, first_name, last_name, username):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = make_pw_hash(password)
        self.username = create_username(username, first_name, last_name)

class User_Meta(db.Model):
    __tablename__ = 'usermeta'
    meta_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('blog__user.id', ondelete='CASCADE'))
    meta_key = db.Column(db.String(50), unique=True, nullable=False)
    meta_value = db.Column(db.Text, nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('blog__user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog__user.id', ondelete='CASCADE'))
    login = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id):
        self.user_id = self.user_id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('blog__user.id',  ondelete='CASCADE'), nullable=False,)
    content = db.Column(db.Text, nullable=False)
    post_status = db.Column(db.String(10), nullable=False, default='draft')
    post_type = db.Column(db.String(100))
    post_mime_type = db.Column(db.String(100))
    slug = db.Column(db.String(255), nullable=False)
    post_parent = db.Column(db.Integer, default=0, nullable=False)
    published_post = db.relationship('Published_Post', backref='published_posts', lazy=True)
    term_relationships = db.relationship('Term_Relationship', backref="post_terms", lazy=True)
    post_meta = db.relationship('Post_Meta', backref='postmeta', lazy=True)


    def __init__(self, title, content, post_type, post_mime_type=''):
        self.title = title 
        self.author_id = get_author_id()
        self.content = content
        self.post_type = post_type
        self.post_mime_type = post_mime_type
        self.slug = slugify(title)

    
class Published_Post(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'),  primary_key=True, nullable=False)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    published_by = db.Column(db.String(255), nullable=False)

    def __init__(self, post_id):
        self.post_id = post_id
        self.published_by = get_publisher()

class Post_Meta(db.Model):
    __tablename__ = 'postmeta'
    meta_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    meta_key = db.Column(db.String(255),  nullable=False)
    meta_value = db.Column(db.Text, nullable=False)

    def __init__(self, post_id, meta_key, meta_value):
        self.post_id = post_id
        self.meta_key = meta_key
        self.meta_value = meta_value
        

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
    term_id = db.Column(db.Integer, db.ForeignKey('term.id',  ondelete='CASCADE'), nullable=False)
    terms_relationships = db.relationship('Term_Relationship', backref='terms_taxonomy_relationship', lazy=True)

    def __init__(self, taxonomy, term_id):
        self.taxonomy = taxonomy
        self.term_id = term_id

class Term_Relationship(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True, nullable=False)
    term_taxonomy_id = db.Column(db.Integer, db.ForeignKey('term__taxonomy.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    
    def __init__(self, post_id, term_taxonomy_id):
        self.post_id = post_id
        self.term_taxonomy_id = term_taxonomy_id

event.listen(Term.__table__, 'after_create', DDL(""" INSERT INTO term (id, name, slug) VALUE (1, 'Blog', 'blog'), (2, 'Event', 'event'), (3, 'Page', 'page'), (4, 'Post Tag', 'post-tag'), (5, 'Attachment', 'attachment'), (6, 'Slide', 'slide') """))
event.listen(Term_Taxonomy.__table__, 'after_create', DDL(""" INSERT INTO term__taxonomy (id, taxonomy, term_id)  VALUE (1, 'category', 1), (2, 'category', 2), (3, 'category', 3), (4, 'tag', 4), (5, 'category', 5), (6, 'category', 6) """))
event.listen(Role.__table__, 'after_create', DDL(""" INSERT INTO roles (id, name)  VALUE (1, 'admin'), (2, 'editior'), (3, 'author') """))




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

# @app.context_processor 
# def get_feeds():
#     if request.method == 'POST':
#         if request.json:
#             feed = request.json
#             return dict('feed', feed  )
#     return None


# home page first 13 posts
@app.route('/')
def home():
    tags = get_tags()    

    results = Post.query.limit(13).all()
    post = get_post_and_postmeta(results)
     #[]
    # for p in posts:
    #     postmeta = {}
    #     if Post_Meta.query.filter_by(post_id=p.id).all():
    #        postmeta['meta'] = Post_Meta.query.filter_by(post_id=p.id).all()
    #     postmeta['author'] = Blog_User.query.filter_by(id=p.author_id).first()
    #     postmeta['post'] = p
    #     post.append(postmeta)
    return render_template('site/pages/index.html', title='Home', post=post, footerPosts=recent_posts(), archive=get_archive(), tags=tags)

#Page by number

@app.route('/<int:page_num>')
def homeAll(page_num):
    posts = Post.query().all().paginate(per_page=13, page=page_num, error_out=True)
    postmeta = []
    for post in posts:
        img_url = Post_Meta.query.filter((Post_Meta.post_id == post.id) & (Post_Meta.meta_key == 'post_attachment')).first().meta_value
        author_name = Blog_User.query.filter_by(id == post.author_id).first().first_name
        author_name += ' ' +Blog_User.query.filter_by(id == post.author_id).first().last_name
        postmeta.append({post.id: [img_url, author_name]})
    return render_template('site/pages/index.html', title='Home', posts=posts, postmeta=postmeta, archive=get_archive())

#post of all types 

@app.route('/posts')
def posts():
    posts = Post.query().all().paginate(per_page=13, page=1)
    return render_template('site/pages/blog.html', title="Blog", posts=posts, archive=get_archive())

#post by type

@app.route('/posts/<type>', methods=['GET'])
def posts_type(type):
    posts = Post.query.filter_by(post_type=type).all()
    return render_template('site/pages/blog.html', title=type.upper(), posts=posts, archive=get_archive())

#single post page by post id

@app.route('/post/<int:post_id>')
def post(post_id):    
    result = []
    result.append(Post.query.filter_by(id=post_id).first())
    post = get_post_and_postmeta(result)

    return render_template('site/pages/single.html', post=post, archive=get_archive(), footerPosts=recent_posts(), tags=get_tags())

@app.route('/archives/<int:month>')
def archives_byMonth(month):
    l = Published_Post.query.filter(extract('month', Published_Post.published_date) == month).all()
    return render_template('site/archives', l=l, title='Archives')



#=============================================Auth Routes=====================================================
@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('authenticated'):
        return jsonify({'status': 'success', 'message': 'You\'re already registered. Please, log out to change users.', 'alertType': 'info', 'callback': 'goToAdmin', 'timer': 4500})
    else:
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            username = request.form['username']
            email = request.form['email']
            conemail = request.form['confirm-email']
            passwrd = request.form['pass']
            conpass = request.form['confirm-pass']
            if email == conemail:
                current_user = Blog_User.query.filter_by(email=email).first()
                if current_user:
                    return jsonify({'status': 'error', 'message': 'A user with this email already exist. Please, sign in.', 'alertType': 'error', 'callback': 'goToAdmin', 'timer': 3000})
                elif passwrd == conpass:
                    new_user = Blog_User(first_name=fname, last_name=lname, username=username, email=email, password=passwrd)
                    db.session.add(new_user)
                    db.session.commit()
                    session['authenticated'] = True
                    session['id'] = new_user.id
                    return jsonify({'status': 'success', 'message': 'You\'re in!', 'alertType': 'success', 'callback': 'goToAdmin', 'timer': 2000})
                else:
                    return jsonify({'status': 'error', 'message': 'passwords do not match', 'alertType': 'error', 'callback': 'clearPassFields', 'timer': 3500})
            else:
                return jsonify({'status': 'error', 'message': 'emails do not match', 'alertType': 'error', 'callback': 'clearEmailFields', 'timer': 3500})
    return render_template('admin/auth/pages/register.html', reg_link="/register", log_link="/login", lock_link="/lock", reg_active='active', filter_color = 'rose')

#=========================Login===============================================================================
@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'authenticated' in session:
        redirect(url_for('admin'))
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if email != "" and password !="":
                user = Blog_User.query.filter_by(email=email).first()
                if user:
                    if check_pw_hash(password, user.password):
                        session['authenticated'] = True
                        session['id'] = user.id
                        return jsonify({'message': 'Hello ' + user.first_name, 'alertType': 'success', 'callback': 'goToAdmin', 'timer': 2000})
                    else: 
                        return jsonify({'callback': 'clearPassFields', 'message': 'Invalid email or password', 'alertType': 'error', 'timer': 5000 })
                else:
                    return jsonify({'callback': 'goToRegister', 'message': 'That user does not exist. Please, register.', 'alertType': 'error', 'timer': 3500 })
            else:
                return jsonify({'callback': '', 'message': 'Email and password are required.', 'alertType': 'error', 'timer': 2500})
    filterColor = 'rose' 
    return render_template('admin/auth/pages/login.html', reg_link="/register", log_link="/login", lock_link="/lock", log_active='active', filter_color = filterColor)

#=======================================Lock================================================================================
@app.route("/lock", methods=['POST', 'GET'])
def lock():
    if request.method == 'POST':
        password = request.form['password']
        if 'id' in session:
            if check_pw_hash(password, session.get('user')['password']):
                session['authenticated'] = True
                session.pop('locked', None)
                return jsonify({'message': 'Welcome back, ' + session.get('user')['first_name'], 'callback': 'unlock', 'param': session.get('current_url'), 'alertType': 'success', 'timer': 3500})
            else:
                return '', 204
                #jsonify({'message': 'Invalid user or password.', 'alertType': 'error', 'callback': 'noMatch', 'param': 'form'})
        else:
            return jsonify({'message': 'Your session has expired. Please, login.', 'callback': 'goToLogin', 'alertType': 'info', 'timer': 3500})
    session.pop('authenticated', None)
    session['locked'] = True
    return render_template("admin/auth/pages/lock.html", lock_active='active', user=session.get('user'), avatar=session.get('avatar'))

#=====================================Log Out==============================================================================
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('id', None)
    session.pop('authenticated', None)
    return redirect(url_for('login'))


#======================================================================================================================================================



#===========================================Dash Routes=======================================================================
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if 'authenticated' in session:
        auth_user = Blog_User.query.filter_by(id=session.get('id')).first()
        active_user = jsonpickle.encode(auth_user, unpicklable=False, max_depth=2)
        user = jsonpickle.decode( active_user)
        session['user'] = user
        name = session.get('user')['first_name'] + ' ' + session.get('user')['last_name']
        images = get_uploads()
        feed = getJSON('D:/Courses/Development/Programming/Python/LaunchCode/LC101/unit2/build-a-blog/data/data1.json').get('items',[])
        session['current_url'] = request.url
        
        array = Post.query.order_by(Post.date_created.desc()).limit(3).all()
        hposts = []
        for i in array:
            hposts.append(Post.query.filter_by(id=i.id).first()) 
        posts = []
        for p in hposts:
            post = {}
            id = p.author_id
            author = Blog_User.query.filter_by(id=id).first()
            pubDate = Published_Post.query.filter_by(post_id=p.id).first().published_date
            img = Post_Meta.query.filter((Post_Meta.post_id == p.id) & (Post_Meta.meta_key == 'attachment')).first().meta_value
            post['post'] = p
            post['author'] = author
            post['pubdate'] = pubDate
            post['img'] = img
            posts.append(post)
        
        postCount = len(Post.query.all())
        pageCount = len(Post.query.filter_by(post_type='page').all())
        catCount = len(Term_Taxonomy.query.filter_by(taxonomy='category').all())
        tagCount = len(Term_Taxonomy.query.filter_by(taxonomy='tag').all())
        counts = {'post':postCount, 'page': pageCount, 'cat': catCount, 'tag': tagCount}
        return render_template('admin/dash/pages/dash.html', user=user, id=session.get('user')['id'], name=name, pagename='Dashboard', feed=feed, avatar=session.get('avatar'), dash_active="active", images=images, posts=posts, counts=counts)
    return redirect(url_for('login'))

#=================Dashboard Actions========================================================================

#Add Media to Library
@app.route('/admin/quickAdd', methods=['POST', 'GET'])
def quickAdd():
    if request.method == 'POST':
        if request.files:
            media  = request.files['attachment']
            if media.filename == '':
                return jsonify({'message': 'Your file must have a name.', 'alertType': 'error', 'callback': '', 'timer': 2500})
            filename = secure_filename(media.filename)
            media.save(os.path.join(app.config['ADMIN_UPLOADS'], filename))
            return jsonify({'message': 'OK', 'alertType': 'success', 'timer': 2000, 'callback': 'reset', 'param': 'form'})
    return redirect(url_for('admin'))


#View Created Posts By Type
@app.route('/admin/posts/<postType>')
def view_posts(postType):
    if 'authenticated' in session:
        if 'user' in session:
            session['current_url'] = request.url
            posts = []
            theposts = Post.query.filter_by(post_type=postType).all()
            for p in theposts:
                post = {}
                id = p.author_id
                author = Blog_User.query.filter_by(id=id).first()
                post['post'] = p
                post['author'] = author                
                posts.append(post)
            return render_template('admin/dash/pages/posts.html', user=session.get('user'), pagename='Posts', tablename="Blog Posts", parent_post='active', avatar=session.get('avatar'), post_active='active', posts=posts), print(posts)

#Create a new post
@app.route('/admin/posts/blog/add_post', methods=['POST', 'GET'])
def add_posts():
    if 'authenticated' in session:
        if 'user' in session:
            session['current_url'] = request.url
            images = get_uploads()
            cats = Term_Taxonomy.query.filter_by(taxonomy='category').all()
            cat_ids = []
            for cat in cats:
                cat_ids.append(cat.term_id)
            categories = [] 
            for id in cat_ids:
                term = Term.query.filter_by(id=id).first().name
                categories.append(term)
            if request.method == 'POST' :
                title = request.form['title']
                content = request.form['content']
                post_type = 'Blog'
                newPost = Post(title, content, post_type)
                db.session.add(newPost)
                db.session.commit()
                id = newPost.id
                return redirect(url_for('single_post', post_id = id))
            return render_template('admin/dash/pages/post-edit.html', user=session.get('user'), pagename='New Blog Post', parent_post='active', avatar=session.get('avatar'), post_active='active', images=images, categories=categories, bodyClass="page-post_edit")
    return redirect(url_for('login'))

#Publish a new post
@app.route('/admin/posts/blog/add_post/publish', methods=['POST', 'GET'])
def publish_post():
    if 'authenticated' in session:
        if 'user' in session:
            if request.method == 'POST':
            # create the new post
                title = request.form['title']
                content = request.form['content']
                if 'postType' in request.args:
                    post_type = request.form['postType']    
                else:
                    post_type = 'Blog'
                newPost = Post(title, content, post_type)
                db.session.add(newPost)
                db.session.commit()
#================Get the new ID of post ===============================            
                new_id = newPost.id
#================Create the url to view post ==========================
                url = '/post/' + str(new_id)
#======================================================================

            # update the post_status    
                updatePost = Post.query.filter_by(id=new_id).first()
                updatePost.post_status = 'published'
            #Add Post to published_post table
                pubPost = Published_Post(new_id)
                db.session.add(pubPost)
                db.session.commit()

#=============================================================================            
            #update tags, categories, and postmeta data
#=============================================================================
                #Tags==============================
                if 'tags' in request.args:
                    tags = request.form['tags']
                    tags = tags.split(',')
                    for tag in tags:                        
                        t = Term.query.filter_by(slug=tag.lower()).first()

                        if t:
                            taxID = Term_Taxonomy.query.filter_by(term_id=t.id).first()
                            if taxID:
                                newRelation = Term_Relationship(new_id, taxID.id)
                                db.session.add(newRelation)
                                db.session.commit()
                                
                        else:
                            newTerm = Term(tag)
                            db.session.add(newTerm)
                            db.session.commit()
                        
                            newTax = Term_Taxonomy('tag', newTerm.id)
                            db.session.add(newTax)
                            db.session.commit()

                            newRelation = Term_Relationship(new_id, newTax.id)
                            db.session.add(newRelation)
                            db.session.commit()    

                #Categories==========================================================
                if 'category' in request.form:
                    categories = request.form['category']
                    categories = categories.split(',')
                    for category in categories:
                        catTerm = Term.query.filter_by(name=category).first()
                        if catTerm:
                            catTax = Term_Taxonomy.query.filter_by(term_id=catTerm.id).first()
                            if catTax:
                                newRelation = Term_Relationship(new_id, catTax.id)
                                db.session.add(newRelation)
                                db.session.commit()
                                        
                #Postmeta==============================================================
                if 'featureImg' in request.form:
                    attach = request.form['featureImg']
                    attachMeta = Post_Meta(new_id, 'attachment', attach)
                    db.session.add(attachMeta)
                if 'slider' in request.form:                    
                    slideMeta = Post_Meta(new_id, 'slider', True)
                    db.session.add(slideMeta)
                if post_type == 'Event':
                    event_date = request.form['eventDate']
                    eveMeta = Post_Meta(new_id, 'event_date', event_date)
                db.session.commit()
                return jsonify({'message': 'OK', 'alertType': 'success', 'timer': 2500, 'callback': 'openView', 'param': '/post/' + str(new_id) })

#=========================================================================================================================================================
#=========================================================================================================================================================

#View Profile
@app.route('/admin/profile/<int:user_id>', methods=['POST', 'GET'])
def profile(user_id):
    if 'authenticated' in session:
        if user_id == session.get('user')['id']:
            user = session.get('user')
            session['current_url'] = request.url
            return render_template('admin/dash/pages/user.html', user=user, pagename='User Profile', avatar=session.get('avatar'), profile_active="active")
    return redirect(url_for('login')) 

#Update Profile
@app.route('/updateProfile/<int:user_id>', methods=['POST', 'GET'])
def updateProfile(user_id):
    if request.method == 'POST':
        if 'authenticated' in session:
            if user_id == session.get('user')['id']:
                update = Blog_User.query.filter_by(id = user_id).first()
                # updatemeta = User_Meta.query.filter_by(user_id = user_id).first()
                
                #Get  and update username
                if request.form['username'] != '':
                    update.username = request.form['username']
                
                 #Get  and update email
                if request.form['email'] != '':
                    update.email = request.form['email']
                
                 #Get  and update first name
                if request.form['fname'] != '':
                    update.first_name = request.form['fname']
                    
                 #Get  and update last name
                if request.form['lname'] != '':
                    update.last_name = request.form['lname']

                #Get and update password
                if request.form['pass']:
                    pswd = request.form['pass']
                if request.form['confirm']:
                    confirm = request.form['confirm']
                if pswd == confirm:
                    newpass = make_pw_hash(confirm)
                update.password = newpass

                 #Get  and update user bio
                # if request.form['bio'] != '':
                #     updatemeta.user_bio = request.form['bio']
                 
                #if updatemeta:
                    #updatemeta.meta_vale = os.path.join(app.config['ADMIN_UPLOADS'], avatar.filename) where meta_key == avatar
                    #else: 
                        #User_meta.meta_key = avatar
                        #User_meta.meta_value == avatar.url
                        #session.add()  

                #commit updates to the database
                db.session.commit()
                #get updated user 
                updated = Blog_User.query.filter_by(id = user_id).first()
                active_user = jsonpickle.encode(updated, unpicklable=False, max_depth=2)
                user = jsonpickle.decode( active_user)
                session['user'] = user
                return jsonify({'message': 'OK', 'alertType': 'success', 'timer': 2000, 'callback': 'loadProfile'})
    return redirect(url_for('profile', user_id = user_id))
#===========================================================================================================================
#===========================================================================================================================

#Update user avatar
@app.route('/update_avatar/<int:user_id>', methods=['POST', 'GET'])
def update_avatar(user_id):
    if request.method == 'POST':
        if 'authenticated' in session:
            if user_id == session.get('user')['id']:
                # updatemeta = User_Meta.query.filter_by(user_id = user_id).first()
                    if request.files:
                        avatar  = request.files['attachment']
                        if avatar.filename == '':
                            return jsonify({'message': 'Image must have a name.', 'alertType': 'error', 'callback': '', 'timer': 2500})
                        filename = secure_filename(avatar.filename)
                        avatar.save(os.path.join(app.config['ADMIN_UPLOADS'], filename))
                        session['avatar'] = os.path.join(app.config['RELATIVE_PATH_ADMIN'], filename)
                        #if updatemeta:
                            #updatemeta.meta_vale = os.path.join(app.config['ADMIN_UPLOADS'], avatar.filename) where meta_key == avatar
                            #else: 
                                #User_meta.meta_key = avatar
                                #User_meta.meta_value == avatar.url
                                #session.add()
                        return jsonify({'message': 'OK', 'alertType': 'success', 'timer': 2000, 'callback': 'loadAvatar'})
    return redirect(url_for('profile', user_id = user_id))



if (__name__) == '__main__':
    #db.create_all()
    app.run()
