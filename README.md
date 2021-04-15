# NFL Ref Sentiment Analysis
Analyze Reddit threads for how win percentage delta affects sentiment directed towards refs

@Nick Edit the paper proposal at the Google Docs link https://docs.google.com/document/d/1SghkqW9KjwRPjkTqzbE5PwmLbw2UXThVHGgy6L6pziQ/edit

Gather comments from any Reddit thread by utilizing the `nfl_gamethread_scraper.py` script

Place personal credentials into the `praw.Reddit` object and the thread url into the `submission` object.

Uncomment the `replace_more` line to indicate how many times the script will expand the comment selection (None is ideal but has caused timeout errors for me)

Modify `comment_dict_reduced` to filter out only the metadata from the reddit comments that you want. 
I recommend taking a small sample of comments so that you can observe the structure of the comment dict and parse accordingly.
It is contained inside a `praw.reddit.Reddit` object. A Python Console is necessary to view this easily.


Also, Reddit rate limits us. Expect 10k comments to take about an hour. Run the script and go watch a movie or something. 

`nfl_gamethread_sentiment_analysis.py` is currently basically copied from another project and has lots of editing to do don't look too much into that yet.
