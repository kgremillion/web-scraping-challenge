import pandas as pd
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from splinter import Browser
import time


def init_browser():
    executable_path = {'executable_path': 'C:/Windows/System32/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser

def scrape():

    browser = init_browser()

    # insert URL into variable
    url = "https://mars.nasa.gov/news/"
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # call on the link
    browser.visit(url)
   
    time.sleep(5)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)

    # save list into variable
    li = soup.select_one("ul.item_list li.slide")

    # use inspect & print all paragraph texts
    title_news = li.find('div', class_='content_title').get_text()
    print(title_news)

    # use inspect & print all paragraph texts
    paragraph = li.find('div', class_='article_teaser_body').get_text()
    print(paragraph)

    #Mars Featured Image

    # visit image URL
    browser.visit(url_image)

    time.sleep(5)

    # click on full featured image
    featured_img_button = browser.find_by_id("full_image")
    featured_img_button.click()

    time.sleep(5)

    # click on more info
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()

    # save image URL
    test = browser.links.find_by_partial_href("/spaceimages/images")
    test.click()

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    featured_img = img_soup.find('img')['src']

    # Mars Weather Report

    # save twitter URL as variable
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    # visit the URL
    browser.visit(url_twitter)

    time.sleep(10)

    # save HTML into variable & parse
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(10)

    content = soup.find_all('div', class_ = 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')

    mars_tweet = content[0]
   
    mars_weather = mars_tweet.find('span', class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
    print(mars_weather)

    # Mars Facts

    # save twitter URL as variable
    url_facts = "https://space-facts.com/mars/"

    # read webpage into tables with Pandas
    tables = pd.read_html(url_facts)
    tables

    time.sleep(5)

    type(tables)

    df = tables[0]

    df.rename(columns={0: 'Subject', 1: 'Value'})

    html_table = df.to_html()
    html_table

    # Mars Hemispheres

    url_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemi)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # find image links by class
    image_class = soup.find_all('div', class_='item')

    # save hemisphere images into list 
    hemi_links = []
    # find root URL for site
    root_URL = "https://astrogeology.usgs.gov"

    # loop through each image link & pull image URL & title
    for img in image_class:
        # save the image title 
        title_img = img.find('h3').text
        # find the end URL for each image
        img_end_url = img.find('a', class_='itemLink product-item')['href']
        # go to the image link
        browser.visit(root_URL + img_end_url)
        # save HTML into variable & parse
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # save image URL
        image_url = root_URL + soup.find('img', class_='wide-image')['src']
        # append the dictionary
        hemi_links.append({"Title": title_img, "Image_URL": image_url})

    mars_scrape = {
        "News_Title": title_news,
        "News_Content": paragraph,
        "Mars_Featured_Image": featured_img,
        "Mars_Weather_Data": mars_weather,
        "Mars_Facts": html_table,
        "Mars_Hemisphere_Images": hemi_links
            }

    browser.quit()

    return mars_scrape

if __name__ == "__main__":
    print("Loading....")    
    scrape()
