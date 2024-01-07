import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def get_final_url(url):
    try:
        session = requests.Session()
        response = session.get(url, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

def identify_website(url):
    if 'amazon.' in url:
        return 'amazon'
    elif 'flipkart.' in url:
        return 'flipkart'
    # Add more elif blocks for other e-commerce sites
    else:
        return None

def scrape_amazon(soup):
    # Placeholder selectors for Amazon - these will likely need to be updated
    title_selector = 'span#productTitle'
    price_selector = 'span#priceblock_ourprice'
    description_selector = 'div#productDescription'
    
    title = soup.select_one(title_selector).get_text().strip() if soup.select_one(title_selector) else "Title not found"
    price = soup.select_one(price_selector).get_text().strip() if soup.select_one(price_selector) else "Price not found"
    description = soup.select_one(description_selector).get_text().strip() if soup.select_one(description_selector) else "Description not found"
    
    return title, price, description

def scrape_flipkart(soup):
    # Placeholder selectors for Flipkart - these will likely need to be updated
    title_selector = 'span.B_NuCI'
    price_selector = 'div._30jeq3'
    description_selector = 'div._1mXcCf'
    
    title = soup.select_one(title_selector).get_text().strip() if soup.select_one(title_selector) else "Title not found"
    price = soup.select_one(price_selector).get_text().strip() if soup.select_one(price_selector) else "Price not found"
    description = soup.select_one(description_selector).get_text().strip() if soup.select_one(description_selector) else "Description not found"
    
    return title, price, description

def scrape_product_info(url):
    final_url = get_final_url(url)
    if not final_url:
        return {"error": "Failed to retrieve the final URL"}

    website = identify_website(final_url)
    if not website:
        return {"error": "Website not supported"}

    response = requests.get(final_url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        return {"error": "Failed to retrieve the webpage"}

    soup = BeautifulSoup(response.content, 'html.parser')

    if website == 'amazon':
        title, price, description = scrape_amazon(soup)
    elif website == 'flipkart':
        title, price, description = scrape_flipkart(soup)
    # Add more elif blocks for other e-commerce sites

    return {
        'title': title,
        'price': price,
        'description': description
    }

# Example Usage
url = 'https://www.flipkart.com/samsung-galaxy-z-flip3-5g-cream-128-gb/p/itmf84b792824408?pid=MOBG6YQHHB84XVGN&lid=LSTMOBG6YQHHB84XVGNXUIVZP&marketplace=FLIPKART&q=flip+mobile&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=1a04e17e-2e8a-49d6-9713-696a07833e73.MOBG6YQHHB84XVGN.SEARCH&ppt=sp&ppn=sp&ssid=zdv1d6a9ps0000001704613345658&qH=82fe25e4cc0bf1d7'
product_info = scrape_product_info(url)
print(product_info)
