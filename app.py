from flask import Flask
from flask_cors import CORS
import psycopg2
app = Flask(__name__)
CORS(app)
DATABASE_URL = "postgres://rdrhinxhcqfrkm:989d6c91e8eb163284de44343083d0c4928b4d539e493bb8dffbe16ce29e994d@ec2-52-203-98-126.compute-1.amazonaws.com:5432/d8u52i7luh8cuv?sslmode=require"

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/blog_posts')
def fetch_blog_posts():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("select * from blog_post;")
    posts = cur.fetchall()
    return str(posts)

@app.route('/add_post')
def add_blog_post():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("select * from blog_post;")
    posts = cur.fetchall()
    return str(posts)

@app.route("/shopify/articles/", methods=['POST'])
def post_articles():
    # error handling
    # blog_id, data = 
    # r = requests.post(ARTICLE_URL(blog_id),json={'article':data})
    return "test"


if __name__ == '__main__':
    app.run()