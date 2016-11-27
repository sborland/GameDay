# pulls data about games and puts them into the database.

#Key for Game database : https://market.mashape.com/igdbcom/internet-game-database
IGBDkey = "kUe3uZXJcSmshT3CXf5O16Z7DPUjp1n5R0NjsnMr9K0qItyY2Q"
IBGDurl= "https://igdbcom-internet-game-database-v1.p.mashape.com/"

#URL for images
#tesing: https://res.cloudinary.com/igdb/image/upload/t_cover_big/rm8orl3sh5bf7fe1oqvz.jpg
IBGDimages = "https://res.cloudinary.com/igdb/image/upload/t_"
SIZES ={
'thumb': 'thumb',
'small': 'cover_big',
'med': 'screenshot_med',
'large': 'screenshot_huge'
}

#all videos are from youtube
IBGDvideo = "https://www.youtube.com/embed/"

import requests
import time, datetime,json

#GLOBAL VARIABLES DON'T TOUCH#
MONTHS = {'01' : "January",'02' : "February",'03' : "March",'04' : "April",'06' : "May",'07' : "June",'08' : "July",'09' : "August",'10' : "September",'11' : "November",'12' : "December",
}
PLATFORMS ={
"132" : "Amazon Fire TV", "131" : "Nintendo PlayStation", "130" : "NX", "129" : "Texas Instruments TI-99", "128" : "PC Engine SuperGrafx", "127" : "Fairchild Channel F", "126" : "TRS-80", "125" : "PC-8801", "124" : "SwanCrystal", "123" : "WonderSwan Color", "122" : "Nuon", "121" : "Sharp X68000", "120" : "Neo Geo Pocket Color", "119" : "Neo Geo Pocket", "118" : "FM Towns", "117" : "Philips CD-i", "116" : "Acorn Archimedes", "115" : "Apple IIGS", "114" : "Amiga CD32", "113" : "OnLive Game System", "112" : "Microcomputer", "111" : "Imlac PDS-1", "110" : "PLATO", "109" : "CDC Cyber 70", "108" : "PDP-11", "107" : "Call-A-Computer time-shared mainframe computer system", "106" : "SDS Sigma 7", "105" : "HP 3000", "104" : "HP 2100", "103" : "PDP-7", "102" : "EDSAC", "101" : "Ferranti Nimrod Computer", "100" : "Analogue electronics", "99" : "Family Computer", "98" : "DEC GT40", "97" : "PDP-8", "96" : "PDP-10", "95" : "PDP-1", "94" : "Commodore Plus/4", "93" : "Commodore 16", "92" : "SteamOS", "91" : "Bally Astrocade", "90" : "Commodore PET", "89" : "Microvision", "88" : "Odyssey", "87" : "Virtual Boy", "86" : "TurboGrafx-16/PC Engine", "85" : "Donner Model 30", "84" : "SG-1000", "82" : "Web browser", "80" : "Neo Geo AES", "79" : "Neo Geo MVS", "78" : "Sega CD", "77" : "Sharp X1", "75" : "Apple II", "74" : "Windows Phone", "73" : "BlackBerry OS", "72" : "Ouya", "71" : "Commodore VIC-20", "70" : "Vectrex", "69" : "BBC Microcomputer System", "68" : "ColecoVision", "67" : "Intellivision", "66" : "Atari 5200", "65" : "Atari 8-bit", "64" : "Sega Master System", "63" : "Atari ST/STE", "62" : "Atari Jaguar", "61" : "Atari Lynx", "60" : "Atari 7800", "59" : "Atari 2600", "58" : "Super Famicom", "57" : "WonderSwan", "56" : "WiiWare", "55" : "Mobile", "53" : "MSX2", "52" : "Arcade", "51" : "Family Computer Disk System", "50" : "3DO Interactive Multiplayer", "49" : "Xbox One", "48" : "PlayStation 4", "47" : "Virtual Console (Nintendo)", "46" : "PlayStation Vita", "45" : "PlayStation Network", "44" : "Tapwave Zodiac", "42" : "N-Gage", "41" : "Wii U", "39" : "iOS", "38" : "PlayStation Portable", "37" : "Nintendo 3DS", "36" : "Xbox Live Arcade", "35" : "Sega Game Gear", "34" : "Android", "33" : "Game Boy", "32" : "Sega Saturn", "30" : "Sega 32X", "29" : "Sega Mega Drive/Genesis", "27" : "MSX", "26" : "ZX Spectrum", "25" : "Amstrad CPC", "24" : "Game Boy Advance", "23" : "Dreamcast", "22" : "Game Boy Color", "21" : "Nintendo GameCube", "20" : "Nintendo DS", "19" : "Super Nintendo Entertainment System (SNES)", "18" : "Nintendo Entertainment System (NES)", "16" : "Amiga", "15" : "Commodore C64/128", "14" : "Mac", "13" : "PC DOS", "12" : "Xbox 360", "11" : "Xbox", "9" : "PlayStation 3", "8" : "PlayStation 2", "7" : "PlayStation", "6" : "PC (Microsoft Windows)", "5" : "Wii", "4" : "Nintendo 64", "3" : "Linux",    
}
REGIONS = {
"8":"World Wide", "1":"Europe","2":"North America", "3":"Australia", "4":"New Zealand","5":"Japan","6":"China","7":"Asia"
}
THEMES = {"1" : "Action", "17" : "Fantasy", "18" : "Science Fiction", "19" : "Horror", "20" : "Thriller", "21" : "Survival", "22" : "Historical", "23" : "Stealth", "27" : "Comedy", "28" : "Business", "31" : "Drama", "32" : "Non-fiction", "33" : "Sandbox", "34" : "Educational", "35" : "Kids", "38" : "Open World", "39" : "Warfare", "40" : "Party", "41" : "Explore", "42" : "Erotic", "43" : "Mystery"
}
GENRES = {"2" : "Point-and-click", "4" : "Fighting", "5" : "Shooter", "7" : "Music", "8" : "Platform", "9" : "Puzzle", "10" : "Racing", "11" : "Real Time Strategy (RTS)", "12" : "Role-playing (RPG)", "13" : "Simulator", "14" : "Sport", "15" : "Strategy", "16" : "Turn-based strategy (TBS)", "24" : "Tactical", "25" : "Hack and Slash/Beat 'em up", "26" : "Quiz/Trivia", "30" : "Pinball", "31" : "Adventure", "32" : "Indie", "33" : "Arcade"
}
GAMEMODES ={ "1":"Single Player", "2":"Multiplayer", "3":"Co-operative", "4":"Split Screen", "5":"MMO"
}


