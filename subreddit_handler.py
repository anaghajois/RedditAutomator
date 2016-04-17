import praw
import csv

def get_redditors(subredditName, app):
    user_agent = "Subreddit parser /u/ramachari"
    r = praw.Reddit(user_agent=user_agent)

    target = subredditName
    subreddit=r.get_subreddit(target)
    redditors = []

    print '*************************************************************************************************'
    subreddit_submissions = subreddit.get_top_from_year(limit = 1000)
    try:
        submissionCount = 0
        for submission in subreddit_submissions:
            redditors.append(str(submission.author))
            commentlist = praw.helpers.flatten_tree(submission.comments)
            for comment in commentlist:
                if hasattr(comment, 'author'):
                     redditors.append(str(comment.author))
            print len(redditors)

            app.update_state(state='PROGRESS',
                              meta={'current': submissionCount , 'total': 1000,
                                    'redditor_count': len(redditors)})
            submissionCount += 1
    except Exception,e:
        print e
    print len(redditors)
    myset =  set(redditors)
    print len(myset)

    myfile = open(subredditName + '.csv', 'w')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(list(myset))

    app.update_state(state='SUCCESS',
                     meta={'current': submissionCount, 'total': 1000,
                           'redditor_count': len(myset)})

    return len(myset)