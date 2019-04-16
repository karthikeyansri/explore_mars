from typing import Dict, Any

from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

return_info: Dict[Any, Any] = {}

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def get_mars_news():
    try:
        browser = init_browser()

        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve latest news title and news teaser paragraph
        nasa_news_header = soup.find('div', class_='content_title').find('a').text
        nasa_news_teaser = soup.find('div', class_='article_teaser_body').text

        return_info['title'] = nasa_news_header
        return_info['teaser'] = nasa_news_teaser

    except:
        pass
    finally:
        browser.quit()

    return return_info

def get_mars_images():
    try:
        browser = init_browser()

        mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(mars_images_url)

        mars_images = browser.html
        soup = BeautifulSoup(mars_images, 'html.parser')

        # form url using bs4
        mars_images_url = soup.find('article')['style'].replace('background-image: url(', '').replace(');', '')[1:-1]
        mars_images_url = 'https://www.jpl.nasa.gov' + mars_images_url

        return_info['mars_image_url'] = mars_images_url

    except:
        pass
    finally:
        browser.quit()

    return return_info

def get_mars_weather():
    try:
        browser = init_browser()

        mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather_url)

        mars_weather = browser.html
        soup = BeautifulSoup(mars_weather, 'html.parser')

        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in latest_tweets:
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                break
            else:
                pass

        return_info['mars_weather'] = weather_tweet

    except:
        pass
    finally:
        browser.quit()

    return return_info

def get_mars_facts():
    try:
        browser = init_browser()
        mars_facts_url = 'http://space-facts.com/mars/'

        mars_facts = pd.read_html(mars_facts_url)
        mars_facts_df = mars_facts[0]

        mars_facts_df.columns = ['Description', 'Value']
        mars_facts_df.set_index('Description', inplace=True)

        return_info['mars_facts'] = mars_facts_df.to_html()

    except:
        pass

    finally:
        browser.quit()

    return return_info

def get_mars_hemispheres():
    try:
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        items = soup.find_all('div', class_='item')

        hemisphere_image_urls = []
        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        for item in items:
            title = item.find('h3').text

            img_url = item.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + img_url)

            img_html = browser.html
            soup = BeautifulSoup(img_html, 'html.parser')

            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

            hemisphere_image_urls.append({"title": title, "img_url": img_url})

        return_info['mars_hemisphere_uris'] = hemisphere_image_urls

    except:
        pass

    finally:
        browser.quit()

    return return_info


