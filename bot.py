import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_deals():
    url = "https://www.amazon.in/gp/goldbox"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    deals = []
    for deal in soup.select('.DealContent'):
        title = deal.select_one('.DealTitle').get_text(strip=True)
        link = "https://www.amazon.in" + deal.select_one('a')['href']
        link += "?tag=bestdealsbo06-21"  # your affiliate tag
        price = deal.select_one('.a-price .a-offscreen')
        price = price.text if price else 'Price not listed'

        deals.append((title, link, price))

        if len(deals) >= 10:
            break

    return deals

def generate_html(deals):
    html = f"""<html>
    <head><title>Best Deals</title></head>
    <body>
    <h1>Top Amazon Deals - {datetime.now().strftime('%d %B %Y')}</h1>
    <ul>
    """
    for title, link, price in deals:
        html += f"<li><a href='{link}' target='_blank'>{title}</a> - <b>{price}</b></li>\n"

    html += "</ul></body></html>"
    return html

if __name__ == "__main__":
    deals = get_deals()
    html = generate_html(deals)

    with open("index.html", "w", encoding='utf-8') as f:
        f.write(html)
