import os
from flask import Flask, jsonify, request, abort, render_template, url_for, json
from newsapi import NewsApiClient
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from io import BytesIO
import re
import json
app = Flask(__name__)
z="Homicide/Murder"

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/crime-charts.html")
def visualize():
    f = "Population"
    n = "2020"
    df = pd.read_excel(r"DataFinal17-20.xlsx", sheet_name=n)
    df2 = df.iloc[:, 1:23]
    titles = z + " vs \n" + f
    sns.set()
    sns.lmplot(x=z, y=f, data=df2, hue="cluster", legend=1, fit_reg=False, height=6, aspect=1.8).set(title=titles)
    figfile = BytesIO()
    plt.savefig(figfile, format="png")
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    return render_template("crime-charts.html", response=str(figdata_png, "utf-8"))

@app.route('/crime-data.html')
def crime_locator():
    return render_template('crime-data.html')


@app.route('/crime-map.html')
def crime_map():
    return render_template('crime-map.html')

@app.route('/find.html')
def find():
    return render_template('find.html')


newsapi = NewsApiClient(api_key='eb220da406224eedaf4faaa728da0bd5')


def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources, domains


@app.route("/news-feed.html", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        keyword = keyword + ' Crime'
        related_news = newsapi.get_everything(q=keyword,sources=sources,domains=domains,language='en',sort_by='publishedAt')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100: no_of_articles = 100
        print("no.of articles")
        all_articles = newsapi.get_everything(q=keyword, sources=sources, domains=domains, language='en', sort_by='publishedAt', page_size=no_of_articles)['articles']
        print("end of if home")
        return render_template("news-feed.html", all_articles=all_articles, keyword=keyword)
    else:
        #top_headlines = newsapi.get_top_headlines(country="in", language="en")
        #total_results = top_headlines['totalResults']
        #if total_results > 100: total_results = 100
        #all_headlines = newsapi.get_top_headlines(country="in", language="en", page_size=total_results)['articles']
        #return render_template("news-feed.html", all_headlines=all_headlines)
        sources, domains = get_sources_and_domains()
        keyword1 = 'Maharashtra Crime'
        related_news = newsapi.get_everything(q=keyword1,sources=sources,domains=domains,language='en',sort_by='publishedAt')
        no_of_articles = related_news['totalResults']
        all_articles = newsapi.get_everything(q=keyword1, sources=sources, domains=domains, language='en', sort_by='publishedAt', page_size=no_of_articles)['articles']
        print("end of if home")
        return render_template("news-feed.html", all_articles=all_articles, keyword=keyword1)

if __name__ == "__main__":
    app.run(debug=True)
