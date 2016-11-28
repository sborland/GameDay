'''import praw

clientID = "PNeNm3DsY_t8-g"
clientSecret = "WPoyJXHV3yB6Ru87UtfOt_IoQwE"
r = praw.Reddit(user_agent='gamedaytest by /u/gamedayadmin',client_id=clientID,
                     client_secret=clientSecret)
submissions = r.get_subreddit('gamernews').get_hot(limit=15)

for x in submissions:
    print (x.title).encode("utf-8")
    print x.url
    print x
    print x.selftext_html
    #if "thumbnail_url" in x:
    #    print x["thumbnail_url"]
print str(submissions)'''

import requests

clientID = "PNeNm3DsY_t8-g"
clientSecret = "WPoyJXHV3yB6Ru87UtfOt_IoQwE"

@cache(request.env.path_info,time_expire=120,cache_model=cache.ram)
def get_gaming_news():
    rep= requests.get("https://www.reddit.com/r/gamers.json",
             headers = {'user_agent':'gamedaytest by /u/gamedayadmin', })
    res = rep.json()
    print rep.status_code

    listofNews = []
    rep_code = "error"
    if rep.status_code==200:
        rep_code = "ok"
        for item in res['data']['children']:
             if "youtube.com" not in item['data']['domain']:
                # print item['data']['title'].encode("utf-8")
                # print str(item['data']['url'])
                # print "SCORE" + str(item['data']['score'])
                if "preview" in item['data']:
                    story = {}
                    story['title'] = item['data']['title'].encode("utf-8")
                    story['url']=str(item['data']['url'])
                    story['score']=int(item['data']['score'])
                    story['preview']=str(item['data']['preview']['images'][0]['source']['url'])
                    listofNews.append(story)
        listofNews = sorted(listofNews, key = lambda k: k['score'])
        listofNews.reverse()
        listofNews = listofNews[:5]
        for item in listofNews:
            print item['score']
            print item['title']
    return response.json(dict(
        listofNews=listofNews,
        responseStatus = rep_code,
    ))   

