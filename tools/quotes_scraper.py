import requests
from bs4 import BeautifulSoup
import csv

# 1. Fetch the webpage
url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 2. Find all the quote blocks on the page
quotes = soup.find_all("div", class_="quote")

# 3. Open a CSV file and write the data
with open("data/quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "author", "tags"]) # The Header
    
    for q in quotes:
        text = q.find("span", class_="text").get_text()
        author = q.find("small", class_="author").get_text()
        
        # Tags are a list, so we join them with commas into one string
        tags = [tag.get_text() for tag in q.find_all("a", class_="tag")]
        tags_str = ", ".join(tags)
        
        # Write the row (csv.writer handles the quotes automatically)
        writer.writerow([text, author, tags_str])

print(f"Successfully scraped {len(quotes)} quotes into data/quotes.csv")