#Grabs the games that come out that month and year
#Month is a value from 01 to 12 (MUST INCLUDE THE 0 for single digits)
#Year is any valid year value
@cache(request.env.path_info,time_expire=15,cache_model=cache.disk)
def get_games():
    month = int(request.vars.month)
    print request.vars.year
    year = int(request.vars.year)

    #handles Dec-Jan case where
    #December overlaps with January
    nextMonth=month+1
    nextYear = year
    if (month==12):
        nextMonth = "01"
        nextYear = year+1
    month = str(month)
    year = str(year)
    nextMonth = str(nextMonth)
    nextYear = str(nextYear)
    
    game_list=[]
    
    #Because we are only allowed to pull 50 objects per request, I split up
    #the month into thirds to cover all the possible days of the month for new
    #releases.
    resWeekA = get_gamesHelper(year+"-"+month+"-01",year+"-"+month+"-10")
    resWeekB = get_gamesHelper(year+"-"+month+"-11",year+"-"+month+"-20")
    resWeekC = get_gamesHelper(year+"-"+month+"-21",nextYear+"-"+nextMonth+"-01")
    #put all the weeks into a list for easy access
    gameMonth = [resWeekA,resWeekB,resWeekC]
    
    #only grab the release days that lay between the month,
    #this will allow us to compare the pulls
    
    timeStart = year+"-"+month+"-01"
    timeFinish = nextYear+"-"+nextMonth+"-01"
    pattern = '%Y-%m-%d'
    epochStart =  int(time.mktime(time.strptime(timeStart, pattern)))
    epochFinish =  int(time.mktime(time.strptime(timeFinish, pattern)))
    
    requestStatus = "OK"
    
    #Pulling current user's email so we can pull their list of games
    #Empty list if the user is not logged in
    logged_in = auth.user_id is not None
    user_games_dict = None
    if logged_in: 
        curuser_email = db(db.auth_user.id==auth.user_id).select().first().email
        user_games_pull = db(db.user_games_list.user_id==curuser_email).select().first()
        #If new user, create a record for them in the table...
        if user_games_pull==None:
            db.user_games_list.insert(user_id = curuser_email,games_list_json = {},)
        else: #else set their record as the list of games to check
            user_games_dict =user_games_pull['games_list_json']
    else:
        curuser_email = None

   
    print curuser_email
    #TODO: Throwing an error for a bad status code
    if((resWeekA.status_code==200) and (resWeekB.status_code==200) and (resWeekC.status_code==200)):
        #go through each week...
        for week in gameMonth:
            weekResponse = week.json()
            for gameData in weekResponse:
                #get the game's name/id 
                #and check if it's in the user's list. If it is,
                #set user_game attr to 'minus', else set it to 'plus'.
                #if not logged in, set it to 'null'
                if curuser_email is not None:
                    game_in_user_list='plus'
                    if user_games_dict is not None:
                        if str(gameData['id']) in user_games_dict:
                            game_in_user_list = 'minus'
                else:
                    game_in_user_list = 'null'
                
                game = dict(
                    name = gameData['name'].encode("utf-8"),
                    id = gameData['id'],
                    game_in_list = game_in_user_list,
                    release = []
                )
                #the game's release date is divided up by information on
                #region, platform and date. Region & Platform is added to global_variables
                #See https://market.mashape.com/igdbcom/internet-game-database/overview
                for releaseData in gameData['release_dates']:
                    s = int(releaseData['date'])/1000.0
                    realDate = datetime.datetime.fromtimestamp(s).strftime('%d-%m-%Y.%f')
                    #Only grab the relevant release dates
                    if (s>=epochStart) and (s<epochFinish):
                        gameRelease = dict(
                            date = realDate,
                            #get the platform name
                            platform = PLATFORMS[str(releaseData['platform'])],
                            region = "World Wide"
                        )
                        if 'region' in releaseData:
                            gameRelease['region']= REGIONS[str(releaseData['region'])]
                        game['release'].append(gameRelease)
                game_list.append(game)
    else:
        StatusRequest = "ERROR"
        
   # for g in game_list:
    #    print g
    
    return response.json(dict(
        game_list=game_list,
    ))

