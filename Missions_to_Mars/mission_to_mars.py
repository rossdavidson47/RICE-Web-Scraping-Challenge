#!/usr/bin/env python
# coding: utf-8

# # Scraping with Pandas

# In[1]:


# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set up ChromeDriver to run Google Chrome from Python
executable_path = {'executable_path': '/Users/Noctura/RICE/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[2]:


#NASA Mars News
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.

#code from 07-Ins_Splinter
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
time.sleep(10)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[3]:


#Find the latest news title and paragraph text
first_content_title = soup.find_all('div', class_="content_title")[1].text
first_article_teaser_body = soup.find('div', class_="article_teaser_body").text

print(f'The first title on the NASA webpage is: {first_content_title}')
print(' ')
print(f'The first paragraph text is: {first_article_teaser_body}')


# In[4]:


#JPL Mars Space Images - Featured Image
#Visit the url for JPL Featured Space Image here.
#Use splinter to navigate the site and find the image url for the current Featured Mars Image 
#and assign the url string to a variable called featured_image_url.
#Make sure to find the image url to the full size .jpg image.
#Make sure to save a complete url string for this image.
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
time.sleep(1)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


#find the image by navigating through the buttons
#https://splinter.readthedocs.io/en/latest/finding.html
#https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
browser.links.find_by_partial_text('FULL IMAGE').first.click()
browser.links.find_by_partial_text('more info').first.click()
browser.links.find_by_partial_text('.jpg').first.click()
featured_image_url = browser.url
print(f'The url for the featured image is {featured_image_url}')


# In[6]:


#Mars Weather
#Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
#Save the tweet text for the weather report as a variable called mars_weather.
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
time.sleep(1)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[7]:


mars_weather = soup.find_all("div", attrs={"data-testid":"tweet"})[0]
print(f'The text of the first tweet is:')
print(f'{mars_weather.text}')


# In[8]:


#Mars Facts
#Visit the Mars Facts webpage https://space-facts.com/mars/ 
#and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#Use Pandas to convert the data to a HTML table string.
#Code from 09-ins-pandas_scraping
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
tables


# In[9]:


#Convert to a df and tidy up
df = tables[0]
df.columns = ['Mars Planet Profile', 'Values']
df.set_index('Mars Planet Profile', inplace=True)
df


# In[10]:


#convert to html and print
html_table = df.to_html()
html_table.replace('\n', '')
df.to_html('Mars_Planet_Profile.html')
html_table


# In[11]:


#Mars Hemispheres
#Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
#You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
#Save both the image url string for the full resolution hemisphere image, 
#and the Hemisphere title containing the hemisphere name. 
#Use a Python dictionary to store the data using the keys img_url and title.
#Append the dictionary with the image url string and the hemisphere title to a list. 
#This list will contain one dictionary for each hemisphere.

#set up
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
hemisphere_image_urls =[]
img_url_list = []
title_list = ["Valles Marineris Hemisphere","Cerberus Hemisphere","Schiaparelli Hemisphere", "Syrtis Major Hemisphere"]


# In[12]:


#Loop across the website colleting urls to images
for hemisphere in title_list:
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.links.find_by_partial_text(f'{hemisphere}').first.click()
    image_link = browser.links.find_by_partial_text('Sample')
    img_url_list.append(image_link['href'])


# In[13]:


#Create list of dictionaries, code from 10-stu-doctor-decoder
for i in range(0, len(title_list)):
    hemisphere_image_urls.append({"title":title_list[i], "img_url":img_url_list[i]})
hemisphere_image_urls

