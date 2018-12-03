import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': r'C:/Users/dshaf/Documents/School/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def nasa():
    browser = init_browser()
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news = {}
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    news["title"] = news_title
    news["paragraph"] = news_p
    return news

def nasa_image():
    browser = init_browser()
    nasaurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasaurl)
    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = {}
    image = soup.find('article', class_='carousel_item')
    the_url = 'https://www.jpl.nasa.gov' + image.find('a', class_="button fancybox")['data-fancybox-href']
    featured_image_url["url"] = the_url
    return featured_image_url

def mars_weather():
    browser = init_browser()
    mars_twit = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twit)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_tweet = {}
    tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_tweet["weather"] = tweet

    return mars_tweet


def facts():
    browser = init_browser()
    mars_facts = 'https://space-facts.com/mars/'
    browser.visit(mars_facts)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_dict = {}
    tab = soup.find_all('table')[0]
    df = pd.read_html(str(tab))
    df = df[0]
    df.columns = ['Attribute', 'Measurement']
    df.set_index('Attribute', inplace=True)
    mars_dict = df.to_html()
    return mars_dict
facts()

def hemisphere():
    browser = init_browser()
    hems = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hems)
    html = browser.html
    soup = bs(html, 'html.parser')

    hem_links = soup.find_all('div', class_='description')
    hems_image_urls = []
    for link in hem_links:
        suburl = 'https://astrogeology.usgs.gov' + link.find('a')['href']
        browser.visit(suburl)
        response = requests.get(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = link.find('a').text
        subresult = soup.find('div', class_='downloads')
        image_url = subresult.find('a')['href']
        hems_image_urls.append({"title": title, "image_url": image_url})
    return hems_image_urls

def scrape():
    browser = init_browser()
    data = {}
    data["nasa"] = nasa()
    data["nasa_image"] = nasa_image()
    data["weather"] = mars_weather()
    data["facts"] = facts()
    data["hemisphere"]= hemisphere()
    return data
