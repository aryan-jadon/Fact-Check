from newspaper import Article
import pandas as pd
import nltk
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from newspaper import Config


def get_articles():
    source_article_urls = []
    base_url = "https://www.newsweek.com/us?page={page_number}"
    for current_page in range(1, 500):
        current_url = base_url.format(page_number=current_page)
        print("Processing url {current_url}".format(current_url=current_url))
        req = Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})

        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        for a in page_soup.find_all('a', href=True):
            print("Found the URL:", a['href'])
            source_article_urls.append(("NewsWeek", a['href']))

    newsweek_dataframe = pd.DataFrame(source_article_urls, columns=["Source", "NewsLink"])
    newsweek_dataframe.to_excel("NewsWeek.xlsx", index=False)


# function to parse web articles
def parse_article(article_url):
    """
    function which extracts information given a web url
    :param article_url: article url
    :return: json record
    """
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

    config = Config()
    config.browser_user_agent = user_agent

    # passing the article url
    article = Article(article_url, config=config)

    # downloading the data
    article.download()

    # parsing the article
    article.parse()

    # processing natural language processing on article
    article.nlp()

    # creating a json record
    article_record = {
        "article_title": article.title,  # article title
        "article_authors": article.authors,  # article authors
        "article_published_date": str(article.publish_date),  # article published data
        "article_text": article.text,  # article web text
        "images_link": article.top_image,  # article image link
        "video_link": article.movies,  # article video link
        "article_summary": article.summary,  # article summary
        "article_keywords": article.keywords,  # keywords associated with articles
        "article_url": article_url  # article url
    }

    # return json record
    return article_record


def process_site():
    news_articles = pd.read_excel("NewsWeek.xlsx")
    news_articles_data = []

    for index, row in tqdm(news_articles.iterrows(), total=news_articles.shape[0]):
        try:
            article_url = "https://www.newsweek.com/" + row["NewsLink"]
            print(article_url)
            record = parse_article(article_url)
            news_articles_data.append([
                "NewsWeek",
                record["article_title"],
                ",".join(record["article_authors"]),
                record["article_published_date"],
                record["article_text"],
                record["article_summary"],
                ",".join(record["article_keywords"]),
                record["article_url"]
            ])
        except Exception as e:
            print(e)

    news_dataframe = pd.DataFrame(news_articles_data,
                                  columns=[
                                      "Source",
                                      "Title",
                                      "Authors",
                                      "PublishedDate",
                                      "ArticleText",
                                      "Summary",
                                      "Keywords",
                                      "URL"
                                  ])

    news_dataframe.to_excel("NewsWeek_Articles.xlsx", index=False)


process_site()
