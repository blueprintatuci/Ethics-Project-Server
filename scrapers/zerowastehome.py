from bs4 import BeautifulSoup
import requests
from scrapers.utils import *

## for zerowastehome.com

def scrape_zerowastehome(table_article):
    '''
    Input: table_article is a dict of the most recent published article from zerowastehome 
            that was inserted into the articles table
    Scrapes content from zerowastehome; if a duplicate article is detected, script will terminate and return output
    Output: list of dicts representing articles
    '''
    l = []
    
    base_url = 'https://zerowastehome.com/blog/' 
    print(base_url)

    # Request URL and Beautiful Parser
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    blogposts = soup.find_all('div', class_="post-content")

    for item in blogposts:
        d = { }
        dup_flag = False

        ## url
        url = item.find("a", class_="entire-meta-link")
        d['url'] = url['href']

        ## title
        title = item.find("h3", class_="title").get_text()
        d['title'] = title.strip()

        ## author
        author = item.find("div", class_="text").find("a").get_text()
        d['author'] = author

        ## image_url
        image_url = item.find("span", class_='post-featured-img') 
        #image_url['style'] = ''background-image: url(https://s3-us-east-2.amazonaws.com/zerowaste-media/wp-content/uploads/20180803124650/2018-07-01-06.32.13-900x600.jpg);'
        d['image_url'] = image_url['style'].strip("background-image: url(").strip(");")

        ## publish_date
        publish_date = item.find("div", class_="text").find("span").get_text()
        d['publish_date'] = date_convert(publish_date)

        ## site name
        d['site_title'] = 'zerowastehome'

        #### dup check 
        if d['publish_date'] == table_article['publish_date'] or d['publish_date'] < table_article['publish_date']:
            dup_flag = True 
        dup_flag =  dup_flag and d['url'] == table_article['url']
        dup_flag =  dup_flag and d['title'] == table_article['title']

        if not dup_flag:
            l.append(d)
        else:
            break

    return l


if __name__ == "__main__":
    test_article = {
                'url': "",
                'title':"",
                'author':"",
                'image_url':"",
                'publish_date' : datetime.datetime(1,1,1),
                'site_title': 'zerowastehome',
            }
    zwh = scrape_zerowastehome(test_article)
    print('Number of new articles: ', len(zwh))
    print (zwh)
    