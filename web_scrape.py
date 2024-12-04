
from google_play_scraper import reviews
from google_play_scraper import Sort
from google_play_scraper import search


def app_search(app_name, num_results = 5):
    result = search(
        f"{app_name}",
        lang="en",  # defaults to 'en'
        country="us",  # defaults to 'us'
        n_hits=num_results
    )

    return result
