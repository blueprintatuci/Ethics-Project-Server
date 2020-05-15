from bs4 import BeautifulSoup
import requests
from scrapers.utils import * 

## for treehugger.com
## does not include featured article, can include all articles once duplicate catcher is in place?

def scrape_treehugger(table_article):
    '''
    Input: table_article is a dict of the most recent published article from treehugger 
            that was inserted into the articles table
    Scrapes content from treehugger; if a duplicate article is detected, script will terminate and return output
    Output: list of dicts representing articles
    '''
    l = []
    
    base_url = 'https://www.treehugger.com/' 
    print(base_url)

    # Request URL and Beautiful Parser
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    latest_stories = soup.find_all('article', class_="c-article c-article--card")

    for item in latest_stories:
        d = { }
        dup_flag = False
        
        ## url
        url = item.find("div", class_ = "c-article__image").find("a")
        d['url'] = 'https://www.treehugger.com' + url['href']

        ## title
        title = item.find("div", class_="c-article__summary").find("a").get_text().strip('\n')
        d['title'] = title

        ## author
        author = item.find("div", class_='c-article__summary').find("div", class_='c-article__byline').find('a').get_text()
        d['author'] = author

        ## image_url
        image_url = item.find("div", class_ = "c-article__image").find("img")
        d['image_url'] = image_url['src']

        ## publish_date
        publish_date = item.find("div", class_="c-article__byline").find('a', class_="c-article__published").get_text()
        d['publish_date'] = date_convert(publish_date)

        ## site name
        d['site_title'] = 'treehugger'

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
                'site_title' : 'treehugger',
            }
    th = scrape_treehugger(test_article)
    print('Number of new articles: ', len(th))
    print (th)
    