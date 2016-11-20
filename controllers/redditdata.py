import praw

clientID = "PNeNm3DsY_t8-g"
clientSecret = "WPoyJXHV3yB6Ru87UtfOt_IoQwE"
r = praw.Reddit(user_agent='gamedaytest by /u/gamedayadmin',client_id=clientID,
                     client_secret=clientSecret)
submissions = r.get_subreddit('gamernews').get_hot(limit=50)

for x in submissions:
    print (x.title).encode("utf-8")
    print x.url
    print x
    if "thumbnail_url" in x:
        print x["thumbnail_url"]