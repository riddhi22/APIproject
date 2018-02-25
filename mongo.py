from flask import Flask
from flask import jsonify,make_response
from flask import request
from flask_pymongo import PyMongo
import json
from tweepy.streaming import StreamListener
from pymongo import MongoClient
from tweepy import OAuthHandler
from tweepy import Stream
from flask_paginate import Pagination
from datetime import datetime
import time
import re
import csv

access_token = "960794570677133312-GV9qB6QeDxQqcP4miVdnhOoiK6mHkuC"
access_token_secret = "Ivli6wCqLgv2OOBxsHLQruW05NhvBbpqEZfEkct9c1u0s"
consumer_key = "5V4W6TBK4XYztEM9EkOCSKfhf"
consumer_secret =  "fr4I99lYwvC1mch5oSlF3eniqnzmHpyC03P6BTgcPXWlTsk9ka"

app = Flask(__name__)
#MONGO_HOST = "mongodb://ritz22:lovecoding22@ds131698.mlab.com:31698/twitter_db"

app.config['MONGO_DBNAME'] = 'twitter_db'
app.config['MONGO_URI'] = 'mongodb://riddhi22:lovecoding2297@ds131698.mlab.com:31698/twitter_db'

mongo = PyMongo(app)

class StdOutListener(StreamListener):
  def __init__(self, time_limit=60):
    self.start_time = time.time()
    self.limit = time_limit
    super(StdOutListener, self).__init__()

  def on_data(self, data):
    if (time.time() - self.start_time) < self.limit:
      try:
        user = mongo.db.users
        tweet = mongo.db.tweets
        datajson = json.loads(data)
        id1 = datajson['user']['id']
        name = datajson['user']['name']
        screenname = datajson['user']['screen_name']
        location = datajson['user']['location']
        followers = datajson['user']['followers_count']  
        user.insert_one(
        {
        "id": id1,
        "name":name,
        "screen_name": screenname,
        "location": location,
        "followers_count": followers,
         })

        created_at = datajson['created_at']
        idtw = datajson['id']
        text = datajson['text']
        retweet = datajson['retweet_count']
        fav = datajson['favorite_count']
        lang = datajson['lang']
        mention = datajson['entities']['user_mentions']
        tweet.insert_one({
          "iduni": id1,
          "created_at": created_at,
          "id": idtw,
          "text": text,
          "retweet_count": retweet,
          "fav_count": fav,
          "lang": lang,
          "mention": mention,
          })
      except Exception as e:
        print(e)
      return True
    else:
      return False

  def on_error(self, status):
    print status

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/firstapi/<string:keyword>',methods=['POST'])
def get_all_data(keyword):
   l = StdOutListener()
   auth = OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   stream = Stream(auth, l)
   stream.filter(track=[keyword])


