# import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import requests
from splinter import Browser
from selenium import webdriver
import time
import pymongo

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
def scrape():
    
    title = nasa_mars_news(browser)
    paragraph = nasa_mars_news(browser)
    imagemars = jpl_mars_space_image(browser)
    marsweather = mars_weather_data(browser)
    marsfacts = mars_facts_table(browser)
    marshemi = mars_hemi_image_title(browser)

    # print (title,paragraph)
    # print (imagemars) 
    # print (marsweather)
    # print (marsfacts)
    # print (marshemi)
    mars = {
        "title":title,
        "paragraph":paragraph,
        "imagemars":imagemars,
        "marsweather":marsweather,
        "marsfacts":marsfacts,
        "marshemi":marshemi
    }
    
    return mars
    
def nasa_mars_news(browser):
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    news_string = browser.html
    soup = bs(news_string, 'html.parser')
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    return news_title,news_p


def jpl_mars_space_image(browser):
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    #click the button to get to the full image
    browser.click_link_by_id('full_image')
    time.sleep(2)
    # Create a Beautiful Soup object
    jpl_string = browser.html
    soup = bs(jpl_string, 'html.parser')
    image = soup.find('img', class_ = 'fancybox-image')['src']
    featured_image_url = "https://jpl.nasa.gov"+image
    return featured_image_url

def mars_weather_data(browser):
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    twitter_html = browser.html
    soup = bs(twitter_html, 'html.parser')
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return mars_weather

def mars_facts_table(browser):
    url4 = "https://space-facts.com/mars/"
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Description', 'Values']
    html_table = df.to_html()
    html_table
    return html_table

def mars_hemi_image_title(browser):
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    hemisphere_image_url = []
    clicks = browser.find_by_css('a.product-item h3')
    for i in range(len(clicks)):
        hemi_dict = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.find_link_by_text('Sample').first
        hemi_dict["img_url"]=element["href"]
        hemi_dict["title"]=browser.find_by_css("h2.title").text
        hemisphere_image_url.append(hemi_dict)
        browser.back()
    return hemisphere_image_url

