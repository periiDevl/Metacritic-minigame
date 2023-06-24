import requests
from bs4 import BeautifulSoup

url = "https://www.metacritic.com/browse/games/score/metascore/all/ps4/filtered"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(response.text, 'html.parser')

titles = soup.find_all("a", class_="title")

with open("top.txt", "w") as f:
    for title in titles:
        formatted_title = title.text.strip().replace(" ", "-").lower().replace(":", "").replace("'", "")
        f.write(formatted_title + "\n")
