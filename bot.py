import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Replace with actual product URLs later
PRODUCT_URLS = [
    "https://www.amazon.in/dp/B07DJL15QT",  # Sample product
    "https://www.amazon.in/dp/B089MS8XQ7"
]

AFFILIATE_TAG = "bestdealsbo06-21"

def fetch_price_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find(id='productTitle')
    price = soup.find('span', {'class': 'a-offscreen'})
    if title and price:
        return {
            "title": title.get_text(strip=True),
            "price": price.get_text(strip=True),
            "url": url + f"?tag={AFFILIATE_TAG}"
        }
    return None

def update_html(deals):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"<html><head><title>Best Deals</title></head><body>")
        f.write(f"<h1>🔥 Best Deals (Updated: {now})</h1><ul>")
        for deal in deals:
            f.write(f"<li><a href='{deal['url']}' target='_blank'>{deal['title']}</a> - {deal['price']}</li>")
        f.write("</ul></body></html>")

if __name__ == "__main__":
    deals = []
    for url in PRODUCT_URLS:
        data = fetch_price_amazon(url)
        if data:
            deals.append(data)
    update_html(deals)