#helper for get_games - pulls all the games that are going to be released between two dates
def get_gamesHelper(date1,date2):
    #print IBGDurl+"?fields=name,release_dates&limit=50&filter[release_dates.date][gt]="+date1+"&filter[release_dates.date][lte]="+date2
    response = requests.get(IBGDurl+"games/?fields=name,release_dates&limit=50&filter[release_dates.date][gt]="+date1+"&filter[release_dates.date][lte]="+date2,
        headers={
            "X-Mashape-Key": IGBDkey,
            "Accept": "application/json"
        }
    )
    return response

    
#gets a single game's data using it's ID
#@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def get_game_data():
    id = str(request.vars.id)
    
    rep= requests.get(IBGDurl+"games/"+id+"/?fields=name,summary,storyline,publishers,developers,release_dates,screenshots,cover,videos,themes,game_modes",
        headers={
            "X-Mashape-Key": IGBDkey,
            "Accept": "application/json"
        }
    )
    
    responseStatus = "OK"
    
    
    #pulls user's list of games
    logged_in = auth.user_id is not None
    user_games_dict = None
    if logged_in: 
        curuser_email = db(db.auth_user.id==auth.user_id).select().first().email
        user_games_pull = db(db.user_games_list.user_id==curuser_email).select().first()
        #If new user, create a record for them in the table...
        if user_games_pull==None:
            db.user_games_list.insert(user_id = curuser_email,games_list_json = {},)
            
        else: #else set their record as the list of games to check
            user_games_dict =user_games_pull['games_list_json']
    else:
        curuser_email = None
    
   
    
     #returning a dictionary representation of
     #the game's data.
    game_data = dict(
            name = "Game Name",
            id = "0",
            storyline = "Game Storyline not available.",
            summary = "Game Summary not available.",
            publishers=[],
            developers=[],
            videos=[],
            screenshots = [],
            release = [],
            themes =[],
            gameModes = [],
            game_in_list = 'null',
            #TODO: replace temp cover not found image
            coverThumb = "https://www.naplesgarden.org/wp-content/themes/naples_botanical/img/notfound.jpg",
            coverReg = "https://www.naplesgarden.org/wp-content/themes/naples_botanical/img/notfound.jpg"
         ) 
    print rep.status_code
 
 
    if (rep.status_code==200):
        
         res = rep.json()[0]
         
         game_data["name"] = res['name'].encode("utf-8")
         game_data['id'] =res['id'] 
         print "LOOOOOOOOOK AT ME"
         print game_data['id'] 
         #checks whether the game is in the user's list or not
         if curuser_email is not None:
            game_data['game_in_list']='plus'
            if user_games_dict is not None:
                if str(res['id']) in user_games_dict:
                    game_data['game_in_list'] = 'minus'
         
         #pulls game's list of likes/game postings
         game_db_pull = db(db.games.game_id==game_data['id']).select().first()
         game_likes = []
         #game_postings = []
            #If game is newly selected, create a record for them in the game table...
         if game_db_pull==None:
              db.games.insert(game_id = game_data['id'],game_likes_json = [],game_postings_json=[])
            
         else: #else pull the list of games and postings
              game_likes = game_db_pull['game_likes_json']
                #game_postings = game_db_pull['game_postings_json']
         game_data['game_likes']= len(game_likes)
         
         
         if "summary" in res:
            game_data["summary"]= res["summary"].encode("utf-8")
        
         if "storyline" in res:
            game_data["storyline"] = res["storyline"].encode("utf-8")
         if "cover" in res:
            game_data['coverThumb'] = IBGDimages+SIZES['thumb']+"/"+res['cover']["cloudinary_id"]+".jpg"
            game_data['coverReg'] = IBGDimages+SIZES['small']+"/"+res['cover']["cloudinary_id"]+".jpg"
         
         #gets publishers and developers for the game
         if "publishers" in res:
            pub = get_game_dataHelper(res["publishers"])
            if pub is not None:
                game_data["publishers"] = pub
                
         if "developers" in res:
            dev = get_game_dataHelper(res["developers"])
            if dev is not None:
                game_data["developers"] = dev
        
         if "videos" in res:
            for video in res["videos"]:
                vid = dict(
                    vidURL = IBGDvideo+video['video_id'],
                    vidName = video['name'],
                )
                game_data["videos"].append(vid)
                
         if "screenshots" in res:   
            for screenshot in res["screenshots"]:
                img = dict(
                    imgSmallURL = IBGDimages+SIZES['small']+"/"+screenshot["cloudinary_id"]+".jpg",
                    imgMediumURL = IBGDimages+SIZES['med']+"/"+screenshot["cloudinary_id"]+".jpg",
                    imgLargeURL = IBGDimages+SIZES['large']+"/"+screenshot["cloudinary_id"]+".jpg",
                )
                game_data["screenshots"].append(img)
            
         for releaseData in res['release_dates']:
             s = int(releaseData['date'])/1000.0
             realDate = datetime.datetime.fromtimestamp(s).strftime('%d-%m-%Y.%f')
             gameRelease = dict(
                   date = realDate,
                   #get the platform name
                   platform = PLATFORMS[str(releaseData['platform'])],
                   region = "World Wide"
                   )
             if 'region' in releaseData:
                   gameRelease['region']= REGIONS[str(releaseData['region'])]
             game_data["release"].append(gameRelease)   
        
         if "themes" in res: 
            for theme in res["themes"]:
                if THEMES[str(theme)] is not None:
                    game_data["themes"].append(THEMES[str(theme)])
         if "game_modes" in res: 
            for gameMode in res["game_modes"]:
                if GAMEMODES[str(gameMode)] is not None:
                    game_data["gameModes"].append(GAMEMODES[str(gameMode)])
            
    else:
        responseStatus = "ERROR"

    #print game_data
    return response.json(dict(game_data=game_data))
        
        
        
