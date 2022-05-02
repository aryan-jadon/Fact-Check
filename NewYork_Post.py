from newspaper import Article
import pandas as pd
import nltk
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


def get_articles():
    source_article_urls = []
    base_url = "https://nypost.com/2022/"
    for current_month in range(1, 5):
        for current_date in range(1, 32):
            if current_date < 9:
                current_url = base_url + "0" + str(current_month) + "/0" + str(current_date)
            else:
                current_url = base_url + "0" + str(current_month) + "/" + str(current_date)

            print("Processing url {current_url}".format(current_url=current_url))

            page = requests.get(current_url)
            soup = BeautifulSoup(page.text, 'html.parser')

            try:
                for element in soup.find_all('h3', 'story__headline headline headline--archive'):
                    article_url = element.find('a')['href']
                    print(article_url)
                    source_article_urls.append(("NewYorkPost", article_url))
            except Exception as e:
                print(e)

    news_dataframe = pd.DataFrame(source_article_urls, columns=["Source", "NewsLink"])
    news_dataframe.to_excel("NewYorkPost.xlsx", index=False)


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


def process_nypost_site():
    nypost_articles = pd.read_excel("NewYorkPost.xlsx")
    nypost_articles_data = []

    for index, row in tqdm(nypost_articles.head(10000).iterrows(), total=nypost_articles.shape[0]):
        try:
            record = parse_article(row["NewsLink"])
            nypost_articles_data.append([
                "NewYorkPost",
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

    nypost_news_dataframe = pd.DataFrame(nypost_articles_data,
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

    nypost_news_dataframe.to_excel("NewYorkPost_Articles.xlsx", index=False)


process_nypost_site()