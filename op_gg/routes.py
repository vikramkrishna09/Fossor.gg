from flask import render_template,url_for,redirect,request,flash,jsonify
from op_gg.forms import SearchForm
from op_gg.APIAccessor import getstats
from op_gg.APIAccessorExceptions import InvalidSummonerNameException,InvalidAPiKeyException
from op_gg.Summoner import Summoner

import json
from op_gg.Database import Searchdb,db
from op_gg import session as Session
db.create_all()
cache = list()
from op_gg import app,bcrypt
import os
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route("/home#", methods=['GET', 'POST'])
@app.route("/home/Username=<name>",methods=['GET', 'POST'])
def home(name=None):
    form = SearchForm()

    """ 
    print(request.environ['REMOTE_ADDR'])
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    print(request.remote_addr)
    print(request.headers.get('X-Forwarded-For', request.remote_addr))
    print(request.host)
    """
    ipaddress = getipaddress()
    unjesonifySession(ipaddress)
    Session[ipaddress] = returncache(ipaddress)
    kappacache = json.dumps(Session[ipaddress])
    if form.validate_on_submit():
        return redirect("http://" + request.host + "/" + form.playerregion.data + "/Username=" + form.playername.data + "")

    return render_template('home.html', form=form,cache=kappacache)




def getipaddress():
    return request.headers.get('X-Forwarded-For', request.remote_addr)


def setupcache(ipaddress):

    databaseresult = Searchdb.query.filter_by(ipaddress=ipaddress).all()
    global cache
    flag = 0
    for i in databaseresult:
        newsummoner = Summoner(i.summonername,i.region)
        cache.append(newsummoner.__dict__)


def returncache(ipaddress):
    databaseresult = Searchdb.query.filter_by(ipaddress=ipaddress).all()
    cache = list()
    flag = 0
    for i in databaseresult:
        newsummoner = Summoner(i.summonername, i.region)
        cache.append(newsummoner.__dict__)
    return cache




def appendSummoner(newsummoner, cache):
        newcache = json.loads(cache)
        newcache.append(newsummoner.__dict__)
        newcache = json.dumps(newcache)
        return newcache


def unjesonifySession(ipaddress):
    if ipaddress in Session:
        if isinstance(Session[ipaddress], str):
            Session[ipaddress] = json.loads(Session[ipaddress])


@app.route("/Livegame/<region>/Username=<name>")
def Livegame(name=None,region=None):
    y = 5


@app.route("/na1/Username=<name>", methods=['GET', 'POST'])
def na(name=None):
   return anyregion('na1',name)

@app.route("/euw1/Username=<name>", methods=['GET','POST'])
def euw(name=None):
  return anyregion('euw1',name)


def anyregion(region,name):
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(
            "http://" + request.host + "/" + form.playerregion.data + "/Username=" + form.playername.data + "")
    if name is not None:
        try:
            values = getstats(region, 'carousel.html', name)


        except InvalidAPiKeyException:
            flash('Invalid API Key, please change API Key!', 'error')
            return render_template('home.html', form=form, cache=cache)
        except InvalidSummonerNameException:
            flash('Invalid Summoner name, please change region, or check spelling', 'error')
            return render_template('home.html', form=form, cache=cache)
        ipaddress = getipaddress()
        newentry = Searchdb(ipaddress=ipaddress, region='na1', summonername=name)
        newsummoner = Summoner(name, 'na1')
        db.session.add(newentry)
        db.session.commit()
        unjesonifySession(ipaddress)
        if ipaddress in Session:
            Session[ipaddress].append(newsummoner.__dict__)
        else:
            Session[ipaddress] = returncache(ipaddress)
        kappacache = json.dumps(Session[ipaddress])
        return render_template('carousel.html', form=form, values=values, cache=kappacache)
    return render_template('home.html', form=form)