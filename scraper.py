import requests
from bs4 import BeautifulSoup

# Target URL to scrape
url = "http://quotes.toscrape.com"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find all quote containers on the page
quotes = soup.find_all("div", class_="quote")

# Loop through the quotes and print them
for quote in quotes:
    text = quote.find("span", class_="text").get_text()
    author = quote.find("small", class_="author").get_text()
    print(f"Quote: {text}")
    print(f"Author: {author}")
    print("-" * 80)