def datafilter(name,word,scrname,rtcount,favcount,datestart,dateend,language,location,mention,sort):
  user = mongo.db.users
  tweet = mongo.db.tweets
  output = []
  if name != None:
    tempname = name
    typename = name[:2].lower()
    name = name[2:]
  if word != None:
    temptext = word
    typetext = word[:2].lower()
    text = word[2:]
  if scrname != None:
    tempscr = scrname
    scrtype = scrname[:2].lower()
    scrname = scrname[2:]
  if mention != None: 
    tempmen = mention
    mentiontype = mention[:2].lower()
    mention = mention[2:]
  if favcount != None:
    tempfav = favcount
    favtype = favcount[:2].lower()
    favcount = favcount[2:]
  if rtcount != None:
    temprt = rtcount
    rttype = rtcount[:2].lower()
    rtcount = rtcount[2:]
  
    # print type(a)
  for a in user.find():
    # print type(a)
    for t in tweet.find({"iduni": a["id"]}):

      t["use"] = a
      d = datetime.strptime(t["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
      day_string = d.strftime('%Y-%m-%d')

      if datestart != None and dateend != None:
        if day_string > datestart and day_string < dateend:
          t["flagdate"] = True
      elif datestart == None and dateend != None:
        if day_string < dateend:
          t["flagdate"] = True
      elif datestart != None and dateend == None: 
        if day_string > datestart:
          t["flagdate"] = True

      # print t
      if word != None:
        #print t["text"]
        if typetext == "sw":
          if t['text'].startswith(text):
            t['flagtext'] = True
        elif typetext == "ew":
          if t['text'].endswith(text):
            t['flagtext'] = True
        elif typetext == "co":
          if re.search(text,t["text"]):
            t['flagtext'] = True
        else:
          if temptext == t["text"]:
            t['flagtext'] = True
      

      if name != None:
        #print "Hello"
        if typename == "sw":
          if t["use"]["name"].startswith(name):
            print "Hello"
            t["flagname"] = True
            print t["flagname"]
        elif typename == "ew":
          if t['use']['name'].endswith(name):
            t['flagname'] = True
        elif typename == "co":
          if re.search(name,t["use"]["name"]):
            t['flagname'] = True
        else:
          if tempname == t['use']['name']:
            t['flagname'] = True
      

      if scrname != None: 
        if scrtype == "sw":
          if t['use']['screen_name'].startswith(scrname):
            t['flagscr'] = True
        elif scrtype == "ew":
          if t['use']['screen_name'].endswith(scrname):
            t['flagscr'] = True
        elif scrtype == "co":
          if re.search(scrname,t["use"]["screen_name"]):
            t['flagscr'] = True
        else:
          if tempscr == t['use']['screen_name']:
            t['flagscr'] = True

      
      if mention != None:  
        if mentiontype == "sw":
          if t['mention'].startswith(mention):
            t['flagmen'] = True
        elif mentiontype == "ew":
          if t['mention'].endswith(mention):
            t['flagmen'] = True
        elif mentiontype == "co":
          if re.search(mention,t["mention"]):
            t['flagmen'] = True
        else:
          if tempmen == t['mention']:
            t['flagmen'] = True


      if favcount != None:
        if favtype == "lt":
          if t['fav_count'] < int(favcount):
            t['flagfav'] = True
        elif favtype == "gt":
          if t['fav_count'] > int(favcount):
            t['flagfav'] = True
        elif favtype == "eq":
          if t['fav_count'] == int(favcount):
            t['flagfav'] = True
        else:
          if t['fav_count'] == int(tempfav):
            t['flagfav'] = True
    

      if rtcount != None:
        if rttype == "lt":
          if t['retweet_count'] < int(rtcount):
            t['flagrt'] = True
        elif rttype == "gt":
          if t['retweet_count'] > int(rtcount):
            t['flagrt'] = True
        elif rttype == "eq":
          if t['retweet_count'] == int(rtcount):
            t['flagrt'] = True
        else:
          if t['retweet_count'] == int(temprt):
            t['flagrt'] = True
      

      if language != None:
        if t['lang'] == language:
          t['flaglang'] = True

  
      if datestart != None or dateend != None:
        if "flagdate" not in t:
          continue
      if word != None:
        if "flagtext" not in t:
          continue
      if name != None:
        if "flagname" not in t:
          continue
      if scrname != None:
        if "flagscr" not in t:
          continue
      if mention != None:
        if "flagmen" not in t:
          continue
      if favcount != None:
        if "flagfav" not in t:
          continue
      if rtcount != None:
        if "flagrt" not in t:
          continue
      if language != None:
        if "flaglang" not in t:
          continue 
      output.append(t)
  
  if sort != None:
    if sort == "name":   
      newlist = sorted(output, key=lambda k: k['use']['name'])
    elif sort == "scrname":
      newlist = sorted(output, key=lambda k: k['use']['screen_name'])
    elif sort == "text":
      newlist = sorted(output, key=lambda k: k['text'])
    return newlist
  else:
    return output


@app.route('/secondapi/',methods=['GET'])
def get_all_datatext():
  try:
    name = request.args.get('name')
    word = request.args.get('text')
    scrname = request.args.get('scrname')
    rtcount = request.args.get('rtcount')
    favcount = request.args.get('favcount')
    datestart = request.args.get('datestart')
    dateend = request.args.get('dateend')
    language = request.args.get('lang') 
    location = request.args.get('location')
    mention = request.args.get('mention')
    sort = request.args.get('sort')
    newlist = datafilter(name,word,scrname,rtcount,favcount,datestart,dateend,language,location,mention,sort)
    
    #page = request.args.get('page')
    page = request.args.get('page', 1)
    try:
      page = int(page)
    except:
      page = 1
    limit = 10
    next_page = page + 1
    previous = page-1
    if previous<1:
      previous=1
   
    if len(newlist) <=(page*limit):
      next_page = 1
    newlist = newlist[((page-1)*limit) : (page*limit)]
    return JSONEncoder().encode({'newlist': newlist, 'page': page, 
      'next_page':next_page, 'previous':previous})
  except:
    message = "Something is wrong"
    status_code = error.status_code
    success = False  
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }
    return jsonify(response), status_code
  


@app.route('/firstCSVfile/',methods=['GET','POST'])
def get_branch_data_file():
  try:
    name = request.args.get('name')
    word = request.args.get('text')
    scrname = request.args.get('scrname')
    rtcount = request.args.get('rtcount')
    favcount = request.args.get('favcount')
    datestart = request.args.get('datestart')
    dateend = request.args.get('dateend')
    language = request.args.get('lang') 
    location = request.args.get('location')
    mention = request.args.get('mention')
    sort = request.args.get('sort')
    newlist = datafilter(name,word,scrname,rtcount,favcount,datestart,dateend,language,location,mention,sort)
    return_csvfile = "id,language,name,screen_name,user_id,text,mentions,retweet_count,favorite_count\n"
    for i in newlist:
      return_csvfile += ",".join([str(i['id']),i['lang'].encode("utf-8"), i['use']['name'].encode("utf-8"), 
        i['use']['screen_name'].encode("utf-8") ,str(i['use']['id']), i['text'].encode("utf-8"),str(i['mention']), 
        str(i['retweet_count']), str(i['fav_count'])]) + "\n"

    response = make_response(return_csvfile)
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=twitter_file.csv'
    return response
  except:
    message = "Something is wrong"
    status_code = error.status_code
    success = False  
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }
    return jsonify(response), status_code


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)  


#print result

  #ans =  user.find({'text': { '$regex' : 'text'}})
  
  