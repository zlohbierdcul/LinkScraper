from GrabzIt import GrabzItClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import json

grab = GrabzItClient.GrabzItClient(
    "MzM0MzQ0MWU2ZWM4NDkwN2IyYjJjYjcwZTE4NGQ5ZGU=", "Kj8hPz8/fQEhRj8/P1lpP3duVD8/HnE/T2s/Pz90CEo=")


def create_json(dict):
    with open("search.json", "w") as data:
        json.dump(dict, data)


def create_html(url):
    print("Currently creating the rendered HTML.\nThis this can take a few seconds!")
    grab.URLToRenderedHTML(url)

    if not os.path.exists("pages"):
        os.mkdir("pages")
    path = "./pages/search.html"
    grab.SaveTo(path)
    print("Finished rendering the HTML")


def find_shows():
    print("Currently finding all Episodes!")
    with open('./pages/search.html', 'rb') as page:
        contents = page.read()
        soup = BeautifulSoup(contents, "html.parser")

    search_results = {}
    items = soup.find_all("a", class_="dynamic-name")

    show = 0
    for episode_item in items:
        show += 1
        url = "zoro.to/" + str(episode_item.get("href"))
        title = episode_item.get("title")

        search_results[show] = {
            "Title": title,
            "URL": url
        }
    return search_results


def find_watch_link(url):
    pass


if __name__ == "__main__":
    print("Search:")
    search = input("> ")

    create_html("zoro.to/search?keyword=" + search.replace(" ", "-"))
    create_json(find_shows())
