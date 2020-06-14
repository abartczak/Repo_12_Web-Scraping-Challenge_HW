#!/usr/bin/env python

# Import the necessary Python modules
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import numpy as np
import pandas as pd
import time
import re

def get_chrome():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "D:/Drivers/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


def scrape():

    # ###
    # ### NASA Mars News
    # ###

    # Render NASA website in Chrome adding some delay to settle display
    browser  = get_chrome()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    # Get HTML object and process it with Beautiful Soup
    html = browser.html 
    soup = bs(html, 'html.parser')
    #print(soup.prettify())

    # Start testing the returned object  
    title = soup.title.text
    print(title)

    # View part of HTML code to find tags and classes needed to gather the rerquired text
    results = soup.find_all('div', class_='slide', limit=20)
    for i in range(1): 
        print(results[0])

    # Pull news title based on the unique class 'content_title'
    title_list = soup.find_all('div', class_='content_title')
    news_title=title_list[0].text.strip()
    news_title

    # Pull news paragraph based on the unique class 'rollover_description_inner'
    # results are returned as an iterable list
    paragraph_list = soup.find_all('div', class_='rollover_description_inner')
    news_p=paragraph_list[0].text.strip()
    news_p

    # Exit the current Chrome browser session
    browser.quit()

    # ###
    # ### JPL Mars Space Images - Featured Image
    # ###

    # Render JPL website in Chrome adding some delay to settle display
    browser  = get_chrome()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)

    # Select the 'FULL IMAGE' button to get large high resolution image
    browser.click_link_by_partial_text('FULL IMAGE')

    # Find 'more_info' selector to get to the right level of hierarchy
    browser.is_element_present_by_text("more info", wait_time=1)
    mi_element = browser.find_link_by_partial_text("more info")
    mi_element.click()

    # Get HTML object and process it with Beautiful Soup
    html = browser.html 
    soup = bs(html, 'html.parser')
    #print(soup.prettify())

    # Continue scraping the image based on element 'figure' class_='lede'
    image_url = soup.find('figure', class_='lede').a["href"]

    # Update scraped image URL to create a featureed image URL
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'
    featured_image_url

    # Exit the current Chrome browser session
    browser.quit()

    # ###
    # ### Mars Weather
    # ###

    # Render JPL website in Chrome adding some delay to settle display
    browser  = get_chrome()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(2)

    # Get HTML object and process it with Beautiful Soup
    html = browser.html 
    soup = bs(html, 'html.parser')
    print(soup.prettify())

    tweet = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').get_text()
    tweet

    mars_weather = tweet.replace('\n', ' ')
    mars_weather

    # Exit the current Chrome browser session
    browser.quit()

    # ###
    # ### Mars Facts
    # ###   

    # Render JPL website in Chrome adding some delay to settle display
    browser  = get_chrome()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(2)

    # Get HTML object and process it with Beautiful Soup
    html = browser.html 
    soup = bs(html, 'html.parser')
    print(soup.prettify())

    # Access Mars facts table from HTML above, read into Pandas and process it
    facts_table = pd.read_html(url)
    facts_df = facts_table[0]
    facts_df.columns = ["Category", "Measurement"]
    facts_df = facts_df.set_index("Category")
    facts_df

    # Export table above to HTML for further processing
    mars_facts_table = facts_df.to_html()
    mars_facts_table

    # Exit the current Chrome browser session
    browser.quit()

    # ###
    # ### Mars Hemispheres
    # ###   

    # Render Astropedia website in Chrome adding some delay to settle display
    browser  = get_chrome()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(10)

    # Get HTML object and process it with Beautiful Soup
    html = browser.html 
    soup = bs(html, 'html.parser')
    print(soup.prettify())

    # Select HTML code corresponding to the four Marse Image items only
    imgs = soup.find_all("div", class_="item")
    imgs

    # Access the four Large High Resolution images by clicking a link corresponding to the corresponding image title
    hemisphere_image_urls = []

    for img in imgs:
        # Get a page title and acces that page
        title = img.find('h3').text
        browser.click_link_by_partial_text(title)
        time.sleep(2)

        # Get HTML object and process it with Beautiful Soup
        html = browser.html 
        single_soup = bs(html, 'html.parser')
        
        # Process this page by Beautiful Soup and build the complete dictionary with title and HTML link
        img_url = single_soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : f'https://astrogeology.usgs.gov{img_url}'})

        # Return to the original HTML link
        browser.visit(url)
        time.sleep(5)    
        
    hemisphere_image_urls

    # Exit the current Chrome browser session
    browser.quit()

    # Since I had issues upstreamm with Twitter scraping, I saved data from Jypyter Notebook original run to diagnose the issue
    #mars_weather = 'InSight sol 548 (2020-06-11) low -91.2ºC (-132.1ºF) high -2.8ºC (26.9ºF) winds from the SW at 4.8 m/s (10.8 mph) gusting to 20.1 m/s (45.0 mph) pressure at 7.40 hPa'

    # Likewise, I had issues with extracting pictures of Mars since splinter controlled web scraping was timing out or crashing, so I save the values below from Jupyter notebook run
    #hemisphere_image_urls = [{'title': 'Cerberus Hemisphere Enhanced',
    #                            'img_url': 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'},
    #                        {'title': 'Schiaparelli Hemisphere Enhanced',
    #                            'img_url': 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'},
    #                        {'title': 'Syrtis Major Hemisphere Enhanced',
    #                            'img_url': 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},
    #                        {'title': 'Valles Marineris Hemisphere Enhanced',
    #                            'img_url': 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}]

    # Create the final dirctionary with the scraped data as a function output
    final_dict = {
        "Latest_Mars_Title": news_title,
        "News": news_p,
        "Featured_Picture": featured_image_url,
        "Twitter": mars_weather,
        "Table": mars_facts_table,  
        "Hem_Img_URLs": hemisphere_image_urls}

    print(final_dict)
    return final_dict
