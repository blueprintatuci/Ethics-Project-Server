from flask import Flask
import psycopg2
app = Flask(__name__)
DATABASE_URL = "postgres://rdrhinxhcqfrkm:989d6c91e8eb163284de44343083d0c4928b4d539e493bb8dffbe16ce29e994d@ec2-52-203-98-126.compute-1.amazonaws.com:5432/d8u52i7luh8cuv?sslmode=require"

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/blog_posts')
def fetch_blog_posts():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("select * from blog_post;")
    print(cur.fetchone())
    return str(cur.fetchone())


if __name__ == '__main__':
    app.run()