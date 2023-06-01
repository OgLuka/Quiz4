import requests
from bs4 import BeautifulSoup
import csv
import time

url = "https://www.imdb.com/chart/top"

interval = 16

num_pages = 5

with open("movies.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Year", "Rating"])

    for page in range(1, num_pages + 1):
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.select(".lister-list tr")

        for listing in listings:
            title = listing.select_one(".titleColumn a").text
            year = listing.select_one(".titleColumn span.secondaryInfo").text.strip("()")
            rating = listing.select_one(".imdbRating strong").text

            writer.writerow([title, year, rating])

        next_page_link = soup.select_one(".lister-page-next a")

        if next_page_link and page < num_pages:
            url = "https://www.imdb.com" + next_page_link["href"]
        else:
            break

        time.sleep(interval)
