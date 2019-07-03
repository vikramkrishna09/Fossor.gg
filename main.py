from flask import Flask, render_template,url_for,redirect
import requests
from forms import SearchForm

app = Flask(__name__)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
apikey = "RGAPI-c10f5c78-9ffa-4a58-93a3-97f1519420f3"
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route("/home#", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        print(requestSummonerData("na1",form.playername.data,apikey))
        print('this has been reached')
        return redirect(url_for('home'))

    return render_template('home.html',form=form)





def getsolorankedtier(responseJSON):
    if responseJSON[0]['queueType']== 'RANKED_SOLO_5x5':
        return responseJSON[0]['tier']
    else:
        if responseJSON[0]['queueType'] == 'RANKED_FLEX_SR' and len(responseJSON) == 1:
            return 'Unranked'
        else:
            return responseJSON[1]['tier']

def getsolorankeddivision(responseJSON):
    if (responseJSON[0]['queueType'] == 'RANKED_SOLO_5x5'):
        return responseJSON[0]['rank']
    else:
        return responseJSON[1]['rank']

def getsolorankedleaguepoints(responseJSON):
    if (responseJSON[0]['queueType'] == 'RANKED_SOLO_5x5'):
        return responseJSON[0]['leaguePoints']
    else:
        return responseJSON[1]['leaguePoints']


def getsummonerid(responseJSON):
    ID = responseJSON["id"];
    ID = str(ID)
    return ID


def returnSoloqueuestats(responseJSON):
    tier = getsolorankedtier(responseJSON)
    division = getsolorankeddivision(responseJSON)
    lp = getsolorankedleaguepoints(responseJSON)
    soloqueuewins = getanything(responseJSON, 'wins', rankedsoloqueuetype)
    soloqueuelosses = getanything(responseJSON, 'losses', rankedsoloqueuetype)
    soloqueuewinpercentage = soloqueuewins / (soloqueuelosses + soloqueuewins)
    soloqueuewinpercentage = round(soloqueuewinpercentage, 2)*100
    return [tier,division,lp,soloqueuewins,soloqueuelosses,soloqueuewinpercentage]


def returnRanked5sstats(responseJSON):
    ranked5tier = getanything(responseJSON, 'tier', ranked5squeuetype)
    ranked5division = getanything(responseJSON, 'rank', ranked5squeuetype)
    ranked5lp = getanything(responseJSON, 'leaguePoints', ranked5squeuetype)
    ranked5squeuewins = getanything(responseJSON, 'wins', ranked5squeuetype)
    ranked5squeuelosses = getanything(responseJSON, 'losses', ranked5squeuetype)
    ranked5squeuepercentage = ranked5squeuewins / (ranked5squeuewins + ranked5squeuelosses)
    ranked5squeuepercentage = round(ranked5squeuepercentage, 2)*100
    return [ranked5tier,ranked5division,ranked5lp,ranked5squeuewins,ranked5squeuelosses,ranked5squeuepercentage]



def getstats(region,filename):
    form = SearchForm()
    values = []
    if form.validate_on_submit():
        responseJSON = requestSummonerData(region, form.playername.data, apikey)
        playername = form.playername.data
        print (responseJSON)
        summonerid = getsummonerid(responseJSON)
        responseJSON = requestRankedData(region, summonerid, apikey)
        print(responseJSON)
        if len(responseJSON) == 2:
            print(responseJSON)

            values.append(returnSoloqueuestats(responseJSON))
            values.append(returnRanked5sstats(responseJSON))
            values.append(playername)
            print(values)
            return returnpage(values,filename,form)
        else:
            if(responseJSON[0]['queueType'] == rankedsoloqueuetype):
                values.append(returnSoloqueuestats(responseJSON))
                values.append('Unranked')
                values.append(playername)
                print(values)
                return returnpage(values, filename, form)
            else:
                values.append('Unranked')
                values.append(returnRanked5sstats(responseJSON))
                values.append(playername)
                print(values)
                return returnpage(values, filename, form)








    return returnpage(values, filename, form)


def returnpage(values,filename,form):
    if (len(values) > 0):
        return render_template(filename, form=form, values=values)
    else:
        return render_template('home.html', form=form)

@app.route("/NA", methods=['GET', 'POST'])
def na():
    return getstats('na1', 'carousel.html')


rankedsoloqueuetype = 'RANKED_SOLO_5x5'
ranked5squeuetype = 'RANKED_FLEX_SR'



def getanything(responseJSON, key, queuetype):
    if (responseJSON[0]['queueType'] == queuetype):
        return responseJSON[0][key]
    else:
        return responseJSON[1][key]






@app.route("/EUW", methods=['GET','POST'])
def euw():
    return getstats('euw1', 'home.html')



def requestSummonerData(region, summonerName, APIKey):
    # Here is how I make my URL.  There are many ways to create these.

    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    print ('URL')
    # requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    # Here I return the JSON we just got.
    return response.json()


def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + "?api_key=" + APIKey
    print ('URL')
    response = requests.get(URL)
    return response.json()