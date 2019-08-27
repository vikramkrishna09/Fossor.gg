#! /usr/bin/python3


from flask import Flask, render_template,url_for,redirect
import requests
from forms import SearchForm



app = Flask(__name__)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
apikey = "RGAPI-e9019ca3-fd0a-4b1e-94b7-6720d666d0aa"
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



@app.route("/EUW", methods=['GET','POST'])
def euw():
    return getstats('euw1', 'home.html')

@app.route("/NA", methods=['GET', 'POST'])
def na():
    return getstats('na1', 'carousel.html')


def getsummonerid(responseJSON):
    ID = responseJSON["id"]
    ID = str(ID)
    return ID


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
    division = Get_anything(responseJSON,'rank',queueType)
    lp = Get_anything(responseJSON,'leaguePoints',queueType)
    wins = Get_anything(responseJSON, 'wins', queueType)
    losses = Get_anything(responseJSON, 'losses', queueType)
    queuewinpercentage = wins / (losses + wins)
    queuewinpercentage = round(queuewinpercentage, 2)*100
    return [tier,division,lp,wins,losses,queuewinpercentage]

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
        if len(responseJSON) == 3:
            queue1type = responseJSON[0]['queueType']
            queue2type = responseJSON[1]['queueType']
            queue3type = responseJSON[2]['queueType']

            if(queue1type == rankedsoloqueuetype or queue2type == rankedsoloqueuetype or queue3type == rankedsoloqueuetype):
                values.append(returnStats(responseJSON,rankedsoloqueuetype))
            else:
                values.append('Unranked')
            if queue1type == ranked5squeuetype or queue2type == ranked5squeuetype or queue3type == ranked5squeuetype:
                values.append(returnStats(responseJSON,ranked5squeuetype))
            else:
                values.append('Unranked')
            values.append(playername)
            if queue1type == rankedTwistedtreelinetype or queue2type == rankedTwistedtreelinetype or queue3type == rankedTwistedtreelinetype:
                values.append(returnStats(responseJSON,rankedTwistedtreelinetype))
            else:
                values.append('Unranked')
            if queue1type == rankedtfttype or queue2type == rankedtfttype or queue3type == rankedtfttype:
                values.append(returnStats(responseJSON,rankedtfttype))
            else:
                values.append('Unranked')

            print(values)
            return returnpage(values,filename,form)


        if len(responseJSON) == 2:

            if(responseJSON[0]['queueType'] == rankedsoloqueuetype or responseJSON[1]['queueType'] == rankedsoloqueuetype):
                values.append(returnStats(responseJSON,rankedsoloqueuetype))
            else:
                values.append('Unranked')
            if(responseJSON[0]['queueType'] == ranked5squeuetype or responseJSON[1]['queueType'] == ranked5squeuetype):
                values.append(returnStats(responseJSON,ranked5squeuetype))
            else:
                values.append('Unranked')
            values.append(playername)
            if(responseJSON[0]['queueType'] == rankedTwistedtreelinetype or responseJSON[1]['queueType'] == rankedTwistedtreelinetype):
                values.append(returnStats(responseJSON,rankedTwistedtreelinetype))
            else:
                values.append('Unranked')
            if(responseJSON[0]['queueType'] == rankedtfttype or responseJSON[1]['queueType'] == rankedtfttype):
                values.append(returnStats(responseJSON,rankedtfttype))
            else:
                values.append('Unranked')
            return returnpage(values,filename,form)
        if len(responseJSON) == 1:
            if responseJSON[0]['queueType'] == rankedsoloqueuetype:
                values.append(returnStats(responseJSON,rankedsoloqueuetype))
                values.append('Unranked')
                values.append(playername)
                values.append('Unranked')
                values.append('Unranked')

                return returnpage(values, filename, form)
            elif responseJSON[0]['queueType'] == rankedTwistedtreelinetype:
                values.append('Unranked')
                values.append('Unranked')
                values.append(playername)
                values.append(returnStats(responseJSON,rankedTwistedtreelinetype))
                values.append('Unranked')

                return returnpage(values,filename,form)

            elif responseJSON[0]['queueType'] == ranked5squeuetype:
                values.append('Unranked')
                values.append(returnStats(responseJSON,ranked5squeuetype))
                values.append(playername)
                values.append('Unranked')
                values.append('Unranked')


                return returnpage(values, filename, form)

            elif (responseJSON[0]['queueType'] == rankedtfttype):
                values.append('Unranked')
                values.append('Unranked')
                values.append(playername)
                values.append('Unranked')
                values.append(returnStats(responseJSON,rankedtfttype))







    return returnpage(values, filename, form)


def returnpage(values,filename,form):
    if (len(values) > 0):
        return render_template(filename, form=form, values=values)
    else:
        return render_template('home.html', form=form)




rankedsoloqueuetype = 'RANKED_SOLO_5x5'
ranked5squeuetype = 'RANKED_FLEX_SR'
rankedTwistedtreelinetype = 'RANKED_FLEX_TT'
rankedtfttype = 'RANKED_TFT'


def getanything(responseJSON, key, queuetype):
    if (responseJSON[0]['queueType'] == queuetype):
        return responseJSON[0][key]
    else:
        return responseJSON[1][key]


def Get_anything(responseJSON,key,queuetype):
    for i in responseJSON:
        if i['queueType'] == queuetype:
            return i[key]







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



if  __name__ == "__main__":
    app.run(port=5010,debug=True)