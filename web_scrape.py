
from google_play_scraper import reviews
from google_play_scraper import Sort
from google_play_scraper import search
import pandas as pd

#Code Modified from Kaggle Jupyter Notebook found below:
# Hasija , S. (2021, July 16). Play store app reviews scrapper (daily update). Kaggle. 
# https://www.kaggle.com/code/odins0n/play-store-app-reviews-scrapper-daily-update  

def app_search(app_name, num_results = 5):
    result = search(
        f"{app_name}",
        lang="en",  # defaults to 'en'
        country="us",  # defaults to 'us'
        n_hits=num_results
    )

    return result

def get_reviews(app_name, app_id):

    apps = {
    f"{app_name}": f"{app_id}",
    }

    SORT = Sort.NEWEST
    N_REVIEWS = 1000
    reviews_dict =  {k : {} for k in apps}

    ## Scraping reviews
    for app in apps.keys():
        reviews_dict[app], _  = reviews(
            apps[app],
            lang='en',
            country='us',
            sort= SORT,
            count=N_REVIEWS,
            filter_score_with=None
        )
        assert len(reviews_dict[app]) == N_REVIEWS

    df = pd.DataFrame()
    for app in apps.keys():
        temp_df = pd.DataFrame(
            reviews_dict[app],
            columns = ["reviewId", "content", "score"]
                            )
        temp_df["app"] = app
        df = pd.concat((df ,temp_df))
    
    return df