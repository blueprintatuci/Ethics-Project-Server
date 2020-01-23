# connecting to pg db
import os
import psycopg2

DATABASE_URL = "postgres://rdrhinxhcqfrkm:989d6c91e8eb163284de44343083d0c4928b4d539e493bb8dffbe16ce29e994d@ec2-52-203-98-126.compute-1.amazonaws.com:5432/d8u52i7luh8cuv?sslmode=require"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute("select * from blog_post;")
print(cur.fetchone())