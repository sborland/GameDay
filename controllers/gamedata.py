# pulls data about games and puts them into the database.

#Key for Game database : https://market.mashape.com/igdbcom/internet-game-database
IGBDkey = "kUe3uZXJcSmshT3CXf5O16Z7DPUjp1n5R0NjsnMr9K0qItyY2Q"

IBGDurl= "https://igdbcom-internet-game-database-v1.p.mashape.com/games/"

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

#Grabs the games that come out that month and year
#Month is a value from 01 to 12 (MUST INCLUDE THE 0 for single digits)
#Year is any valid year value 
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
    resWeekA = ibgdRequestHelper(year+"-"+month+"-01",year+"-"+month+"-10")
    resWeekB = ibgdRequestHelper(year+"-"+month+"-11",year+"-"+month+"-20")
    resWeekC = ibgdRequestHelper(year+"-"+month+"-21",nextYear+"-"+nextMonth+"-01")
    #put all the weeks into a list for easy access
    gameMonth = [resWeekA,resWeekB,resWeekC]
    
    #only grab the release days that lay between the month,
    #this will allow us to compare the pulls
    
    timeStart = year+"-"+month+"-01"
    timeFinish = nextYear+"-"+nextMonth+"-01"
    pattern = '%Y-%m-%d'
    epochStart =  int(time.mktime(time.strptime(timeStart, pattern)))
    epochFinish =  int(time.mktime(time.strptime(timeFinish, pattern)))
    
    
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
    for g in game_list:
        print g
    return response.json(dict(
        game_list=game_list,
    ))

#helper for get_games
def ibgdRequestHelper(date1,date2):
    print IBGDurl+"?fields=name,release_dates&limit=50&filter[release_dates.date][gt]="+date1+"&filter[release_dates.date][lte]="+date2
    response = requests.get(IBGDurl+"?fields=name,release_dates&limit=50&filter[release_dates.date][gt]="+date1+"&filter[release_dates.date][lte]="+date2,
        headers={
            "X-Mashape-Key": IGBDkey,
            "Accept": "application/json"
        }
    )
    return response

#testing
#get_games(11,2016)




