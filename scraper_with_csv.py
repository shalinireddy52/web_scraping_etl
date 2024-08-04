import requests
from bs4 import BeautifulSoup
import csv
import time

# Target URL to scrape
base_url = "http://quotes.toscrape.com"

def clean_data(text):
    """Clean up unwanted characters and leading/trailing spaces."""
    return text.strip().replace("\n", " ").replace("\r", "").replace("\t", "")

# Open a CSV file to save the data
with open("quotes_cleaned.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Quote", "Author", "Tags"])  # Write the header row

    page_num = 1
    while True:
        url = f"{base_url}/page/{page_num}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break  # Exit the loop if no quotes are found (end of pages)

        for quote in quotes:
            try:
                text = quote.find("span", class_="text").get_text()
                author = quote.find("small", class_="author").get_text()
                tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

                # Clean the data before saving
                text = clean_data(text)
                author = clean_data(author)
                tags = [clean_data(tag) for tag in tags]

                if not text or not author:
                    continue  # Skip quotes that are missing critical data (e.g., empty quote or author)

                # Write the quote data to the CSV file
                writer.writerow([text, author, ", ".join(tags)])

            except AttributeError as e:
                print(f"Error extracting quote data: {e}")

        page_num += 1
        time.sleep(1)  # To avoid overwhelming the server
