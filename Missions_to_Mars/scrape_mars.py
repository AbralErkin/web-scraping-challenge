# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def scrape_mars():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    scrape_results = {}

    # URL of newspage to be scraped
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup_news = BeautifulSoup(html, 'html.parser')
    #Collect the latest News Title
    news_title = soup_news.find_all('div', class_="content_title")
    link = news_title[1].find('a')
    scrape_results["news_title"] = link.text.strip()
    news_p = soup_news.find_all('div', class_="article_teaser_body")
    while  news_p  == []:
        html = browser.html
        soup_news = BeautifulSoup(html, 'html.parser')
        news_title = soup_news.find_all('div', class_="content_title")
        link = news_title[1].find('a')
        scrape_results["news_title"] = link.text.strip()
        news_p = soup_news.find_all('div', class_="article_teaser_body")
    scrape_results["news_p"] = news_p[0].text.strip()
    # URL of image page to be scraped
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup_image = BeautifulSoup(html, 'html.parser')
    image_title = soup_image.find_all('figure', class_="lede")
    link = image_title[0].find('a')['href']
    scrape_results["featured_image_url"] = 'https://www.jpl.nasa.gov'+link
    # URL of weather page to be scraped
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html = browser.html
    soup_weather = BeautifulSoup(html, 'html.parser')
    weather = soup_weather.find_all('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    while weather == []:
        html = browser.html
        soup_weather = BeautifulSoup(html, 'html.parser')
        weather = soup_weather.find_all('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    scrape_results["mars_weather"] = weather[0].find('span').text.strip()
    # URL of Mars facts page to be scraped
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts = tables[0]
    mars_facts.columns = ['Description','Value']
    mars_facts.reset_index(drop = True,inplace=True)
    scrape_results["scrapmars_facts_html"] = mars_facts.to_html()

    #url of the webpage to be scraped
    url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemis)
    #get the html of the main page
    html = browser.html
    soup_hemis = BeautifulSoup(html, 'html.parser')
    
    #find the each hemisphere names
    hemis = soup_hemis.find_all('div',class_='description')
    #hemisphere_image_urls = []
    i=1
    for names in hemis:
        browser.visit(url_hemis)
        browser.click_link_by_partial_text(names.find('a').text.strip())
        html = browser.html  
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find_all('img',class_='wide-image')
        scrape_results["hemisphere_tile"+str(i)] = names.find('a').text.strip()
        scrape_results["hemisphere_url"+str(i)] = "https://astrogeology.usgs.gov"+temp[0]['src']
        i+=1
        #hemisphere_image_urls.append({"title":names.find('a').text.strip(),"img_url":"https://astrogeology.usgs.gov"+temp[0]['src']})

   # scrape_results["hemisphere_image_urls"] = hemisphere_image_urls

    return scrape_results

if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    print(scrape_mars()) 
