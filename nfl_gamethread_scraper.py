import praw
import numpy as np
import json
import codecs

if __name__ == "__main__":
    reddit = praw.Reddit(client_id='s0EbXF6ElYxSQA',
                         client_secret='ti5S5SDRDliW2K1jujsI_SCzcAzVcg',
                         user_agent='nflgamethreadscraper by u/scottieburr',
                         # Insert your values here
                         username='user',
                         password='pass')
    # Insert your thread url here
    submission = reddit.submission(url='https://www.reddit.com/r/nfl/comments/kzhfxm/game_thread_tampa_bay_buccaneers_115_at_new/')
    # Uncomment and set number of times the script will load more comments
    # submission.comments.replace_more(limit=1500)
    submission_comments = np.array(submission.comments._comments)
    comments = []
    i = 0
    while i < len(submission_comments):
        try:
            comment = submission_comments[i]
            comment_dict = {k: v for k, v in comment.__dict__.items() if k != '_reddit'}
            comment_dict_reduced = {
                'timestamp': comment_dict['created_utc'],
                'body': comment_dict['body'],
                'flair': comment_dict['author_flair_css_class']
            }
            comment_array = np.asarray(comment_dict_reduced)
            comment_list = comment_array.tolist()
            comments.append(comment_list)
        except:
            pass
        i += 1
    submission_comments_array = np.asarray(comments)
    submission_comments_list = submission_comments_array.tolist()
    json.dump(submission_comments_list, codecs.open('nfl_gamethread_comments.json', 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
