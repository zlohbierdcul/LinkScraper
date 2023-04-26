from GrabzIt import GrabzItClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import json
import time

URL = "https://9animetv.to/watch/one-piece-100?ep=2714"

grab = GrabzItClient.GrabzItClient(
    "MzM0MzQ0MWU2ZWM4NDkwN2IyYjJjYjcwZTE4NGQ5ZGU=", "Kj8hPz8/fQEhRj8/P1lpP3duVD8/HnE/T2s/Pz90CEo=")


def get_sufix(url, domain):
    url_string = str(url)
    parsed = url_string.replace("https://" + domain + "/watch/", "")
    index = parsed.index("?")
    return parsed[:index]


def create_html(url):
    start = time.perf_counter()
    print("Currently creating the rendered HTML.\nThis this can take a few seconds!")
    grab.URLToRenderedHTML(url)

    if not os.path.exists("pages"):
        os.mkdir("pages")
    path = "./pages/page.html"
    grab.SaveTo(path)
    end = time.perf_counter()
    print("Finished rendering the HTML")
    print(f"It took: {end - start:0.4f} seconds")


def create_json(dict):
    with open("links.json", "w") as data:
        json.dump(dict, data)


def create_links(sufix):
    print("Currently finding all Episodes!")
    with open('./pages/page.html', 'rb') as page:
        contents = page.read()
        soup = BeautifulSoup(contents, "html.parser")

    links = {}
    items = soup.find_all("a", class_="ep-item")
    total_episodes = len(items)
    filler_count = 0

    for episode_item in items:
        url = domain_name + str(episode_item.get("href"))
        episode = episode_item.get("data-number")
        title = episode_item.get("title")
        filler = False

        if "ssl-item-filler" in episode_item.get("class"):
            filler = True
            filler_count += 1

        links[episode] = {
            "Title": title,
            "Filler": filler,
            "URL": url
        }
    print("Finished finding the episodes!")
    print("Total Episodes: ", total_episodes)
    print("Filler Episodes: ", filler_count)
    print("Non Filler Episodes: ", total_episodes - filler_count)
    return links


if __name__ == "__main__":
    url = input("Please enter the url: ")
    # url = URL
    start = time.perf_counter()
    domain_name = urlparse(url).netloc

    print(get_sufix(url=url, domain=domain_name))
    create_html(url=url)
    create_json(create_links(get_sufix(url, domain_name)))
    try:
        os.remove("pages/page.html")
    except Exception:
        print("file not found")
    end = time.perf_counter()
    print(f"Total Time: {end - start:0.4f} seconds")
