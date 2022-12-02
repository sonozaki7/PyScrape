# blog post: https://serpapi.com/blog/scrape-google-scholar-metrics-results-to-csv-with-python/#top_publications

import requests, lxml
from bs4 import BeautifulSoup
import pandas as pd


def scrape_all_metrics_top_publications():

    params = {
        "view_op": "top_venues",  # top publications results
        "hl": "en"  # or other lang: pt, sp, de, ru, fr, ja, ko, pl, uk, id
        }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    # whatismybrowser.com/detect/what-is-my-user-agent
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Safari/537.36"
        }

    html = requests.get("https://scholar.google.com/citations", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml").find("table")

    df = pd.DataFrame(pd.read_html(str(soup))[0])
    df.drop(df.columns[0], axis=1, inplace=True)
    df.insert(loc=2,
              column="h5-index link",
              value=[f'https://scholar.google.com/{link.a["href"]}' for link in soup.select(".gsc_mvt_t+ td")])

    df.to_csv("google_scholar_metrics_top_publications.csv", index=False)

    # save to csv for specific language
    # df.to_csv(f"google_scholar_metrics_top_publications_lang_{params['hl']}.csv", index=False)

scrape_all_metrics_top_publications()
