from flask import  Flask, render_template, request


app = Flask(__name__)
app.config['DEBUG'] =True

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/index.html')
def home():
    return render_template('index.html', title='Home')

@app.route('/blog.html')
def blog():
    return render_template('blog.html', title="Blog")

if (__name__) == '__main__':
    app.run()
