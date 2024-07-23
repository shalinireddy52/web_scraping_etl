import requests
from bs4 import BeautifulSoup
import csv
import time

# Target URLs to scrape
urls = [
    "http://quotes.toscrape.com",
    "http://quotes.toscrape.com/tag/inspirational/",
    "http://quotes.toscrape.com/tag/love/"
]

# Open a CSV file to save the data
with open("quotes_multiple_sources.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Quote", "Author", "Tags", "Source"])  # Added source column to track where the quote came from

    # Loop through the URLs
    for url in urls:
        page_num = 1
        while True:
            response = requests.get(f"{url}/page/{page_num}/")
            if response.status_code != 200:
                break  # Exit the loop if no more pages or failed request

            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all("div", class_="quote")

            if not quotes:
                break  # Exit the loop if no quotes are found (end of pages)

            for quote in quotes:
                text = quote.find("span", class_="text").get_text()
                author = quote.find("small", class_="author").get_text()
                tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

                # Write the quote data to the CSV file along with the source URL
                writer.writerow([text, author, ", ".join(tags), url])

            page_num += 1
            time.sleep(1)  # Avoid overwhelming the server
