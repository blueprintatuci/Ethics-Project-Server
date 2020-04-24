from flask import Flask, request, jsonify, make_response
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
    Returns all articles in our database, sorted from most recent publish date
    to least recent
    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("select * from articles order by publish_date desc;")
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

@app.route('/blogs', methods=['GET'])
def get_blogs():
    """
    GET request
    gets all blogs from shopify and returns parsed json
    return json format --> {"store_name":id}
    """
    blogs_r = requests.get(API.BLOG_URL)
    if blogs_r.status_code != 200:
        return blogs_r.json(), blogs_r.status_code

    blogs_json = blogs_r.json()
    json = dict()
    for blog in blogs_json["blogs"]:
        json[blog["title"]] = blog["id"]

    return jsonify(json), 200


@app.route('/add_article', methods=['POST'])
def add_article():
    """
    POST request
    Adds a single article to our database
    POST body params:
        url - link to the article (str)
        title - title of the article (str)
        author - name of the author (str)
        image_url - (str)
        date - date that the article was published (str in MM/DD/YYYY format)
    times_used will be filled on this server's end (initial value: 0)
    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify({"error": "Did not provide POST body"}), 400
    query = "INSERT INTO articles (url, title, author, image_url, publish_date) VALUES(%s, %s, %s, %s, %s)"
    values = (data["url"], data["title"], data["author"], data["image_url"], data["publish_date"])
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
            article_id - id of article in database (int)
            blog_id - id of blog to post to (int)
            
    """
    blog_id = str(request.json['json']['blog_id'])

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    get_stmt = ("SELECT url, title, author, image_url, content FROM articles "
                "WHERE id = (%s)")
    values = (request.json['json']['article_id'],)
    cur.execute(get_stmt, values)
    data = cur.fetchall()

    if not data: # if id not found
        abort(404)
    
    if not data[0][4]:
        content = '\n\nURL: '+ data[0][0]
    else:
        content = data[0][4] + '\n\nURL: '+ data[0][0]
    json = {'title':data[0][1],
            'body_html':content,
            'author':data[0][2],
            'image':{'src':data[0][3]}}
    r = requests.post(API.ARTICLE_URL(API.ADMIN_URL,blog_id),json={'article':json})
    cur.close()
    conn.close()

    if r.status_code == 201:
        return r.json(), r.status_code
    else:
        return jsonify({"Message":r.text}), r.status_code

if __name__ == '__main__':
    app.run()



