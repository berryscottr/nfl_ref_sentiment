import codecs

import vaderSentiment.vaderSentiment
import numpy as np
import matplotlib.pyplot as plt
import re
import json
from datetime import datetime, timezone
import time
from scipy.stats import linregress
from collections import defaultdict

sia = vaderSentiment.vaderSentiment.SentimentIntensityAnalyzer()


def remove_noise(tweets):
    cleaned_tweets = []
    ref_tweets_index = []
    i = 0
    link = 0
    for tweet in tweets:
        cleaned_tweet = str(tweet)
        link += cleaned_tweet.count("http")
        cleaned_tweet = re.sub(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|'
            '(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            '',
            cleaned_tweet
        )
        cleaned_tweet = re.sub(
            "(@[A-Za-z0-9_]+)",
            "",
            cleaned_tweet
        )
        cleaned_tweet = re.sub(
            "\[deleted\]",
            "",
            cleaned_tweet
        )
        ref_words = ['ref', 'flag', 'penalty', 'call'] # add types of penalties
        if len(cleaned_tweet) > 0:
            is_ref = [word for word in ref_words if(word in cleaned_tweet)]
            if is_ref:
                ref_tweets_index.append(i)
        cleaned_tweets.append(cleaned_tweet)
        i += 1
    return cleaned_tweets, ref_tweets_index


def plot_fit(
        date_timestamps,
        dates,
        scores,
        title,
        x_label="Unix Time of Comment",
        y_label="Sentiment of Comment"
):
    plt.scatter(
        date_timestamps,
        scores
    )
    plt.plot(
        np.unique(date_timestamps),
        np.poly1d(
            np.polyfit(
                date_timestamps,
                scores,
                1
            )
        )
            (
            np.unique(
                date_timestamps
            )
        ),
        'y->'
    )
    plt.title("Scatter Plot and Linear Regression of " + title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    linear_regression = linregress(date_timestamps, scores)
    return linear_regression


def analyse_comments(
        comment_date_timestamps,
        comment_dates,
        comments,
        ref_indices
):
    neg_score_array = []
    neu_score_array = []
    pos_score_array = []
    compound_score_array = []
    date_timestamp_array = []
    date_array = []
    plot_x = []
    i = 0
    neu = 0

    while i < len(comments):
        if i in ref_indices:
            tweet = comments[i]
            tweet_timestamp_date = comment_date_timestamps[i]
            tweet_date = comment_dates[i]
            score = sia.polarity_scores(tweet)
            neg_score = score['neg']
            neu_score = score['neu']
            pos_score = score['pos']
            compound_score = score['compound']
            if neu_score < 1:
                neg_score_array.append(neg_score)
                neg_score_avg = np.mean(neg_score_array)
                neu_score_array.append(neu_score)
                neu_score_avg = np.mean(neu_score_array)
                pos_score_array.append(pos_score)
                pos_score_avg = np.mean(pos_score_array)
                compound_score_array.append(compound_score)
                compound_score_avg = np.mean(compound_score_array)
                # print(
                #     [
                #         neg_score_avg,
                #         neu_score_avg,
                #         pos_score_avg,
                #         compound_score_avg
                #     ]
                # )
                plot_x.append(i + 1)
                date_timestamp_array.append(tweet_timestamp_date)
                date_array.append(tweet_date)
            else:
                neu += 1
        i += 1

    lin_reg_neg = plot_fit(
        date_timestamp_array,
        date_array,
        neg_score_array,
        "Negative Scores"
    )
    lin_reg_neu = plot_fit(
        date_timestamp_array,
        date_array,
        neu_score_array,
        "Neutral Scores"
    )
    lin_reg_pos = plot_fit(
        date_timestamp_array,
        date_array,
        pos_score_array,
        "Positive Scores"
    )
    lin_reg_compound = plot_fit(
        date_timestamp_array,
        date_array,
        compound_score_array,
        "Compound Scores"
    )
    # print(lin_reg_neg)
    # print(lin_reg_neu)
    # print(lin_reg_pos)
    # print(lin_reg_compound)
    return lin_reg_neg, lin_reg_neu, lin_reg_pos, lin_reg_compound


def json_to_tweets(tweets_json):
    i = 0
    tweet_array = []
    while i < len(tweets_json):
        tweet = tweets_json[i]['body']
        tweet_array.append(tweet)
        i += 1
    return tweet_array


def json_to_dates(tweets_json):
    i = 0
    date_timestamp_array = []
    date_array = []
    while i < len(tweets_json):
        date_timestamp = tweets_json[i]['timestamp']
        date_timestamp_array.append(date_timestamp)
        date = datetime.fromtimestamp(
            date_timestamp / 1000.0,
            tz=timezone.utc
        )
        date_array.append(date)
        i += 1
    return date_timestamp_array, date_array


def real_to_unix(realtime):
    year = 2021
    month = 1
    day = 17
    partitioned_realtime = realtime.partition(':')
    hour = int(partitioned_realtime[0])
    minute = int(partitioned_realtime[-1])
    datetime_real = datetime(year, month, day, hour, minute)
    unixtime = time.mktime(datetime_real.timetuple())
    return unixtime


if __name__ == "__main__":
    # load comments as a variable
    json_file = open(
        'nfl_gamethread_comments_full.json',
        errors="ignore"
    )
    comments_json = json.load(json_file)
    json_file.close()
    # get just the bodies of the tweets, retaining index
    comment_bodies = json_to_tweets(comments_json)
    # get unix timestamps and human readable dates, retaining index
    comment_date_timestamps, comment_dates = json_to_dates(comments_json)
    # remove noise from bodies (i.e. links, usernames)
    # any comments with length zero are then denoted by the null indices
    cleaned_comments, ref_indices = remove_noise(comment_bodies)
    # import csv
    play_by_play = np.genfromtxt('play_by_play.csv', delimiter=',', dtype=str)
    ep_delta_penalties = np.array(play_by_play[1:, 13])
    penalty_index = np.array(play_by_play[1:, 12])
    penalty_realtime = np.array(play_by_play[1:, 14])
    penalty_unixtime = [real_to_unix(x) for x in penalty_realtime]
    # perform sentiment analysis on each body and plot linear regression
    lin_reg_neg, \
    lin_reg_neu, \
    lin_reg_pos, \
    lin_reg_compound = analyse_comments(
        comment_date_timestamps,
        comment_dates,
        cleaned_comments,
        ref_indices
    )
