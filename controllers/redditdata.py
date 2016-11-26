
import requests

clientID = "PNeNm3DsY_t8-g"
clientSecret = "WPoyJXHV3yB6Ru87UtfOt_IoQwE"

#gets and cache's gaming news
@cache(request.env.path_info,time_expire=120,cache_model=cache.disk)
def get_gaming_news():
    rep= requests.get("https://www.reddit.com/r/gamernews.json",
             headers = {'user_agent':'gamedaytest by /u/gamedayadmin',
            'client_id':clientID,'client_secret':clientSecret})
    res = rep.json()
    print rep.status_code

    listofNews = []
    rep_code = 'error'
    if rep.status_code==200:
        rep_code = 'ok'
        for item in res['data']['children']:
             if "youtube.com" not in item['data']['domain']:
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
