# NFL Ref Sentiment Analysis
Analyze Reddit threads for how win percentage delta affects sentiment directed towards refs

Gather comments from any Reddit thread by utilizing the `nfl_gamethread_scraper.py` script

Place personal credentials into the `praw.Reddit` object and the thread url into the `submission` object.

Uncomment the `replace_more` line to indicate how many times the script will expand the comment selection (None is ideal but has caused timeout errors for me)

Modify `comment_dict_reduced` to filter out only the metadata from the reddit comments that you want. 
I recommend taking a small sample of comments so that you can observe the structure of the comment dict and parse accordingly.
It is contained inside a `praw.reddit.Reddit` object. A Python Console is necessary to view this easily.


Also, Reddit rate limits us. Expect 10k comments to take about an hour. Run the script and go watch a movie or something. 

The above has been completed as shown in `nfl_gamethread_comments.json`

`nfl_gamethread_sentiment_analysis.py` is currently basically copied from another project and has lots of editing. 
The parsing of data in the method should be sufficient. 

What we will need to work on is the data analysis function to match the requirements as detailed in `paper2Proposal.pdf`
