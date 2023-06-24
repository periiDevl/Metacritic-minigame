import requests

def scrape_games(name):
    bool exist
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    base_url = "https://www.metacritic.com/game/playstation-4/"

    
    name = name.strip()
    url = base_url + name
    session = requests.Session()
    response = session.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 404:
        print("doesnt exist")
        exist = False
    else:
        print("exists")
        exist = True
    return exist




scrape_games(name)