#gets a developer/publisher name using id    
#@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def get_game_dataHelper(listIDs):
    sID = ""
    sIDlen = len(listIDs)
    for id in listIDs:
        if sIDlen >1:
            sID = sID+str(id)+','
            sIDlen=sIDlen-1
        else:
            sID = sID+str(id)
        
    response = requests.get(IBGDurl+"companies/"+sID+"/?fields=name",
        headers={
            "X-Mashape-Key": IGBDkey,
            "Accept": "application/json"
        }
    )
    if (response.status_code==200):
        res = response.json()
        returnList = []
        for r in res:
            returnList.append(r["name"])
        return returnList
    else:
        return None


#################Database user's game list functions###############################################


#given an id, adds a game to user's list
def add_game_to_userlist():
    print request.vars.id
    game_id=request.vars.id
    game_name=request.vars.name
    game_thumbnail=request.vars.thumb
    #grabs user's email, the user's game list and database entry
    curuser_email = db(db.auth_user.id==auth.user_id).select().first().email
    user_games_dict = json.loads(db(db.user_games_list.user_id==curuser_email).select().first().games_list_json)
    game_userlist_entry = db(db.user_games_list.user_id==curuser_email).select().first()

   #creates dictionary for game info and adds game to user's list and updates database entry
    #game_list_json -> key: game_id | value: {name, thumbnail}
    add_game_dict = { 'name':game_name, 'thumbnail':game_thumbnail }
    user_games_dict[game_id] = add_game_dict
    game_userlist_entry.games_list_json = json.dumps(user_games_dict)
    game_userlist_entry.update_record()
    
    #Gets the game's list of users that added the game to their list.
    #appends the user's email to the list and returns 
    game_likes = db(db.games.game_id==game_id).select().first().game_likes_json
    game_db_entry = db(db.games.game_id==game_id).select().first()
    game_likes.append(curuser_email)
    game_db_entry.game_likes_json = game_likes
    game_db_entry.update_record()
    like_count = len(game_likes)
    
    
    game_list = user_games_list_helper(user_games_dict)
    return response.json(dict(game_list=game_list,user_id=curuser_email,game_likes=like_count))
 

