from bs4 import BeautifulSoup
import requests

## for treehugger.com
## does not include featured article

def scrape():
    l = []
    
       
    base_url = 'https://www.treehugger.com/' 
    print(base_url)

    # Request URL and Beautiful Parser
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    all_product = soup.find_all('article', class_="c-article c-article--card")
    print(len(all_product))

    for item in all_product:
        d = { }
        # item = item.find("div", class_="c-article__container")
        # 'url' : 'https://www.treehugger.com' + art.css('div.c-article__image a::attr(href)').get(),
        url = item.find("div", class_ = "c-article__image").find("a")
        d['url'] = 'https://www.treehugger.com' + url['href']

        # 'title' : art.css('div.c-article__summary a::text').get().strip(),
        title = item.find("div", class_="c-article__summary").find("a").get_text().strip('\n')
        d['title'] = title

        # 'author' : art.css('div.c-article__summary div.c-article__byline a::text').get(),
        author = item.find("div", class_='c-article__summary').find("div", class_='c-article__byline').find('a').get_text()
        d['author'] = author

        # 'image_url' : art.css('div.c-article__image img::attr(src)').get(),
        image_url = item.find("div", class_ = "c-article__image").find("img")
        d['image_url'] = image_url['src']

        # 'publish_date' : date_convert(art.css('div.c-article__byline span a::text')[-1].get()),
        publish_date = item.find("div", class_="c-article__byline").find('a', class_="c-article__published").get_text()
        d['publish_date'] = publish_date

        # 'source': self.name,


        l.append(d)

    return l


if __name__ == "__main__":
    print(scrape())