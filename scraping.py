#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


# set up splinter
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    #title_name, url = hemisphere_scrape(browser)

       # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_images": featured_images(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_scrape(browser)
        }
    

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # scrape mars news
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Add try/except for error handling
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### Featured Images

def featured_images(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    print (img_url)
    return img_url

# Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()




#Hemispheres
# url = 'https://marshemispheres.com/'
# response = requests.get(url)
# img_mars = soup(response.text, 'html.parser')


def hemisphere_scrape(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    #html = browser.html
    #img_mars = soup(html, 'html.parser')

    response = requests.get(url)
    img_mars = soup(response.text, 'html.parser')


# Create a list to hold the images and titles.
    hemisphere_image = []
    # Write code to retrieve the image urls and titles for each hemisphere.

    results = img_mars.find_all('div', class_='item')

    for result in results:
        link = result.find('img', class_ = 'thumb').get('src')
        title_name = result.find('h3').text
        url = (f'https://marshemispheres.com/' + link)
        #hemispheres = {img_url, title}
        hemispheres = {
        "title": title_name,
        "img_url": url
    }
        hemisphere_image.append(hemispheres) 
    return hemisphere_image
# 4. Print the list that holds the dictionary of each image url and title.
    print(hemisphere_image)

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())





