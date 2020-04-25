from bs4 import BeautifulSoup
import requests

## for treehugger.com
## does not include featured article, can include all articles once duplicate catcher is in place?
 
months = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December' :12
}

def date_convert(string):
    date = string.split()
    mon = months[date[0]]
    day = date[1].strip(',')
    year = date[2]
    return "{}/{}/{}".format(mon, day, year)


def scrape_treehugger():
    l = []
    
    base_url = 'https://www.treehugger.com/' 
    print(base_url)

    # Request URL and Beautiful Parser
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    latest_stories = soup.find_all('article', class_="c-article c-article--card")

    for item in latest_stories:
        d = { }

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

        l.append(d)

    return l


if __name__ == "__main__":
    print(treehugger())
    