#given an id, removes a game from user's list  
def rem_game_from_userlist():
    print request.vars.id
    game_id=request.vars.id
    #grabs user's email, the user's game list and database entry
    curuser_email = db(db.auth_user.id==auth.user_id).select().first().email
    user_games_dict = json.loads(db(db.user_games_list.user_id==curuser_email).select().first().games_list_json)
    game_list_entry = db(db.user_games_list.user_id==curuser_email).select().first()

    #delete's game from user's list and updates database entry
    del user_games_dict[game_id]
    game_list_entry.games_list_json = json.dumps(user_games_dict)
    game_list_entry.update_record()
    
    #Gets the game's list of users that added the game to their list.
    #remove user's email from the game's list
    game_likes = db(db.games.game_id==game_id).select().first().game_likes_json
    game_db_entry = db(db.games.game_id==game_id).select().first()
    game_likes.remove(curuser_email)
    game_db_entry.game_likes_json = game_likes
    game_db_entry.update_record()
    like_count = len(game_likes)
    
    
    game_list = user_games_list_helper(user_games_dict)
    return response.json(dict(game_list=game_list,user_id=curuser_email,game_likes=like_count))


#returns a list of the user's games
def get_games_from_userlist():
    logged_in = auth.user_id is not None
    user_games_dict = {}
    curuser_email = 'null'
    if logged_in: 
        curuser_email = db(db.auth_user.id==auth.user_id).select().first().email
        user_games_pull = db(db.user_games_list.user_id==curuser_email).select().first()
        #If new user, create a record for them in the table...
        if user_games_pull==None:
            db.user_games_list.insert(user_id = curuser_email,games_list_json = {},)
        else: #else set their record as the list of games
            user_games_dict =  json.loads(db(db.user_games_list.user_id==curuser_email).select().first().games_list_json)
    
    game_list = user_games_list_helper(user_games_dict)
    return response.json(dict(game_list=game_list,user_id=curuser_email))

def user_games_list_helper(user_games_dict):
    #not the most optimal solution, but works for now.
    game_list = []
    
    for key in user_games_dict.keys():
        data = {}
        data['thumb']=user_games_dict[key]['thumbnail']
        data['name']=(user_games_dict[key]['name'])
        data['id']=key
        game_list.append(data)
    #game_list = sorted(game_list, key = lambda k: k['name'])
    return game_list

    
    
#testing
#get_games(11,2016)
#get_game_data('359')





