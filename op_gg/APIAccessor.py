
from op_gg import apikey
import requests
from op_gg.APIAccessorExceptions import  InvalidAPiKeyException, InvalidSummonerNameException







def returnTFTStats(responseJSON):
    ranked5tier = Get_anything(responseJSON, 'tier', rankedtfttype)
    ranked5division = Get_anything(responseJSON, 'rank', rankedtfttype)
    ranked5lp = Get_anything(responseJSON, 'leaguePoints', rankedtfttype)
    ranked5squeuewins = Get_anything(responseJSON, 'wins', rankedtfttype)
    ranked5squeuelosses = Get_anything(responseJSON, 'losses', rankedtfttype)
    ranked5squeuepercentage = ranked5squeuewins / (ranked5squeuewins + ranked5squeuelosses)
    ranked5squeuepercentage = round(ranked5squeuepercentage, 2) * 100
    return [ranked5tier, ranked5division, ranked5lp, ranked5squeuewins, ranked5squeuelosses, ranked5squeuepercentage]



def returnStats(responseJSON,queueType):
    tier = Get_anything(responseJSON,'tier',queueType)
    if(tier == None):
        return 'Unranked'
    division = Get_anything(responseJSON,'rank',queueType)
    lp = Get_anything(responseJSON,'leaguePoints',queueType)
    wins = Get_anything(responseJSON, 'wins', queueType)
    losses = Get_anything(responseJSON, 'losses', queueType)
    queuewinpercentage = wins / (losses + wins)
    queuewinpercentage = round(queuewinpercentage, 2)*100
    return [tier,division,lp,wins,losses,queuewinpercentage]


def getsummonerid(responseJSON):
    ID = responseJSON.get("id")
    print(responseJSON)
    if(ID == None):
        if responseJSON is not None:
            status = responseJSON.get('status')
            statuscode = status.get('status_code')
            print(statuscode)
            if(statuscode == 403):
                raise InvalidAPiKeyException('Invalid API Key, please change API Key!')
            elif(statuscode == 404):
                raise InvalidSummonerNameException('Invalid Summoner name, please change region, or check spelling')



    ID = str(ID)
    return ID


rankedsoloqueuetype = 'RANKED_SOLO_5x5'
ranked5squeuetype = 'RANKED_FLEX_SR'
rankedTwistedtreelinetype = 'RANKED_FLEX_TT'
rankedtfttype = 'RANKED_TFT'



def getstats(region,filename, playername):

        values = []
        x = 1
        responseJSON = requestSummonerData(region, playername, apikey)
        try:
            summonerid = getsummonerid(responseJSON)
        except InvalidAPiKeyException:
            raise
        except InvalidSummonerNameException:
            raise
        responseJSON = requestRankedData(region, summonerid, apikey)
        values.append(returnStats(responseJSON,rankedsoloqueuetype))
        values.append(returnStats(responseJSON,ranked5squeuetype))
        values.append(playername)

        values.append(returnStats(responseJSON,rankedTwistedtreelinetype))
        values.append(returnStats(responseJSON,rankedtfttype))

        return values



def Get_anything(responseJSON,key,queuetype):
    for i in responseJSON:
        if i.get('queueType') == queuetype:
            return i.get(key)
    return None







def requestSummonerData(region, summonerName, APIKey):


    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    print ('URL')
    response = requests.get(URL)
    return response.json()


def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + "?api_key=" + APIKey
    print ('URL')
    response = requests.get(URL)
    return response.json()

def requestLiveGameData(region,ID,APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/active-games/by-summoner/" + ID + "?api_key=" + APIKey
    print('URL')
    response = requests.get(URL)
    return response.json()