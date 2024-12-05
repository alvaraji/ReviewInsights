import pandas as pd
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
from transformers import pipeline
import os
from initial_config import run_config

if os.path.isfile("initial.txt"):
    pass
else:
    run_config()

def summarize(comments, amount = 10):
    interest_str = ""

    for index, review in comments.head(15).iterrows():
        interest_str = interest_str + review['content'] + " "

    interest_str = interest_str.strip()

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    output = summarizer(interest_str, max_length=90, min_length=30, do_sample=True)

    return output[0]['summary_text']

#All code below is code modified from Kaggle Jupyter Notebook found at link below:
# Mulla, R. (2022, May 5). Sentiment Analysis Python 🤗 [youtube tutorial]. Kaggle. 
# https://www.kaggle.com/code/robikscube/sentiment-analysis-python-youtube-tutorial 


def analyze(df):

    sia = SentimentIntensityAnalyzer()

    res = {}

    for i, row in tqdm(df.iterrows(), total=len(df)):
        text = row['content']
        myid = row['reviewId']
        res[myid] = sia.polarity_scores(text)
    
    vaders = pd.DataFrame(res).T

    # Drop the existing 'reviewId' column if it exists
    if 'reviewId' in vaders.columns:
        vaders = vaders.drop(columns=['reviewId'])
    # Now, reset the index and rename it to 'reviewId'
    vaders = vaders.reset_index().rename(columns={'index': 'reviewId'})
    # Proceed with the merge
    vaders = vaders.merge(df, on='reviewId', how='left')

    # Now we have sentiment score and metadata
    return vaders

def good_bad_interst_split(vaders):
    bad_reviews = vaders.query('score == 1').sort_values('neg', ascending=False)
    bad_reviews = bad_reviews[bad_reviews['content'].apply(len) > 30]

    good_reviews = vaders.sort_values('pos', ascending=False)
    good_reviews = good_reviews[good_reviews['content'].apply(len) > 30]

    interest_good = vaders.query('score == 5').sort_values('neg', ascending=False)
    interest_bad = vaders.query('score == 1').sort_values('pos', ascending=False)
    interesting_reviews = pd.merge(interest_good.head(), interest_bad.head(), how='outer')

    return (good_reviews, bad_reviews, interesting_reviews)






    