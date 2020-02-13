from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import requests

from api_url import API

app = Flask(__name__)
CORS(app)
DATABASE_URL = "postgres://rdrhinxhcqfrkm:989d6c91e8eb163284de44343083d0c4928b4d539e493bb8dffbe16ce29e994d@ec2-52-203-98-126.compute-1.amazonaws.com:5432/d8u52i7luh8cuv?sslmode=require"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Did not provide valid POST body"}), 400

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/articles')
def fetch_articles():
    """
    GET request
    Returns all articles in our database
    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("select * from articles;")
    articles = cur.fetchall()
    col_names = []
    for col in cur.description:
        col_names.append(col[0])
    
    json_articles = []

    for article in articles:
        json_article = dict()
        for i in range(len(col_names)):
            json_article[col_names[i]] = article[i]
        json_articles.append(json_article)
    
    cur.close()
    conn.close()

    return jsonify({"articles": json_articles}), 200

@app.route('/add_article', methods=['POST'])
def add_article():
    """
    POST request
    Adds a single article to our database
    POST body params:
        url - link to the article (str)
        title - title of the article (str)
        author - name of the author (str)
        content - excerpt or content of the article (str)
        date - date that the article was published (str in MM/DD/YYYY format)
    times_used will be filled on this server's end (initial value: 0)
    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify({"error": "Did not provide POST body"}), 400
    query = "INSERT INTO articles (url, title, author, image_url, content, publish_date, times_used) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    values = (data["url"], data["title"], data["author"], data["image_url"], data["content"], data["publish_date"], "0")
    cur.execute(query, values)
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"inserted": "success"}), 200

@app.route("/shopify/articles", methods=['POST'])
def post_articles():
    """
    POST request
    Posts a single article to Shopify blog
    POST body params:
        json - contains all data
            id - id of article in database (int)
    """
    blog_id = "54254043195" # should be a parameter in future

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    get_stmt = ("SELECT url, title, author, image_url FROM articles "
                "WHERE id = (%s)")
    cur.execute(get_stmt,(request.json['json']['id'],))
    data = cur.fetchall()

    if not data: # if id not found
        abort(404)
    
    img_src = {"src":data[0][3]}
    json = {'title':data[0][1],'body_html':'URL:'+ data[0][0],'author':data[0][2],'image':img_src}
    r = requests.post(API.ARTICLE_URL(API.ADMIN_URL,blog_id),json={'article':json})
    curr.close()
    conn.close()

    if r.status_code == 201:
        return r.json(), r.status_code
    else:
        return jsonify({"Message":r.text}), r.status_code

if __name__ == '__main__':
    app.run()



