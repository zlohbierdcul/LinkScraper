from GrabzIt import GrabzItClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import json

URL = "https://zoro.to/watch/one-piece-100"

grab = GrabzItClient.GrabzItClient(
    "MzM0MzQ0MWU2ZWM4NDkwN2IyYjJjYjcwZTE4NGQ5ZGU=", "Kj8hPz8/fQEhRj8/P1lpP3duVD8/HnE/T2s/Pz90CEo=")


def get_sufix(url, domain):
    url_string = str(url)
    parsed = url_string.replace("https://" + domain + "/watch/", "")
    index = parsed.index("?")
    return parsed[:index]


def create_html(url):
    grab.URLToRenderedHTML(url)

    if not os.path.exists("pages"):
        os.mkdir("pages")
    path = "./pages/page.html"
    grab.SaveTo(path)


def create_json(dict):
    with open("links.json", "w") as data:
        json.dump(dict, data)


def create_links(sufix):
    with open('./pages/page.html', 'rb') as page:
        contents = page.read()
        soup = BeautifulSoup(contents, "html.parser")

    links = {}
    episode = 0
    for link in soup.find_all("a"):
        url = link.get("href")
        if "watch/" + sufix in str(url):
            episode += 1
            links.setdefault(episode, domain_name + url)
    return links


if __name__ == "__main__":
    url = input("Please enter the url: ")
    # url = URL
    domain_name = urlparse(url).netloc

    print(get_sufix(url=url, domain=domain_name))
    create_html(url=url)
    create_json(create_links(get_sufix(url, domain_name)))
    try:
        os.remove("pages/page.html")
    except Exception:
        print("file not found")
