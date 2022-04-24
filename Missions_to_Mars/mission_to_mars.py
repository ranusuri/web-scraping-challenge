#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
import requests
import pymongo
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data = {}

    # URL of the page to be scrapped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    ### NASA Mars News

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text

    news_title
    news_p

    #add new title and paragraph to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    ### JPL Mars Space Images - Featured Image
    jpl_url="https://spaceimages-mars.com"
    browser.visit(jpl_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    image_block=soup.find('img', class_='headerimage fade-in')

    image_url = image_block.get("src")

    featured_image_url=jpl_url+ "/" + image_url

    featured_image_url

    #add featured image url to dictionary
    mars_data['featured_image_url'] = featured_image_url


    ### Mars Facts

    #Visit the Mars Facts webpage [here](https://galaxyfacts-mars.com) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.

    url='https://galaxyfacts-mars.com'
    tables=pd.read_html(url)
    type(tables)
    df = tables[0]
    df.head()

    #drop single header rows


    df.head()
    mars_fact=df.rename(columns={0:"Description", 1:"Mars",2:"Earth"},errors="raise")

    #df.drop('dropme',axis=1,inplace=True)
    #mars_fact.set_index("Stat",inplace=True)

    mars_fact.columns = mars_fact.columns.get_level_values(0)

    # remove column 
    #mars_fact = mars_fact.drop(mars_fact.columns[2], axis=1)
    #drop first row
    mars_fact = mars_fact.iloc[1:,:]

    mars_fact = mars_fact.set_index('Description')

    mars_fact

    #Use to_html method to generate HTML tables from df
    html_table = mars_fact.to_html()
    html_table

    #adding to dictionary
    mars_data["html_table"] = html_table


    # In[132]:


    #Save as html file
    mars_fact.to_html('mars_table.html')

    ### Mars Hemispheres

    # Setting url for alternate browser
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')

    # Extract hemispheres item elements
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    # Loop through each hemisphere item
    for item in mars_item:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(url+hem_url)
            html=browser.html
            soup=BeautifulSoup(html,'html.parser')
            image_src=soup.find('li').a['href']
            image_src=url + image_src
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':image_src
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)


    hemisphere_image_urls

    #adding hemisphere_image_urls to dict
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls


    mars_data

    return mars_data

if __name__ == "__main__":
    scrape()
