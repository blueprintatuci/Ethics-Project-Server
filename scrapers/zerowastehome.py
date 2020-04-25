from bs4 import BeautifulSoup
import requests

## for zerowastehome.com
 
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


def scrape_zerowastehome():
    '''
    Scrapes content from zerowastehome
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

        l.append(d)

    return l


if __name__ == "__main__":
    print(scrape_zerowastehome())
    