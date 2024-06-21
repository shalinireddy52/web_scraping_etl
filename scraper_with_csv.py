import requests
from bs4 import BeautifulSoup
import csv
import time

# Target URL to scrape
base_url = "http://quotes.toscrape.com"

# Open a CSV file to save the data
with open("quotes.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Quote", "Author", "Tags"])  # Write the header row

    # Loop through the pages
    page_num = 1
    while True:
        url = f"{base_url}/page/{page_num}/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_num}: {e}")
            break  # Exit the loop if there's a network error

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            print("No quotes found on page", page_num)
            break  # Exit the loop if no quotes are found (end of pages)

        for quote in quotes:
            try:
                text = quote.find("span", class_="text").get_text()
                author = quote.find("small", class_="author").get_text()
                tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
                writer.writerow([text, author, ", ".join(tags)])
            except AttributeError as e:
                print(f"Error extracting quote data: {e}")

        page_num += 1  # Go to the next page
        time.sleep(1)  # To avoid overwhelming the server
