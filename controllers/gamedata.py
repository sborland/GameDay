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
import time, datetime

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
@cache(request.env.path_info,time_expire=30,cache_model=cache.disk)
def get_games():
    month = int(request.vars.month)
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
    
    #TODO: Throwing an error for a bad status code
    if((resWeekA.status_code==200) and (resWeekB.status_code==200) and (resWeekC.status_code==200)):
        #go through each week...
        for week in gameMonth:
            weekResponse = week.json()
            for gameData in weekResponse:
                #get the game's name and id
                game = dict(
                    name = gameData['name'].encode("utf-8"),
                    id = gameData['id'],
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
            #TODO: replace temp cover not found image
            coverThumb = "https://www.naplesgarden.org/wp-content/themes/naples_botanical/img/notfound.jpg",
            coverReg = "https://www.naplesgarden.org/wp-content/themes/naples_botanical/img/notfound.jpg"
         ) 
    print rep.status_code
 
    if (rep.status_code==200):
         res = rep.json()[0]
         
         #print res 
         game_data["name"] = res['name'].encode("utf-8")
         game_data['id'] =res['id']
         
         
         if "summary" in res:
            game_data["summary"]= res["summary"].encode("utf-8")
         
        # print "summary"
         
         
         if "storyline" in res:
            game_data["storyline"] = res["storyline"].encode("utf-8")
         
        # print "storyline"
         
         if "cover" in res:
            game_data['coverThumb'] = IBGDimages+SIZES['thumb']+"/"+res['cover']["cloudinary_id"]+".jpg"
            game_data['coverReg'] = IBGDimages+SIZES['small']+"/"+res['cover']["cloudinary_id"]+".jpg"
         
         
        # print "cover"
         
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





    
    
#testing
#get_games(11,2016)
#get_game_data('359')





