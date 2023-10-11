from flask import render_template, request
from TVonline import app
from TVonline.forms import SearchForm
from TVonline.funcs import main, information, home, poster, ip_getter
from threading import Thread
import json
from bs4 import BeautifulSoup
from datetime import datetime, time
from pytz import timezone

domain = "https://tv-online.saed3.repl.co"


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
  form = SearchForm()
  with open("TVonline/database/home.json") as file:
    recent = json.load(file)
  urls = []
  for url in recent[1]:
    if "movies" in url:
      urls.append(f"movies/{url.split('/')[-1]}")
      continue
    urls.append(f"series/{url.split('/')[-1]}")
  contents = list(zip(recent[0], urls, recent[-1]))
  return render_template("home.html",
                         title="TV online - Home",
                         form=form,
                         contents=contents,
                         styles=["home", "main"])


@app.route("/search", methods=["GET", "POST"])
def search():
  form = SearchForm()
  name = request.args.get("q").replace(" ", "+")
  results = main(name)
  if not results:
    return render_template("search.html",
                           title=f"TV online - {name}",
                           name=name,
                           not_found=True,
                           styles=["search", "main"],
                           form=form)
  titles, urls, posters = results
  re_urls = []
  for index in range(0, len(urls)):
    if "movie" in urls[index]:
      re_urls.append(f"movies/{urls[index].split('/')[-1]}")
    else:
      re_urls.append(f"series/{urls[index].split('/')[-1]}")
  contents = list(zip(titles, re_urls, posters))
  title = name.replace("+", " ")
  return render_template("search.html",
                         title=f"TV online - {title}",
                         contents=contents,
                         name=title,
                         styles=["search", "main"],
                         form=form)


@app.route("/movies/<name>", methods=["GET", "POST"])
def movies(name, index=0):
  #return render_template("serieses.html", styles=["main"])
  #if index =! 0
  domain = ip_getter()
  url = domain + "/movie/" + name
  info = information(url, "movie")
  return render_template("movies.html",
                         title=info["title"],
                         name=info["title"],
                         poster=info["poster"],
                         info=[ 
                           detail.strip() for detail in info["info"].split("\n")],
                         story=info["story"],
                         watch_server=info["watchServers"][0],
                         styles=["main", "movies"])


@app.route("/series/<name>/<index>", methods=["GET", "POST"])
@app.route("/series/<name>", methods=["GET", "POST"])
def serieses(name, index=0):
  #if index != 0:
  #results = main(name)
  #url = results[0][int(index) - 512]
  #info = information(url)
  return render_template("serieses.html", title=name, styles=["main"])


target = timezone('Africa/Cairo')
retime = str(time(hour=00, minute=1, second=0))


def rehome():
  while True:
    current_time = str(datetime.now(target).strftime("%H:%M:%S"))
    if current_time != retime:
      continue
    recent = home()
    titles = recent[0]
    urls = recent[1]
    posters = poster(urls)
    with open("TVonline/database/home.json", "w") as file:
      json.dump([titles, urls, posters], file)


thread = Thread(target=rehome)
