from bs4 import BeautifulSoup
from requests import Response, Session
from typing import Union

session: Session = Session()

main_url: str = "https://www.faselhd.center"
headers: dict[str] = {
  "User-Agent":
  "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def ip_getter():
  response: Response = session.get(main_url)
  soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
  domain: str = soup.body.find("a", {"class": "logo"}).get("href")
  return domain

def search(name) -> list[BeautifulSoup]:
  response: Response = session.get(main_url)
  soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
  domain: str = soup.body.find("a", {"class": "logo"}).get("href")
  params: dict[str] = {"s": name}
  response: Response = session.get(domain, headers=headers, params=params)
  soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
  results_soup: list[BeautifulSoup] = soup.find_all("div",
                                                    {"class": "postDiv"})
  return results_soup if len(
    results_soup) != 0 else f"There is NO result with \"{name}\"."


def results(soups: list[BeautifulSoup]) -> list[list]:
  titles: list[str] = [
    soup.contents[1].find("div", {
      "class": "h1"
    }).text for soup in soups
  ]
  links: list[str] = [soup.contents[1].get("href") for soup in soups]
  posters = [soup.contents[1].find("img").get("data-src") for soup in soups]
  return [titles, links, posters]


def information(url: str, typness="season") -> dict:
  response: Response = session.get(url, headers=headers)
  soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
  poster: Union[str, None] = soup.body.find("meta", {
    "itemprop": "thumbnailUrl"
  }).get("content")
  title: Union[str, None] = soup.body.find("div", {"class": "title"}).text
  info: str = "\n".join(item.text
                        for item in soup.body.find("div", {
                          "id": "singleList"
                        }).contents[0:] if item.text != "\n")
  story: Union[str, None] = soup.body.find("div", {"class": "singleDesc"}).text
  if typness != "season":
    watch_servers, downloadURLs = movie_eps_urls(soup)
    return {
      "title": title,
      "poster": poster,
      "info": info,
      "story": story,
      "watchServers": watch_servers,
      "downloadURLs": downloadURLs
    }
  return "لسه هكمل المسلسلات"


def movie_eps_urls(soup: BeautifulSoup) -> list:
  servers = soup.body.find("ul", {"class": "tabs-ul"}).contents[0:]
  watch_servers: list[str] = [
    servers[i + 1].get("onclick").split("= ")[-1].strip("'")
    for i in range(0, len(servers), 2) if i < 3
  ]
  servers2 = soup.body.find("div", {"class": "downloadLinks"}).find_all("a")
  downloadURLs: dict = {a.text: a.get("href") for a in servers2}

  return [watch_servers, downloadURLs]


def main(name: str) -> list[list]:
  soups: Union[list[BeautifulSoup], str] = search(name)
  if "NO" in soups:
    return False
  t_urls: list[list] = results(soups)
  titles: list = t_urls[0]
  urls: list = t_urls[1]
  posters: list = t_urls[2]
  return [titles, urls, posters]


def home() -> list:
  response: Response = session.get(main_url, headers=headers)
  soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
  results: list = soup.find_all("div", {"class": "form-row"})
  titles: list = []
  urls: list = []
  for items in results:
    for item in items.find_all("a"):
      title: str = item.find("div", {"class": "h5"}).text
      url: str = item.get("href")
      titles.append(title)
      urls.append(url)
  return [titles, urls]


def poster(urls: list) -> list:
  posters: list = []
  for url in urls:
    response: Response = session.get(url)
    soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
    poster: str = soup.body.find("meta", {
      "itemprop": "thumbnailUrl"
    }).get("content")
    posters.append(poster)

  return posters
