from newspaper import Article
import pandas as pd
import nltk
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


def get_cnn_articles():
    cnn_article_urls = []

    for current_month in range(1, 5):
        cnn_base_url = "https://www.cnn.com/article/sitemap-2022-{month}.html".format(month=current_month)
        print("Processing url {current_url}".format(current_url=cnn_base_url))
        page = requests.get(cnn_base_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            print("Found the URL:", a['href'])
            cnn_article_urls.append(("CNN", a['href']))

    cnn_dataframe = pd.DataFrame(cnn_article_urls, columns=["Source", "NewsLink"])
    cnn_dataframe.to_excel("CNN.xlsx", index=False)


# function to parse web articles
def parse_article(article_url):
    """
    function which extracts information given a web url
    :param article_url: article url
    :return: json record
    """

    # passing the article url
    article = Article(article_url)

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


def process_cnn_site():
    cnn_articles = pd.read_excel("CNN.xlsx")
    cnn_articles_data = []

    for index, row in tqdm(cnn_articles.iterrows(), total=cnn_articles.shape[0]):
        try:
            record = parse_article(row["NewsLink"])
            cnn_articles_data.append([
                "CNN",
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

    cnn_news_dataframe = pd.DataFrame(cnn_articles_data,
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

    cnn_news_dataframe.to_excel("CNN_Articles.xlsx", index=False)


process_cnn_site()