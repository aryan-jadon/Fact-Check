import requests
from newspaper import Article
import pandas as pd
import nltk
from tqdm import tqdm
from bs4 import BeautifulSoup


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


def get_politifact_articles():
    politifact_records = []

    for current_page in range(1, 30):
        url = "https://www.politifact.com/factchecks/list/?page={current_page}&ruling=true".format(
            current_page=current_page)

        print("Processing url {current_url}".format(current_url=url))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for element in soup.find_all('li', 'o-listicle__item'):
            heading_element = element.find('div', 'm-statement__quote')
            article_url = "https://www.politifact.com" + str(heading_element.find('a')['href'])
            politifact_records.append(("Politifact", "True", article_url))

    for current_page in range(1, 30):
        url = "https://www.politifact.com/factchecks/list/?page={current_page}&ruling=mostly-true".format(
            current_page=current_page)

        print("Processing url {current_url}".format(current_url=url))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for element in soup.find_all('li', 'o-listicle__item'):
            heading_element = element.find('div', 'm-statement__quote')
            article_url = "https://www.politifact.com" + str(heading_element.find('a')['href'])
            politifact_records.append(("Politifact", "MostlyTrue", article_url))

    for current_page in range(1, 30):
        url = "https://www.politifact.com/factchecks/list/?page={current_page}&ruling=half-true".format(
            current_page=current_page)

        print("Processing url {current_url}".format(current_url=url))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for element in soup.find_all('li', 'o-listicle__item'):
            heading_element = element.find('div', 'm-statement__quote')
            article_url = "https://www.politifact.com" + str(heading_element.find('a')['href'])
            politifact_records.append(("Politifact", "HalfTrue", article_url))

    for current_page in range(1, 30):
        url = "https://www.politifact.com/factchecks/list/?page={current_page}&ruling=barely-true".format(
            current_page=current_page)

        print("Processing url {current_url}".format(current_url=url))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for element in soup.find_all('li', 'o-listicle__item'):
            heading_element = element.find('div', 'm-statement__quote')
            article_url = "https://www.politifact.com" + str(heading_element.find('a')['href'])
            politifact_records.append(("Politifact", "MostlyFalse", article_url))

    for current_page in range(1, 30):
        url = "https://www.politifact.com/factchecks/list/?page={current_page}&ruling=false".format(
            current_page=current_page)

        print("Processing url {current_url}".format(current_url=url))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for element in soup.find_all('li', 'o-listicle__item'):
            heading_element = element.find('div', 'm-statement__quote')
            article_url = "https://www.politifact.com" + str(heading_element.find('a')['href'])
            politifact_records.append(("Politifact", "False", article_url))

    for current_page in range(1, 30):
        url = "https://www.politifact.com/factchecks/list/?page={current_page}&ruling=pants-fire".format(
            current_page=current_page)

        print("Processing url {current_url}".format(current_url=url))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for element in soup.find_all('li', 'o-listicle__item'):
            heading_element = element.find('div', 'm-statement__quote')
            article_url = "https://www.politifact.com" + str(heading_element.find('a')['href'])
            politifact_records.append(("Politifact", "PantsFire", article_url))

    politifact_records = pd.DataFrame(politifact_records, columns=["Source", "Meter", "URL"])
    politifact_records.to_excel("Politifact_Links.xlsx", index=False)


def process_politifact_site():
    news_articles = pd.read_excel("Politifact_Links.xlsx")
    news_articles_data = []

    for index, row in tqdm(news_articles.iterrows(), total=news_articles.shape[0]):
        try:
            record = parse_article(row["URL"])
            news_articles_data.append([
                row["Source"],
                row["Meter"],
                record["article_title"],
                record["article_published_date"],
                record["article_text"],
                record["article_summary"],
                ",".join(record["article_keywords"]),
                record["article_url"]
            ])
        except Exception as e:
            print(e)

    cnn_news_dataframe = pd.DataFrame(news_articles_data,
                                      columns=[
                                          "Source",
                                          "Meter",
                                          "Title",
                                          "PublishedDate",
                                          "ArticleText",
                                          "Summary",
                                          "Keywords",
                                          "URL"
                                      ])

    cnn_news_dataframe.to_excel("Politifact_Articles.xlsx", index=False)


# get_politifact_articles()
process_politifact_site()
