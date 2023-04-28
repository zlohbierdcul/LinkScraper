from GrabzIt import GrabzItClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import json

grab = GrabzItClient.GrabzItClient(
    "MzM0MzQ0MWU2ZWM4NDkwN2IyYjJjYjcwZTE4NGQ5ZGU=", "Kj8hPz8/fQEhRj8/P1lpP3duVD8/HnE/T2s/Pz90CEo=")


def create_json(dict, file_name):
    with open(f"{file_name}.json", "w") as data:
        json.dump(dict, data)


def get_soup(path):
    with open(f'./pages/{path}.html', 'rb') as page:
        contents = page.read()
        soup = BeautifulSoup(contents, "html.parser")
    return soup


def get_link_from_json(selection, file_name):
    with open(f"{file_name}.json") as json_file:
        data = json.load(json_file)
    return data[selection]["URL"]


def create_html(url, name):
    # print("Currently creating the rendered HTML.\nThis this can take a few seconds!")
    grab.URLToRenderedHTML(url)

    if not os.path.exists("pages"):
        os.mkdir("pages")
    path = f"./pages/{name}.html"
    grab.SaveTo(path)
    # print("Finished rendering the HTML")


def find_shows(show_name, path):
    # print("Currently finding all Episodes!")
    with open(f'./pages/{path}.html', 'rb') as page:
        contents = page.read()
        soup = BeautifulSoup(contents, "html.parser")

    search_results = {}
    film_list = soup.find("div", class_="film_list")
    items = film_list.find_all("a", class_="dynamic-name")

    show_count = 0
    for episode_item in items:

        show_count += 1
        url = "zoro.to" + str(episode_item.get("href"))
        title = episode_item.get("title")
        search_results[show_count] = {
            "Title": title,
            "URL": url
        }
    try:
        os.remove(f"pages/{path}.html")
    except Exception:
        print("file not found")
    return search_results

def find_seasons(url):
    create_html(url, "seasons")
    
    season_links = [] 

    soup = get_soup("seasons")

    try:
        season_block = soup.find("section", class_="block_area-seasons")

        if season_block != None:
            seasons = season_block.find_all("a", class_="os-item")
        
        for season in seasons:
            if "Season" in season.find("div", class_="title").text:
                season_links.append("zoro.to" + str(season.get("href")))
        return season_links
    except Exception:
        return None


def find_links():
    # print("Currently finding all Episodes!")
    with open('./pages/page.html', 'rb') as page:
        contents = page.read()
        soup = BeautifulSoup(contents, "html.parser")

    links = {}
    items = soup.find_all("a", class_="ep-item")
    total_episodes = len(items)
    filler_count = 0

    for episode_item in items:
        url = "zoro.to" + str(episode_item.get("href"))
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
    try:
        os.remove(f"pages/page.html")
    except Exception:
        print("file not found")
    return links


def print_results(file_name):
    with open(f"{file_name}.json") as json_file:
        data = json.load(json_file)

    for element in data:
        print(f"[{element}] {data[element]['Title']}")

# Finds the URL to the watch site from a given URL


def find_watch_link(url):
    create_html(url, "watch")
    soup = get_soup("watch")
    watch_url = "zoro.to" + str(soup.find("a", class_="btn-play").get("href"))
    try:
        os.remove("pages/watch.html")
    except Exception:
        print("file not found")
    return watch_url


if __name__ == "__main__":
    print("Search:")
    search = input("> ")

    create_html("zoro.to/search?keyword=" + search.replace(" ", "-"), "search")
    show_list = find_shows(search, "search")
    
    if len(show_list) > 0:
        create_json(show_list, "search")

        print_results("search")

        print("Which one?")
        selection = input("> ")
        selected_show_url = get_link_from_json(selection, "search")

        season_index = 0
        show_dict = {}
        season_links = find_seasons(selected_show_url)

        if season_links == None:
            create_html(find_watch_link(selected_show_url), "page")
            show_dict["Season 1"] = find_links()
        else:
            for link in season_links:
                season_index += 1
                create_html(find_watch_link(link), "page")
                show_dict["Season " + str(season_index)] = find_links()

        create_json(show_dict, search.lower().replace(" ", "-"))
    else:
        print("No shows were found! try again!")
