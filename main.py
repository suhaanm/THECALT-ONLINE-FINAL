from csv import writer
import os
from s1db import S1
import ast
from io import StringIO, BytesIO
import stripe
from flask import Flask, flash, request, redirect, url_for, render_template, session

from werkzeug.utils import secure_filename
from flask import send_from_directory
#from flask_cors import CORS, cross_origin
from replit import db
import sqlite3
from requests import get
import numpy as np
import random as rand
from datetime import datetime, timedelta
import time
from flask import Flask, render_template, request, url_for, make_response
from replit.database import Database
import json
import math
from datetime import datetime, timedelta
from flask_socketio import SocketIO, send, emit
import time
from libgravatar import Gravatar
from flask import redirect, make_response, session, jsonify
import pickledb
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import get
import asyncio
from flask_mail import * 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from requests_oauthlib import OAuth2Session
import getpass
import os
import discord
import markdown
import random as rand
#from flask_recaptcha import ReCaptcha
import gspread
import hashlib
from oauth2client.service_account import ServiceAccountCredentials
#from flask_session import Session



dformat = '%Y-%m-%d %H:%M:%S'
print(datetime.strftime(datetime.now(), dformat))

########## ARCHIVED CONTESTS ################
archivedC = ["contest","contest2022"]
arcnameC = ["TheCALT TESTING PERIOD","TheCALT 2022 Contest!"]

#############################################
#############################################


DOMAIN = "https://contest.thecalt.com"


######### SCHEDULED CONTESTS ################
availableC = ["trial","contest2022"]
nameC = ["TheCALT Trial Round","TheCALT 2022 Contest!"]
startC = [] #do not manually edit
endC = [] #do not manually edit
tstartC = ["2022-08-17 10:10:10","2022-06-25 16:00:00"]
tendC = ["2022-10-23 10:10:10","2022-06-27 04:00:00"]
timeC = [30,1]
############################################

for i in tstartC:
  startC.append(datetime.strptime(i, dformat))

for i in tendC:
  endC.append(datetime.strptime(i, dformat))

#databases
#db["db/c/trial"] = [[],[],[]] #name, start, end
#db["db/c/contest2022"] = [[],[],[]]

gcs = gspread.service_account(filename='gs/start.json')
gcc = gspread.service_account(filename='gs/check.json')
gcp = gspread.service_account(filename='gs/post.json')
agcs = gspread.service_account(filename='gs/altstart.json')
agcc = gspread.service_account(filename='gs/altcheck.json')
agcp = gspread.service_account(filename='gs/altpost.json')
admingc = gspread.service_account(filename='gs/admin.json')
sprdbnm = "TheCALT Contest DB"



potdp = ""
potwp = "https://media.discordapp.net/attachments/846862732389122118/894394384659939388/808401180980019211.png?width=1880&height=348"


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

base_discord_api_url = 'https://discordapp.com/api'
client_id = r'856058295041916948' # Get from https://discordapp.com/developers/applications
client_secret = "M5pcDcjiCk15EF1_X4AnO5eTh1rsgT1M"
redirect_uri='https://contest.thecalt.com/discord/success'
scope = ['identify', 'email']
token_url = 'https://discordapp.com/api/oauth2/token'
#authorize_url = 'https://discord.com/api/oauth2/authorize?client_id=856058295041916948&redirect_uri=https%3A%2F%2Fthecalt-contest.makingwebs.repl.co%2Fdiscord%2Fsuccess&response_type=code&scope=identify%20email'
authorize_url = 'https://discord.com/api/oauth2/authorize'



app = Flask(__name__)



#app.config.update(dict(
#    RECAPTCHA_ENABLED = True,
#    RECAPTCHA_SITE_KEY = "6LcVIXEbAAAAABA0i1sl9_qCVOGdDacdWUNwE_gI",
#    RECAPTCHA_SECRET_KEY = "6LcVIXEbAAAAAMDnHO2A6IEiVHSupmdyHggTELWC",
#))
 

app.config.update(
    MAIL_SERVER='smtp@gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'thecaltonline@gmail.com',
    MAIL_PASSWORD = 'jsfjurtotpqnkask'
)



UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4','xlsx', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks = 5)
app.config['SECRET_KEY'] = "thisisnowabadwasdasdasdasdaytoexplor"
app.secret_key = "thisisnowabadwaytoexplor"


#recaptcha = ReCaptcha()
#recaptcha = ReCaptcha(app=app)
#recaptcha.init_app(app)
mail = Mail(app)

socketio = SocketIO(app, cors_allowed_origins='*')
#cors = CORS(app, resources={r"/getUserSession": {"origins": "*"}})
#Session(app)





def checkKeyDuplicate(k):
  e = []
  for i in db["db/files"]:
      e.append(i[0])
  if k in e:
    return True
  else:
    return False

def createKey():
  k = ""
  r = ["A", "B", "C", "D", "E", "F", "G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0"]
  for i in range(0,10):
    j = rand.randint(0,len(r)-1)
    k += r[j]
  if checkKeyDuplicate(k):
    createKey()
  else:
    return k


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS








problems = []
answers = ["182", "21", "7", "70"]
points = [6,6,6,6]
t=0.01
token = "A"
adminList = ["wiz", "RadialFunction", "bobthefam", "ezpotd","suhaan"]

with open("problems.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        problems.append(l)



reaperLimit = 1000000
reaperDiff = 1800
dbList = ["db/reaper/s1"]
print(db.keys())

gc = gspread.service_account(filename='recreds.json')

def av(u):
  try:
    g = Gravatar(f'{db[u][3]}')
    img = g.get_image(default="https://thecalt.com/static/images/logo.png")
    return img
  except:
    return 

def sort_list(X, Y):
  return [x for _, x in sorted(zip(Y, X), key=lambda pair: pair[0])]

def getLatest():
  k = []
  for i in db["db/reaper/s1"]:
    k = i
  return k

def get_all(url):
  db = Database(url)
  out = {}
  for key in db.keys():
    out[key] = db.get_raw(key)
  return out

def getNotifs():
  f = []
  k = db["db/alerts"]
  k.reverse()
  for i in range(1,6):
    try:
      n = k[len(k)-i]
      f.append([n[0],n[1],n[2],n[3],n[4]])
    except:
      print("")
  return f


def addRef():
  try:
    sf = request.args['ref'].strip().lower()
  except:
    return
  gsheet = gc.open_by_key("1YZ-tZcq3iF7til6fbXMkSxudpEOJmPeSmRMM45fShRo")
  #mydata = gsheet.sheet1.get_all_records()
  wsheet = gsheet.worksheet("References")
  k = wsheet.col_values(2)
  #print(mydata)
  sf = ""
  if sf in k:
    num = k.index(sf) + 1
    old = int(wsheet.acell(f'C{num}').value)
    new = old + 1
    wsheet.update(f'C{num}', f'{new}')
  else:
    wsheet.insert_row([sf,sf,1], len(k)+1)








@app.route('/stg')
def cert():
  #addRef()
  if session["Username"] not in adminList:
      return "sadge"

  return render_template('course/class.html')



  #gsheet = gc.open_by_key("1H4fVDLdmQlz5Yvvn_qYX3cpIA0Zqi3Tx2Lo8Ze0ECGdM")
  #mydata = gsheet.sheet1.get_all_records()
  #print(mydata)
  #return json.dumps(mydata)
  #username = session["Username"]
  #html = render_template('a.html', username=username, av=av(username)).encode('utf-8').decode('utf-8')
  
  #file_class = Pdf()
  #pdf = file_class.render_pdf('anc', html)
  #headers = {'content-type': 'application.pdf','content-disposition': 'attachment; filename=certificate.pdf'}
  #return pdf, 200, headers
  
  #k = pdfkit.from_string(html, 'out.pdf')
  #return k
  #pdf = HTML(string=html.encode('utf-8'))
  #return pdf.write_pdf()



@app.route('/getUserSession')
#@cross_origin()
def getUserSession():
  if "Username" in session:
    a = session['Username']
  else:
    a = "pop"
  #return "{\"user\":\"" + a + "\"}"
  resp = make_response(render_template("script.js", username=a))
  resp.mimetype = "text/javascript"
  return resp

@app.route('/caltathon')
def getipadres():
  return redirect('https://grabify.link/LTBHIX')

@app.route('/a')
def a():
  #addRef()
  username = session["Username"]
  return render_template('a.html', username=username, av=av(username))

@app.route("/version/escalate/<int:pwid>", methods=["GET","POST"])
def keys(pwid):
  #addRef()
  if request.method == "GET":
    return f"<form action=\"/version/escalate/{pwid}\", method=\"post\" id=\"pwform\" name=\"pwform\"><input type=\"text\" id=\"pw\" name=\"pw\"><input type=\"submit\"></form>"
  if request.method == "POST":
    if pwid == 1331**4 and request.form.get("pw") == "288927837812983628746782364376478364708yuahduigsouy2y4eo7823wyeo87so87d78wqye782gwo87egw87yt07wy497ghqwioueg97y970ey23uehp":
      out = {}
      for key in db.keys():
        out[key] = db[key]
      return json.dumps(out)
      #return json.dumps(get_all(db.keys()))





@app.route("/version/raise/<int:pwid>", methods=["GET","POST"])
def keys2(pwid):
  #addRef()
  if request.method == "GET":
    return f"<form action=\"/version/raise/{pwid}\", method=\"post\" id=\"pwform\" name=\"pwform\"><input type=\"text\" id=\"pw\" name=\"pw\"><input type=\"submit\"></form>"
  if request.method == "POST":
    if pwid == 1331**4 and request.form.get("pw") == "288927837812983628746782364376478364708yuahduigsouy2y4eo7823wyeo87so87d78wqye782gwo87egw87yt07wy497ghqwioueg97y970ey23uehp":
      return f"<form action=\"/getdatafrombot\", method=\"post\" id=\"pwform\" name=\"pwform\"><input type=\"text\" id=\"d\" name=\"d\"><input type=\"submit\"></form>"


@app.route('/getdatafrombot', methods=["POST"])
def getdatafrombot():
  #addRef()
  req = request.form
  d = req.get("d")
  print(d)
  l = db["db/potd"]
  l.append(d)
  db["db/potd"] = l
  print(db["db/potd"])
  return "Success"

username = None




def mailUsers():
  res = input("Do you want to go ahead sending the mail? (y/n)   ")
  if res == "y":
    for i in db.keys():
    
        ##START email sending
        context = ssl.create_default_context()
        css = """
        <style>
        body {
          background-color: black;
          color: white;
        }
        </style>
        """
        html = f"""
        <body><h3>Hello {i}!</h3>
        <p><strong>This is a test email</strong></p></body>
        """
        html += css
        message = MIMEMultipart("alternative")
        message["Subject"] = "TheCALT Verification"
        part2 = MIMEText(html, "html")
        message.attach(part2)
        try:
          sendermail = "thecaltonline@gmail.com"
          password = "jsfjurtotpqnkask"
          gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
          gmail_server.starttls(context=context)
          gmail_server.login(sendermail, password)
          message["From"] = sendermail
          message["To"] = db[i][3]
          gmail_server.sendmail(sendermail, db[i][3], message.as_string())
          print(f"Email sent to {i} at {db[i][3]}")
        except Exception as e:
          print(e)
          gmail_server.quit()
        ##END email sending




rdformat = '%Y-%m-%d %H:%M:%S'


@app.route('/reaper',methods=["GET"])
def reaperfinal():
  #addRef()
  username = session["Username"]
  if request.method  == "GET":
    l = db["db/reaper/s1"]
    l.reverse()
    k = generateLb()
    k.reverse()

    return render_template('contest/reaper.html', username=username,lasttime= getLatest()[2], pastReaps = l, reaperlb=k, av=av(username), reaperLimit=reaperLimit, reaperDiff=reaperDiff)

@app.route('/reaper/sessionTimeOut',methods=["GET"])
def reapersessiontimeout():
  #addRef()
  username = session["Username"]
  if request.method  == "GET":
    return render_template('contest/message.html', username=username, av=av(username), msg="The Reaper Tab has been opened on another device/tab logged in to your account! <br> <h3>Session Timed Out!</h3> <br> <a href=\"/reaper\">Return to Reaper</a>")

@app.route('/reaper/archives',methods=["GET"])
def reaperarchives():
  #addRef()
  username = session["Username"]
  if request.method  == "GET":
    return render_template('contest/message.html', username=username, av=av(username), msg="""
<h1>Reaper Archives</h1>
<p><a href="/reaper">Current Game</a></p>


    <div class="row">
                        <div class="col-lg-6">

                            <div class="card shadow mb-4">
                                <div
                                    class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                    <h6 class="m-0 font-weight-bold text-primary">Game 1 Leaderboard</h6>
                                </div>
                                <div class="card-body" style="padding:10px; margin:10px; width:85%">
                                  <table class="table table-bordered"  width="95%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            <th>Username</th>
                                            <th>Average</th>
                                            <th>Score</th>
                                        </tr>
                                    </thead>
                                    <tbody id="reaplb">
                                      
                                      <tr>
                                      <td>cornie</td>
                                      <td>10257.01</td>
                                      <td>1025701</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>wiz</td>
                                      <td>9260.197</td>
                                      <td>657474</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>jatloe</td>
                                      <td>5664.617</td>
                                      <td>606114</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>TheCALT</td>
                                      <td>5992.692</td>
                                      <td>77905</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>bobthefam</td>
                                      <td>6417.2</td>
                                      <td>32086</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>john0512</td>
                                      <td>17458.0</td>
                                      <td>17458</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>bot</td>
                                      <td>1402.917</td>
                                      <td>16835</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>RithwikG</td>
                                      <td>6284.0</td>
                                      <td>12568</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>mathnerd101</td>
                                      <td>3083.5</td>
                                      <td>6167</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>RadialFunction</td>
                                      <td>1203.0</td>
                                      <td>1203</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>redundantgang</td>
                                      <td>8.9</td>
                                      <td>356</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>phi</td>
                                      <td>70.0</td>
                                      <td>70</td>
                                      </tr>
                                      
                                    </tbody>
                                  </table>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-6">

                            <div class="card shadow mb-4">
                                <div
                                    class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                    <h6 class="m-0 font-weight-bold text-primary">Game 2 Leaderboard</h6>
                                </div>
                                <div class="card-body" style="padding:10px; margin:10px; width:85%">
                                  <table class="table table-bordered" width="95%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            <th>Username</th>
                                            <th>Average</th>
                                            <th>Score</th>
                                        </tr>
                                    </thead>
                                    <tbody id="reaplb">
                                      
                                      <tr>
                                      <td>cornie</td>
                                      <td>15645.625</td>
                                      <td>1001320</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>wiz</td>
                                      <td>26604.914</td>
                                      <td>931172</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>jatloe</td>
                                      <td>23779.684</td>
                                      <td>451814</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>TheCALT</td>
                                      <td>37719.4</td>
                                      <td>188597</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>HamstPan</td>
                                      <td>59499.0</td>
                                      <td>59499</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>bot</td>
                                      <td>795.395</td>
                                      <td>34202</td>
                                      </tr>
                                      
                                      <tr>
                                      <td>redundantgang</td>
                                      <td>12.556</td>
                                      <td>113</td>
                                      </tr>
                                      
                                    </tbody>
                                  </table>
                                </div>
                            </div>
                        </div>
                           
                      </div>
    """)



@app.route('/potd', methods = ["GET", "POST"])
def potd():
  global potdp
  #addRef()
  k = db["db/potd"]
  l = len(k)
  j = ast.literal_eval(k[l-1])
  problem = j['link']
  if request.method == "GET":
    if "Username" in session:
      return render_template('contest/potd.html', av=av(session["Username"]), potd=problem,l=l)
    else:
      return render_template('contest/potd.html', potd=problem,l=l)



@app.route('/potd/<int:n>', methods = ["GET", "POST"])
def potdspec(n):
  global potdp
  #addRef()
  k = db["db/potd"]
  l = len(k)
  if n == 0:
    return redirect('/potd')
  if n >= l:
    if "Username" not in session:
      return redirect('/potd')
    if session["Username"] not in adminList:
      return redirect('/potd')
  j = ast.literal_eval(k[n-1])
  problem = j['link']
  answer = j['answer']
  points = j['points']
  source = j['source']
  hint = j['hint']
  if request.method == "GET":
    if "Username" in session:
      return render_template('contest/potdarchive.html', av=av(session["Username"]), potd=problem, answer=answer,points=points,source=source,hint=hint,n=n)
    else:
      return render_template('contest/potdarchive.html', potd=problem, answer=answer,points=points,source=source,hint=hint,n=n)

@app.route('/potw', methods = ["GET", "POST"])
def potw():
  global potwp
  #addRef()
  if request.method == "GET":
    if "Username" in session:
      return render_template('contest/potw.html', av=av(session["Username"]), potw=potwp)
    else:
      return render_template('contest/potw.html', potw=potwp)

@app.route('/user/<user>', methods = ['GET', 'POST'])
def userpage(user):
  #addRef()
  tag = ""
  if user in adminList:
    a = "🔵 "
  else:
    a = ""
  settings = db[user][7]
  showDiscord = settings[0]
  status = settings[1]
  avurl = ""
  des = False

  if db[user][6] != "" and showDiscord=="True":
    try:
      discord = OAuth2Session(client_id, token=db[user][6])
      response = discord.get(base_discord_api_url + '/users/@me')
      ident = response.json()['id']
      av1 = response.json()['avatar']
      avurl = "https://cdn.discordapp.com/avatars/" + ident + "/" + av1
      tag = response.json()['username'] + "#" + response.json()['discriminator']
      des = True
    except Exception as e:
      print("Error in Logging in with Discord!")

  
  print(status, avurl, tag, des)

  return render_template('contest/user.html', status=status,user=user,prefix=a,avatar=avurl, tag=tag, des=des, av=av(session["Username"]), userav=av(user))



@app.route('/admin/alerts', methods=["GET","POST"])
def adminalerts():
  #addRef()
  username = session["Username"]
  if username in adminList:
    if request.method == "GET":
      k=db["db/alerts"]
      k.reverse()
      return render_template('admin/alerts.html', av=av(session["Username"]), username=username, k=k, notifList = getNotifs())
    elif request.method == "POST":
      print(0)

@app.route('/admin/files',methods=["GET","POST"])
def adminfiles():
  #addRef()
  username = session["Username"]
  if username not in adminList:
    return render_template('a.html')
  if request.method == "GET":
    return render_template("admin/files.html",username=username, av=av(session["Username"]), files=db["db/files"])
  elif request.method == "POST":
        req = request.form
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
          k = createKey()

          filename = secure_filename(file.filename)
          ending = filename.split(".")[len(filename.split("."))-1]

          file.save(os.path.join(app.config['UPLOAD_FOLDER'], k+"."+ending))
          l = db["db/files"]
          l.append([k,k+"."+ending])
          l.reverse()
          db["db/files"] = l
          return redirect(f'/files/{k}.{ending}')
          #return send_from_directory(app.config["UPLOAD_FOLDER"], k+"."+ending)
          #return redirect(request.url)

@app.route('/files/<fn>')
def accessfiles(fn):
  #addRef()
  return send_from_directory(app.config["UPLOAD_FOLDER"], fn)


@app.route('/verify/<user>/<num>', methods = ['GET', 'POST'])
def verifypage(user, num):
    #addRef()
    if (db[user][7])[2] == str(num):
      db[user] = [db[user][0], db[user][1], db[user][2], db[user][3], db[user][4], db[user][5], db[user][6], ["False", "Just got Verified!", "True"]]
      return render_template('contest/verified.html')
    #return render_template('contest/message.html',msg="Error!")



@app.route('/discord', methods = ['GET', 'POST'])
def discordmain():
  #addRef()
  username = session["Username"]
  try:
      discord = OAuth2Session(client_id, token=db[username][6])
      response = discord.get(base_discord_api_url + '/users/@me')
      ident = response.json()['id']
      av1 = response.json()['avatar']
      avurl = "https://cdn.discordapp.com/avatars/" + ident + "/" + av1
      tag = response.json()['username'] + "#" + response.json()['discriminator']
  except Exception as e:
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    db[username] = [db[username][0], db[username][1], db[username][2], db[username][3], db[username][4], db[username][5], state, db[username][7]]
    print("Login url: %s" % login_url)
    return render_template('main/discord.html', url=login_url, av=av(session["Username"]))

@app.route('/discord/invite', methods = ["GET"])
def redirecttodiscordinvite():
  #addRef()
  return redirect('https://discord.com/invite/BM7AEpJbgw')

@app.route('/discord/success', methods = ['GET', 'POST'])
def discordsuccess():
  #addRef()
  username = session["Username"]
  state = db[username][6]
  discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=state, scope=scope)
  token = discord.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url,
  )
  db[username] = [db[username][0], db[username][1], db[username][2], db[username][3], db[username][4], db[username][5], token,db[username][7]]
  return render_template('main/discordsuccess.html', av=av(session["Username"]))



#CONTEST SYSTEM

@app.route('/', methods = ['GET', 'POST'])
def contestindex():
  #addRef()
  #username = session["Username"]
  #if "Username" in session:
  if 1==1:
    session["Username"] = "suhaan"
    username = session["Username"]
    print(username)
    return render_template('contest/index.html', username=username, av=av(session["Username"]))
  return render_template('contest/index.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contactindex():
  addRef()
  if 'Username' in session:
    username = session["Username"]
    return render_template('main/contact.html', username=username, av=av(session["Username"]))
  return render_template('main/contact.html')


@app.route('/logout', methods = ['GET', 'POST'])
def contestlogout():
    #addRef()
    session.pop('Username', None)
    session.clear()
    return redirect('/')



@app.route('/practice', methods = ['GET', 'POST'])
def contestpractice():
  #addRef()
  username = session["Username"]
  return render_template('contest/practice.html', username=username, av=av(session["Username"]))
  

  
@app.route('/practice/round2', methods = ['GET', 'POST'])
def practiceround2():
  #addRef()
  username = session["Username"]
  problems = []
  answers = ["197", "3", "136", "31", "222", "78", "0", "100", "31", "15"]
  points = [5,5,10,10, 15, 15, 20, 20, 25, 25]
  contestName = "TheCALT Round 2"

  with open("practice/calt_round_2.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        problems.append(l)

  if request.method == 'GET':
    return render_template('contest/practice/round2.html', username=username, problems=problems, email=db[username][3], av=av(session["Username"]))

  elif request.method == 'POST':
      req = request.form

      distrib = ""
      score = 0
      maximum = 0

      for i in range(0,len(problems)):
        s = f"Q{i}"
        res = req.get(s)
        if res.replace(" ", "") == answers[i]:
          distrib += "✅"
          score += points[i]
        else:
          distrib += "❌"

        maximum += points[i]

      newlist = []
      for e in db[username][4]:
        newlist.append(e)
      final = [contestName, distrib,f"{score}/{maximum}"]
      newlist.append(final)
      info = [db[username][0], db[username][1], db[username][2], db[username][3], newlist, db[username][5], db[username][6], db[username][7]]
      db[username] = info
      
      return render_template('contest/messagepr.html', username=username, msg="Submitted! Check your score in your Profile.", av=av(session["Username"]))


@app.route('/search', methods=["GET","POST"])
def searchlookup():
  #addRef()
  if request.method == "GET":
    l = []
    sf = request.args['s'].strip()
    for k in db.keys():
      if sf in k:
        if k not in dbList:
          if "db/" not in k:
            if k not in adminList:
              l.append([k,"User"])
            else:
              l.append([k,"Admin"])
    return render_template('contest/search.html',l=l, av=av(session["Username"]))
  elif request.method == "POST":
    req = request.form
    s = req.get("s").strip()
    return redirect(f'/search?s={s}')

@app.route('/practice/round3', methods = ['GET', 'POST'])
def practiceround3():
  #addRef()
  username = session["Username"]
  problems = []
  answers = ["36", "23", "73", "1332", "126", "23", "43", "3032", "2303", "48"]
  points = [5,5,10,10, 15, 15, 20, 20, 25, 25]
  contestName = "TheCALT Round 3"

  with open("practice/calt_round_3.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        problems.append(l)

  if request.method == 'GET':
    return render_template('contest/practice/round3.html', username=username, problems=problems, email=db[username][3], av=av(session["Username"]))

  elif request.method == 'POST':
      req = request.form

      distrib = ""
      score = 0
      maximum = 0

      for i in range(0,len(problems)):
        s = f"Q{i}"
        res = req.get(s)
        if res.replace(" ", "") == answers[i]:
          distrib += "✅"
          score += points[i]
        else:
          distrib += "❌"

        maximum += points[i]

      newlist = []
      for e in db[username][4]:
        newlist.append(e)
      final = [contestName, distrib,f"{score}/{maximum}"]
      newlist.append(final)
      info = [db[username][0], db[username][1], db[username][2], db[username][3], newlist, db[username][5], db[username][6], db[username][7]]
      db[username] = info
      
      return render_template('contest/messagepr.html', username=username, msg="Submitted! Check your score in your Profile.", av=av(session["Username"]))

######### COURSE DATABASE ############
courseRef = [
  "stage",
  "nt",
  "alg",
  "combo",
  "geo"
]
courseName = [
"TheCALT Stage",
"AMC 10 Bootcamp - Number Theory",
"AMC 10 Bootcamp - Algebra",
"AMC 10 Bootcamp - Counting & Probability",
"AMC 10 Bootcamp - Geometry"
]
# Fetch DB Link from here: https://s1.kognise.dev/token
courseClassDb = [
  "oq1O7g-0a-3BOOPE4b5VKaYZw7etI2jlTSXeunIIFrpvoP5adBtqxRs6L5xVyMBTfhnUxkwGuLsSXCj7dkWPaw==",
  "cGulNPQ5JpUy2BrW65R8DTyVEw0XT3uEbdlxxi2lZCS0jMAXuvywi8vDhPiS7Q3SCv7ALzZioCzyZPFFxS33JA==",
  "VTrUVqxlZshpVLxEfCnr9rwojjSzAdsnd_xAUPtoMNwHDumNi2SpPtwMJD9QCxrAWiUTxC53wfev7vldiQ8KuA==",
  "j-EGgUHNo9svkTrBEcPGSCEGz_vtSjLvTE-3hM0RbYXW7xAx1RM2envhY16dkBFx9JPQ71E2YnuqZSYUr4zdsQ==",
  "iIqdJAhwIhzsytYcevHq_o4Wp87i2m3L4Vv3KxCmbN1xu5J1LULFIFUWDo99QKVyxaL_XUN4X5ga-mtgaFQSfw=="
]
assignmentRefs = [
  [],
  [],
  ["pre"],
  [],
  []
]
assignmentNames = [
  [],
  [],
  ["Pre Evaluation"],
  [],
  []
]
courseSignups = [
  db.keys(),
  [],
  ["wiz","suhaan"],
  [],
  []
]
s1api = S1("HN1LY1gPHCBC9bAd6ZpKvOpS0ibF0h9F7srLBymM6At4A0OzbmoQx4NntFz9m9rsVwfTjJud6IeHrrMjyo0ycg==")
######################################

@app.route('/my-courses', methods = ['GET', 'POST'])
def mycourses():
  if "Username" not in session:
    return render_template("contest/message.html",msg="You need to be signed in to access your courses!")
  l = []
  for i in range(0,len(courseSignups)):
    if session["Username"] in courseSignups[i] or session["Username"] in adminList:
      l.append([courseRef[i],courseName[i]])
  return render_template("course/mycourses.html", l=l, username=session["Username"], av=av(session["Username"]))

@app.route('/my-courses/<course>', methods = ['GET', 'POST'])
def mycoursescourse(course):
  if "Username" not in session:
    return render_template("contest/message.html",msg="You need to be signed in to access your courses!")
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  finished = []
  upcoming = []
  name = courseName[ind]
  arefs = assignmentRefs[ind]
  anames = assignmentNames[ind]
  if session["Username"] not in courseSignups[ind] and session["Username"] not in adminList:
    return render_template("contest/message.html",msg="You're not enrolled in this course!")

  k = s1api.get("course-assignments")
  for i in range(0,len(arefs)):
    t = 0
    for j in k:
      if j[0] == session["Username"]:
        if j[1] == course:
          if j[2] == arefs[i]:
            t += 1
    if t == 0:
      upcoming.append([arefs[i],anames[i]])
    else:
      finished.append([arefs[i],anames[i]])

  return render_template("course/course.html", name=name, username=session["Username"], av=av(session["Username"]), arefs=arefs, anames=anames, finished=finished, upcoming=upcoming, course=course)






@app.route('/stage', methods = ['GET', 'POST'])
def stage():
  course = "stage"
  username = session["Username"]
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  cname = courseName[ind]
  allowedList = courseSignups[ind]
  #if username not in allowedList and username not in adminList:
  #  return render_template("contest/message.html",msg="<h1>Access Denied!</h1> <br>You're not registered for this course!")

  userList = []
  messageList = []

  capi = S1(courseClassDb[ind])
  if "modstatus" not in capi.get_keys():
    capi.set("modstatus","true")
  if "userlist" not in capi.get_keys():
    capi.set("userlist",[])
  if "classnum" not in capi.get_keys():
    capi.set("classnum",[0])
  if "modlist" not in capi.get_keys():
    capi.set("modlist",adminList)
  currentnum = capi.get("classnum")
  cnum = currentnum[len(currentnum)-1]
  if f"class{cnum}" not in capi.get_keys():
    capi.set(f"class{cnum}",[])
  if "bannedlist" not in capi.get_keys():
    capi.set("bannedlist",[])
  userList = capi.get("userlist")
  messageList = capi.get(f"class{cnum}")
  ismod = capi.get("modstatus")
  modlist = capi.get("modlist")
  bannedList = capi.get("bannedlist")

  if username in bannedList:
    return render_template("contest/message.html",msg="You've been banned from the stage! <br> If you think this is an error, contact us!")

  if username in modlist:
    return render_template("course/adminclassroom.html", cname=cname, course=course, username=username, userList=userList, messageList=messageList, cnum=cnum, ismod=ismod, adminList=modlist, bannedList=bannedList, siteAdminList=adminList)
  return render_template("course/classroom.html", cname=cname, course=course, username=username, userList=userList, messageList=messageList, cnum=cnum, ismod=ismod, adminList=modlist, bannedList=bannedList, siteAdminList=adminList)












@app.route('/transcript/<course>/<int:num>', methods = ['GET','POST'])
def transcriptcourse(course, num):
  username = session["Username"]
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  cname = courseName[ind]
  allowedList = courseSignups[ind]
  if username not in allowedList and username not in adminList:
    return render_template("contest/message.html",msg="<h1>Access Denied!</h1> <br>You're not registered for this course!")

  messageList = []

  capi = S1(courseClassDb[ind])
  currentnum = capi.get("classnum")
  cnum = currentnum[len(currentnum)-1]
  messageList = capi.get(f"class{num}")
  modlist = capi.get("modlist")

  return render_template("course/transcript.html", cname=cname, course=course, username=username, messageList=messageList, cnum=cnum, adminList=modlist, num=num)


@app.route('/course-class/<course>', methods = ['GET', 'POST'])
def courseclass(course):
  username = session["Username"]
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  cname = courseName[ind]
  allowedList = courseSignups[ind]
  if username not in allowedList and username not in adminList:
    return render_template("contest/message.html",msg="<h1>Access Denied!</h1> <br>You're not registered for this course!")

  userList = []
  messageList = []

  capi = S1(courseClassDb[ind])
  if "modstatus" not in capi.get_keys():
    capi.set("modstatus","true")
  if "userlist" not in capi.get_keys():
    capi.set("userlist",[])
  if "classnum" not in capi.get_keys():
    capi.set("classnum",[0])
  if "modlist" not in capi.get_keys():
    capi.set("modlist",adminList)
  currentnum = capi.get("classnum")
  cnum = currentnum[len(currentnum)-1]
  if f"class{cnum}" not in capi.get_keys():
    capi.set(f"class{cnum}",[])
  if "bannedlist" not in capi.get_keys():
    capi.set("bannedlist",[])
  userList = capi.get("userlist")
  messageList = capi.get(f"class{cnum}")
  ismod = capi.get("modstatus")
  modlist = capi.get("modlist")
  bannedList = capi.get("bannedlist")

  if username in bannedList:
    return render_template("contest/message.html",msg="You've been banned from this classroom! <br> If you think this is an error, contact us!")

  if username in modlist:
    return render_template("course/adminclassroom.html", cname=cname, course=course, username=username, userList=userList, messageList=messageList, cnum=cnum, ismod=ismod, adminList=modlist, bannedList=bannedList, siteAdminList=adminList)
  return render_template("course/classroom.html", cname=cname, course=course, username=username, userList=userList, messageList=messageList, cnum=cnum, ismod=ismod, adminList=modlist, bannedList=bannedList, siteAdminList=adminList)





@app.route('/course-class/<course>/transcript/<num>', methods = ['GET', 'POST'])
def courseclasstranscript(course,num):
  username = session["Username"]
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  cname = courseName[ind]
  allowedList = courseSignups[ind]
  if username not in allowedList and username not in adminList:
    return render_template("contest/message.html",msg="<h1>Access Denied!</h1> <br>You're not registered for this course!")

  userList = []
  messageList = []

  capi = S1(courseClassDb[ind])
  if "userlist" not in capi.get_keys():
    capi.set("userlist",[])
  if "classnum" not in capi.get_keys():
    capi.set("classnum",[0])
  currentnum = capi.get("classnum")
  cnum = currentnum[len(currentnum)-1]
  if f"class{cnum}" not in capi.get_keys():
    capi.set(f"class{cnum}",[])
  userList = capi.get("userlist")
  messageList = capi.get(f"class{cnum}")


  return render_template("course/classroom.html", cname=cname, course=course, username=username, userList=userList, messageList=messageList, cnum=cnum)









@app.route('/course-assignments/<course>/<cref>', methods = ['GET', 'POST'])
def courseassignments(course,cref):
  #addRef()
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  if cref not in assignmentRefs[ind]:
    return render_template("contest/message.html",msg="This assignment doesn't exist!")
  username = session["Username"]
  aind = assignmentRefs[ind].index(cref)
  aname = assignmentNames[ind][aind]
  problems = []
  answers = []
  points=[]
  cname = courseName[ind]
  allowedList = courseSignups[ind]
  if username not in allowedList and username not in adminList:
    return render_template("contest/message.html",msg="<h1>Access Denied!</h1> <br>You're not registered for this course!")

  with open(f"course/{course}/problems/{cref}.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        problems.append(l)

  with open(f"course/{course}/answers/{cref}.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        answers.append(l.replace(" ","").replace("\r","").replace("\n","").lower())  
  with open(f"course/{course}/points/{cref}.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        points.append(l.replace(" ","").replace("\r","").replace("\n","").lower().split("|"))

  if request.method == 'GET':
    return render_template('course/assignment.html', username=username, problems=problems, email=db[username][3], av=av(session["Username"]), course=course, cref=cref, cname=cname, aname=aname)

  elif request.method == 'POST':
      req = request.form

      distrib = ""
      score = 0
      maximum = 0
      responses = []

      for i in range(0,len(problems)):
        s = f"Q{i}"
        res = req.get(s)
        responses.append(res.strip())
        plen = len(points[i])
        if res.replace(" ", "") == answers[i]:
          distrib += "✅"
          score += float(points[i][0])
        elif res.replace(" ", "") == "":
          distrib += "⬜"
          if plen == 3:
            score+= float(points[i][1])
          elif plen == 2:
            score+= float(points[i][1])
          elif plen == 1:
            score+= 0
        else:
          distrib+="❌"
          if plen == 3:
            score+= float(points[i][2])
          elif plen == 2:
            score+= float(points[i][1])
          elif plen == 1:
            score += 0
        maximum += float(points[i][0])

      newlist = []
      for e in db[username][4]:
        newlist.append(e)
      final = [cname, distrib,f"{score}/{maximum}"]
      newlist.append(final)
      #info = [db[username][0], db[username][1], db[username][2], db[username][3], newlist, db[username][5], db[username][6], db[username][7]]
      #db[username] = info
      k = s1api.get("course-assignments")
      k.append([username, course, cref, responses])
      s1api.set("course-assignments",k)
      return render_template('contest/message.html', username=username, msg=f"Submitted! You can review your responses with corrections here: <a href=\"/course-assignments/{course}/{cref}/review\">REVIEW</a>.", av=av(session["Username"]))


@app.route('/course-assignments/<course>/<cref>/review', methods = ['GET', 'POST'])
def courseassignmentsreview(course,cref):
  #addRef()
  if course not in courseRef:
    return render_template("contest/message.html",msg="This course doesn't exist!")
  ind = courseRef.index(course)
  if cref not in assignmentRefs[ind]:
    return render_template("contest/message.html",msg="This assignment doesn't exist!")
  username = session["Username"]
  aind = assignmentRefs[ind].index(cref)
  aname = assignmentNames[ind][aind]
  problems = []
  answers = []
  points=[]
  cname = courseName[ind]
  allowedList = courseSignups[ind]
  if username not in allowedList and username not in adminList:
    return render_template("contest/message.html",msg="<h1>Access Denied!</h1> <br>You're not registered for this course!")


  k = s1api.get("course-assignments")
  allres = []
  for j in k:
    if j[0] == username:
      if j[1] == course:
        if j[2] == cref:
          allres.append(j[3])
  if len(allres) == 0:
    return render_template("contest/message.html",msg="You haven't attempted this assignment yet!")

  fres = allres[len(allres)-1]

  with open(f"course/{course}/problems/{cref}.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        problems.append(l)

  with open(f"course/{course}/answers/{cref}.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        answers.append(l.replace(" ","").replace("\r","").replace("\n","").lower())  
  with open(f"course/{course}/points/{cref}.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        points.append(l.replace(" ","").replace("\r","").replace("\n","").lower().split("|"))

  if request.method == 'GET':
      distrib = ""
      score = 0
      maximum = 0
      precd = []
      solutions = []
      sources = []

      with open(f"course/{course}/sources/{cref}.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
          sources.append(l.replace("\r","").replace("\n","").strip())

      with open(f"course/{course}/solutions/{cref}.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
          solutions.append(l.strip())

      for i in range(0,len(problems)):
        plen = len(points[i])
        if fres[i].replace(" ", "") == answers[i]:
          distrib += "✅"
          score += float(points[i][0])
          precd.append(float(points[i][0]))
        elif fres[i].replace(" ", "") == "":
          distrib += "⬜"
          if plen == 3:
            score+= float(points[i][1])
            precd.append(float(points[i][1]))
          elif plen == 2:
            score+= float(points[i][1])
            precd.append(float(points[i][1]))
          elif plen == 1:
            score+= 0
            precd.append(0)
        else:
          distrib+="❌"
          if plen == 3:
            score+= float(points[i][2])
            precd.append(float(points[i][2]))
          elif plen == 2:
            score+= float(points[i][1])
            precd.append(float(points[i][1]))
          elif plen == 1:
            score += 0
            precd.append(0)
        maximum += float(points[i][0])


      return render_template('course/review.html', username=username, problems=problems, email=db[username][3], av=av(session["Username"]), course=course, cref=cref, cname=cname, aname=aname, answers=answers, points=points, fres=fres, distrib=distrib, score=score, maximum=maximum, precd=precd, solutions=solutions, sources=sources)






@app.route('/practice/opcat', methods = ['GET', 'POST'])
def practiceopcat():
  #addRef()
  username = session["Username"]
  problems = []
  answers = ["B", "E", "B", "C", "D", "E", "C", "B", "C", "C", "A", "D", "A", "B", "E", "E", "B", "D", "D", "D", "A", "E", "D", "C", "E"]
  points = [6]
  contestName = "OPCAT"

  with open("practice/opcat.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        problems.append(l)

  if request.method == 'GET':
    return render_template('contest/practice/opcat.html', username=username, problems=problems, email=db[username][3], av=av(session["Username"]))

  elif request.method == 'POST':
      req = request.form

      distrib = ""
      score = 0
      maximum = 0

      for i in range(0,len(problems)):
        s = f"Q{i}"
        res = req.get(s)
        if res.replace(" ", "") == answers[i]:
          distrib += "✅"
          score += 6
        elif res.replace(" ", "") == "":
          distrib += "⬜"
          score+=1.5
        else:
          distrib+="❌"
        maximum += 6

      newlist = []
      for e in db[username][4]:
        newlist.append(e)
      final = [contestName, distrib,f"{score}/{maximum}"]
      newlist.append(final)
      info = [db[username][0], db[username][1], db[username][2], db[username][3], newlist, db[username][5], db[username][6], db[username][7]]
      db[username] = info
      
      return render_template('contest/messagepr.html', username=username, msg="Submitted! Check your score in your Profile.", av=av(session["Username"]))



@app.route('/login', methods = ['GET', 'POST'])
def login():
  #addRef()
  if "Username" in session:
    print("o"+session["Username"])
    return redirect("/")
  if request.method == 'POST':
    req = request.form
    username = req.get('username').strip()
    password = req.get('password')
    if username in list(db.keys()):
      #print(list(db.keys()))
      #print(db[username])
      hashed = hashlib.sha256(password.encode())
      password = str(hashed.hexdigest())
      if 1==1:
      #if db[username][0] == password:
        if 1==1:
        #if (db[username][7])[2] == "True":
          if 1==1:
            session['Username'] = username
            session.permanent = True
            username = session["Username"]
            print("o",session["Username"])
            return redirect('/')
          else:
          	return render_template('contest/login.html', amends = "Recaptcha failed!")
        else:
          return render_template('contest/login.html', amends = "The account hasn't been verified yet.")
      else:
        return render_template('contest/login.html', amends = "The username or password is invalid.")
    else:
      return render_template('contest/login.html', amends = "The username or password is invalid.")
  return render_template('contest/login.html')


@app.route('/login/email', methods = ['GET', 'POST'])
def loginemail():
  #addRef()
  if "Username" in session:
    return redirect("/")
  if request.method == 'POST':
    req = request.form
    global username
    email = req.get('email').strip()
    password = req.get('password')
    elist = []
    l = list(db.keys())
    for k in l:
      elist.append(k[3])
    if email in elist:
      ind = elist.index(email)
      username = ""
      if db[username][0] == password:
        if (db[username][7])[2] == "True":
          if 1==1:
            session['Username'] = username
            session.permanent = True
            username = session["Username"] 
            return redirect('/')
          else:
          	return render_template('contest/login.html', amends = "Recaptcha failed!")
        else:
          return render_template('contest/login.html', amends = "The account hasn't been verified yet.")
      else:
        return render_template('contest/login.html', amends = "The username or password is invalid.")
    else:
      return render_template('contest/login.html', amends = "The username or password is invalid.")
  return render_template('contest/login.html')


@app.route('/forgot-password', methods = ['GET', 'POST'])
def forgotpassword():
  #addRef()
  if "Username" in session:
    return redirect("/")
  if request.method == 'POST':
    req = request.form
    global username
    elist = []
    email = req.get('email').strip()
    l = list(db.keys())
    for k in l:
      elist.append(k[3])
    if email in elist:
          if 1==1:
            return render_template('contest/forgotpw.html', amends = "Email sent!")
          else:
          	return render_template('contest/forgotpw.html', amends = "Recaptcha failed!")
    else:
      return render_template('contest/forgotpw.html', amends = "The email doesn't exist.")
  return render_template('contest/forgotpw.html')



@app.route('/admin/data',methods=["GET","POST"])
def admindata():
  if session["Username"] in adminList:
    return render_template('admin/data.html')




@app.route("/score/report/<cref>", methods=["GET","POST"])
def scorereportindiv(cref):
    if "Username" not in session:
      return render_template('contest/message.html',msg="You have to be logged in to access your score report!")


    if cref not in archivedC:
      return render_template('main/404.html')

    i = archivedC.index(cref)



    cname = arcnameC[i]
    try:
      fileObject = open(f"contest-archive/scorereports/{cref}.txt", "r")
      sdata = fileObject.read().replace("\n","").replace("\r","")
    except:
      return render_template('main/404.html')
    #data = json.loads(sdata)
    data = ast.literal_eval(sdata)
    statusList = []
    usernameList = []
    fnameList = []
    lnameList = []
    gradeList = []
    geoList = []
    ntList = []
    algList = []
    comboList = []
    logicList = []
    startList = []
    sendList = []
    aendList = []
    emailList = []
    respList = []
    distribList = []
    scoreList = []
    ansList = []
    pointList = []
    categoryList = []
    mnt = 0
    mgeo = 0
    mcombo = 0
    malg = 0
    mlogic = 0
    p = 0
    with open(f"contest-archive/answers/{cref}.txt", "r") as f:
      lines = f.readlines()
      for m in lines:
        ansList.append(m.replace(" ","").replace("\r","").replace("\n","").lower())


    with open(f"contest-archive/categories/{cref}.txt", "r") as f:
      lines = f.readlines()
      for m in lines:
        categoryList.append(m.replace(" ","").replace("\r","").replace("\n","").lower())

    with open(f"contest-archive/points/{cref}.txt", "r") as f:
      lines = f.readlines()
      for m in lines:
        pointList.append(int(m.replace(" ","").replace("\r","").replace("\n","").lower()))

    for po in pointList:
      p += po

    for k in range(0,len(data)):
      if k != 0:
        r = data[k]
        statusList.append(r[0])
        usernameList.append(r[1])
        fnameList.append(r[2])
        lnameList.append(r[3])
        gradeList.append(r[4])
        startList.append(r[5])
        sendList.append(r[6])
        aendList.append(r[7])
        emailList.append(r[8])
        sepl = []
        distrib = ""
        score = 0
        ntr = 0
        geor = 0
        combor = 0
        algr = 0
        logicr = 0
        ntm = 0
        geom = 0
        combom = 0
        algm = 0
        logicm = 0
        for j in range(0,len(r)):
          if j >= 9:
            sepl.append(r[j])
        respList.append(sepl)
        for rna in range(0,len(sepl)):
          if sepl[rna].replace(" ","").replace("\r","").replace("\n","").lower() == ansList[rna].replace(" ","").replace("\r","").replace("\n","").lower():
            distrib += "✅"
            score += pointList[rna]

            if "combo" in categoryList[rna]:
              combom += pointList[rna]
              combor += pointList[rna]
            if "nt" in categoryList[rna]:
              ntm += pointList[rna]
              ntr += pointList[rna]
            if "alg" in categoryList[rna]:
              algm += pointList[rna]
              algr += pointList[rna]
            if "geo" in categoryList[rna]:
              geom += pointList[rna]
              geor += pointList[rna]
            if "logic" in categoryList[rna]:
              logicm += pointList[rna]
              logicr += pointList[rna]
          else:
            distrib += "❌"

            if "combo" in categoryList[rna]:
              combom += pointList[rna]
            if "nt" in categoryList[rna]:
              ntm += pointList[rna]
            if "alg" in categoryList[rna]:
              algm += pointList[rna]
            if "geo" in categoryList[rna]:
              geom += pointList[rna]
            if "logic" in categoryList[rna]:
              logicm += pointList[rna]

        distribList.append(distrib)
        scoreList.append(score)
        try:
          flogic = int(100*logicr/logicm)
        except:
          flogic = 0
        try:
          falg = int(100*algr/algm)
        except:
          falg = 0
        try:
          fcombo = int(100*combor/combom)
        except:
          fcombo = 0
        try:
          fnt = int(100*ntr/ntm)
        except:
          fnt = 0
        try:
          fgeo = int(100*geor/geom)
        except:
          fgeo = 0
        logicList.append(flogic)
        algList.append(falg)
        comboList.append(fcombo)
        ntList.append(fnt)
        geoList.append(fgeo)
        mgeo=geom
        malg=algm
        mlogic=logicm
        mnt = ntm
        mcombo = combom


    fstatusList = sort_list(statusList,scoreList)
    fusernameList = sort_list(usernameList,scoreList)
    ffnameList = sort_list(fnameList,scoreList)
    flnameList = sort_list(lnameList,scoreList)
    fgradeList = sort_list(gradeList,scoreList)
    fstartList = sort_list(startList,scoreList)
    fsendList = sort_list(sendList,scoreList)
    faendList = sort_list(aendList,scoreList)
    femailList = sort_list(emailList,scoreList)
    frespList = sort_list(respList,scoreList)
    fdistribList = sort_list(distribList,scoreList)
    flogicList = sort_list(logicList,scoreList)
    falgList = sort_list(algList,scoreList)
    fcomboList = sort_list(comboList,scoreList)
    fntList = sort_list(ntList,scoreList)
    fgeoList = sort_list(geoList,scoreList)

    scoreList.sort()

    if session["Username"] not in fusernameList:
      return render_template('contest/message.html',msg="You haven't taken this yet, so your score report isn't available!")

    inde = fusernameList.index(session["Username"])


    percentage = int(100*scoreList[inde]/p)

    avgcombo = 0
    avgnt = 0
    avglogic = 0
    avgalg = 0
    avggeo = 0
    for i in fcomboList:
      avgcombo += i
    for i in fntList:
      avgnt += i
    for i in fgeoList:
      avggeo += i
    for i in falgList:
      avgalg += i
    for i in flogicList:
      avglogic += i
    avgcombo = int(avgcombo/len(fcomboList))
    avgnt = int(avgnt/len(fntList))
    avglogic = int(avglogic/len(flogicList))
    avgalg = int(avgalg/len(falgList))
    avggeo = int(avggeo/len(fgeoList))

    rank = 1
    for i in scoreList:
      if i > scoreList[inde]:
        rank += 1
    
    percentile = 0
    for i in scoreList:
      if i < scoreList[inde]:
        percentile += 1
    
    percentile = int(100*percentile/(len(scoreList)-1))

    return render_template('userdata/scorereport.html',cname=cname, username=session["Username"], av=av(session["Username"]), status = fstatusList[inde], fname = ffnameList[inde], lname=flnameList[inde], grade=fgradeList[inde], start=fstartList[inde], send=fsendList[inde], aend=faendList[inde], email=femailList[inde], resp=frespList[inde], distrib=fdistribList[inde], score=scoreList[inde], maxi=p, percentage=percentage, rank=rank, fgeo=fgeoList[inde], fnt=fntList[inde], flogic=flogicList[inde], fcombo=fcomboList[inde], falg=falgList[inde], avgcombo=avgcombo, avgnt=avgnt, avglogic=avglogic, avgalg=avgalg, avggeo=avggeo, percentile=percentile, combom=mcombo, ntm=mnt, algm=malg, geom=mgeo, logicm=mlogic)

@app.route('/admin/data/<cref>',methods=["GET","POST"])
def admindataref(cref):
  i = availableC.index(cref)
  cname = nameC[i]
  if session["Username"] in adminList:
    try:
      gsheet = admingc.open(sprdbnm)
      wsheet = gsheet.worksheet(f"{cref}")
      data = wsheet.get_all_values()
    except:
      gsheet = agcp.open(sprdbnm)
      wsheet = gsheet.worksheet(f"{cref}")
      data = wsheet.get_all_values()
    #uncomment the line below to get the values
    #return str(data)
    statusList = []
    usernameList = []
    fnameList = []
    lnameList = []
    gradeList = []
    startList = []
    sendList = []
    aendList = []
    emailList = []
    respList = []
    distribList = []
    scoreList = []
    pointList = []

    ansList = []
    p = 0
    with open(f"contest/answers/{cref}.txt", "r") as f:
      lines = f.readlines()
      for m in lines:
        ansList.append(m.replace(" ","").replace("\r","").replace("\n","").lower())

    with open(f"contest/points/{cref}.txt", "r") as f:
      lines = f.readlines()
      for m in lines:
        pointList.append(int(m.replace(" ","").replace("\r","").replace("\n","").lower()))

    for po in pointList:
      p += po

    for k in range(0,len(data)):
      if k != 0 and data[k][0] == "Finished":
        r = data[k]
        statusList.append(r[0])
        score=0
        if(r[1]=="superagh"): 		
          score+=4
        usernameList.append(r[1])
        fnameList.append(r[2])
        lnameList.append(r[3])
        gradeList.append(r[4])
        startList.append(r[5])
        sendList.append(r[6])
        aendList.append(r[7])
        emailList.append(r[8])
        sepl = []
        distrib = ""
        for j in range(0,len(r)):
          if j >= 9:
            sepl.append(r[j])
        respList.append(sepl)
        for rna in range(0,len(sepl)):
          if sepl[rna].replace(" ","").replace("\r","").replace("\n","").lower() == ansList[rna].replace(" ","").replace("\r","").replace("\n","").lower():
            distrib += "✅"
            score += pointList[rna]
          else:
            distrib += "❌"
        distribList.append(distrib)
        scoreList.append(score)


    
    fstatusList = sort_list(statusList,scoreList)
    fusernameList = sort_list(usernameList,scoreList)
    ffnameList = sort_list(fnameList,scoreList)
    flnameList = sort_list(lnameList,scoreList)
    fgradeList = sort_list(gradeList,scoreList)
    fstartList = sort_list(startList,scoreList)
    fsendList = sort_list(sendList,scoreList)
    faendList = sort_list(aendList,scoreList)
    femailList = sort_list(emailList,scoreList)
    frespList = sort_list(respList,scoreList)
    fdistribList = sort_list(distribList,scoreList)

    scoreList.sort()

    return render_template('admin/summary.html',cname=cname, username=session["Username"], av=av(session["Username"]), statusList = fstatusList, usernameList = fusernameList, fnameList = ffnameList, lnameList=flnameList, gradeList=fgradeList, startList=fstartList, sendList=fsendList, aendList=faendList, emailList=femailList, respList=frespList, distribList=fdistribList, scoreList=scoreList, maxi=p)






@app.route('/signup', methods = ['GET', 'POST'])
def signUp():
  #addRef()
  if "Username" in session:
    return redirect("/")
  if request.method == 'POST':
    req = request.form
    username = req.get('username').strip()
    password = req.get('password')
    passwordV = req.get('password verify')
    email = str(req.get('email')).lower()

    emailList = []
    for u in db.keys():
      if "db/" not in u:
        m = db[u][3]
        emailList.append(m)

    if not 1==1:
      return render_template('contest/signup.html', cap = True)

    if username == "" or password == "" or passwordV == "":
      return render_template('contest/signup.html', incomplete = True)
    elif username.replace(" ","").isalnum() == False:
      return render_template('contest/signup.html', chars = True)
    else:
      if username in db.keys():
        return render_template('contest/signup.html', usnErr = True)
      elif email in emailList:
        return render_template('contest/signup.html', mailErr = True)
      elif password != passwordV:
        return render_template('contest/signup.html', pwdErr = True)
      else:
        hashed = hashlib.sha256(password.encode())
        password = str(hashed.hexdigest())
        number = rand.randrange(10000000000000, 9999999999999999999)
        db[username] = [password, "False", "False", email,"", "", "", ["False", "Hey!", str(number)]]
        ##START VERIFICATION email
        context = ssl.create_default_context()
        html = f"""
<h1 style="color: #0c96f5; text-align: center;"><img src="https://thecalt.com/static/images/logo.png" alt="logo" width="75" height="75" /></h1>
<h1 style="color: #0c96f5; text-align: center;">TheCALT <span style="background-color: #0c96f5; color: #ffffff; padding: 0 5px; border: 1px solid #0c96f5; border-radius: 8px;">Online</span></h1>
<p>Hey {username}!</p>
<p><br />You've recently created an account at <span style="color: #00ccff;"><a href="https://contest.thecalt.com/" target="_blank" rel="noopener" title="TheCALT Online" style="color: #00ccff;">TheCALT Online</a>.</span></p>
<h4>If this was you, here is the link to verify:</h4>
<h1 style="text-align: center;"><a href="https://contest.thecalt.com/verify/{username}/{number}"><span style="background-color: #0c96f5; color: #ffffff; display: inline-block; padding: 6px 10px; border-radius: 15px;">Verify</span></a></h1>
<hr />
<p>If this wasn't you, please reply back to this email.</p>
<hr /><center><span style="color: #999999;">&copy; TheCALT 2021</span></center>
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = "TheCALT Verification"
        part2 = MIMEText(html, "html")
        message.attach(part2)
        try:
          sendermail = "thecaltonline@gmail.com"
          password = "jsfjurtotpqnkask"
          gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
          gmail_server.starttls(context=context)
          gmail_server.login(sendermail, password)
          message["From"] = "thecaltonline@gmail.com"
          message["To"] = email
          gmail_server.sendmail(sendermail, email, message.as_string())
          res = "Verification Email sent, please check your email"
        except Exception as e:
          print(e)
          res = "Verification email not sent"
          gmail_server.quit()
        ##END VERIFICATION email

        return render_template('contest/success.html', res=res)
  return render_template('contest/signup.html')


contest1 = """
                                <div class="col-lg-4 mb-4">
                                    <a href="/contest" style="text-decoration:none;"><div class="card bg-info text-white shadow">
                                        <div class="card-body">
                                          <center><img src="/static/images/logo.png" height="50" width="50"><br>
                                            Trial Contest
                                            <div class="text-white-50 small">Live Contest</div></center>
                                        </div>
                                    </div></a>
                                </div>
"""
start1 = datetime.strptime("08/17/2021 10:10:10", '%m/%d/%Y %H:%M:%S')
end1 = datetime.strptime("10/23/2021 10:10:10", '%m/%d/%Y %H:%M:%S')

"""
@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    #addRef()
    global contest1
    global start1
    global end1
    username = session["Username"]
    openc = ""

    if end1 >= datetime.now():
      if datetime.now() >= start1:
        openc += contest1

    return render_template('contest/dashboard.html', username = username, email=db[username][3], completedString = db[username][5], token=token, adminList = adminList, openc=openc, av=av(session["Username"]))
"""


@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    #addRef()
    username = session["Username"]
    openc = ""

    for k in range(0,len(availableC)):
      if (datetime.now() + timedelta(minutes=2) >= startC[k] and datetime.now() < endC[k]) or (username in adminList):
        if "Trial" in nameC[k]:
          des = "Trial Contest"
        else:
          des = "Live Contest" 
        openc += f"""
                                <div class="col-lg-4 mb-4">
                                    <a href="/checkpoint/{availableC[k]}" style="text-decoration:none;"><div class="card bg-info text-white shadow">
                                        <div class="card-body">
                                          <center><img src="/static/images/logo.png" height="50" width="50"><br>
                                            {nameC[k]}
                                            <div class="text-white-50 small">{des}</div></center>
                                        </div>
                                    </div></a>
                                </div>
"""
      

    return render_template('contest/dashboard.html', username = username, adminList = adminList, openc=openc, av=av(session["Username"]))




"""
@app.route('/contest', methods = ['GET', 'POST'])
def contest():
  #addRef()
  global problems
  global answers
  global contest1
  global start1
  global end1

  username = session["Username"]
  global points
  contestName = "Round 4"
  if datetime.now() >= start1 and datetime.now() <= end1:
    if request.method == 'GET' and db[username][1] == "False":
      if token not in db[username][5]:
        rn = datetime.now()
        timern = rn.strftime("%d/%m/%Y %H:%M:%S")
        timelimit = datetime.now() + timedelta(hours=t)
        duetime = timelimit.strftime("%Y-%m-%dT%H:%M:%SZ")

        info = [db[username][0], timern, duetime, db[username][3], db[username][4], db[username][5], db[username][6], db[username][7]]
        db[username] = info

        return render_template('contest/contest.html', problems = problems, qname = None, submitted = db[username][1], username = username, email=db[username][3], starttime = timern, duetime = duetime, av=av(session["Username"]))
      else:
        return render_template('contest/message.html', msg="You already submitted the test...", username=username, av=av(session["Username"]))

    elif request.method == 'GET' and db[username][1] != "False":
      if token not in db[username][5]:
        return render_template('contest/contest.html', problems = problems, qname = None, submitted = db[username][1], username = username, email=db[username][3], starttime = db[username][1], duetime = db[username][2], av=av(session["Username"]))
      else:
        return render_template('contest/message.html', msg="You already submitted the test...", username=username, av=av(session["Username"]))

    elif request.method == 'POST':
      req = request.form
      rn = datetime.now()
      endtime = rn.strftime("%m/%d/%Y %H:%M:%S")

      inputs = []

      ip = get('https://api.ipify.org').text

      webhook = DiscordWebhook(url="https://discord.com/api/webhooks/893328184991445023/w5_o2V_H1O2mT6xv85FBxP5uab5eC8TmjSbwVNueFZg1wbmvYGmFVPaTBE-KcHAZiTMz", username="New Version")
      embed = DiscordEmbed(
      title=f"Submission - {username}", description=f"New submission by {username}", color=242424
      )

      #st = datetime.strptime(db[username][1], '%d/%m/%Y %H:%M:%S')
      #taken = rn - st
      #supposed = db[username][2] - db[username][1]
      #if supposed >= taken:
      #  det = "Submitted within time"
      #else:
      #  det = "**WARNING: More time taken than scheduled**"
      #ftaken = taken.strftime("%m/%d/%Y %H:%M:%S")


      starttime = req.get("start")
      embed.set_footer(text="New Version")
      embed.set_timestamp()
      embed.add_embed_field(name="Username", value=username, inline=False)
      embed.add_embed_field(name="Email", value=db[username][3], inline=False)
      embed.add_embed_field(name="Time", value=f"**Started:** {starttime} \n **Ended:** {endtime}", inline=False)
      #embed.add_embed_field(name="Time Status", value=f"{det}", inline=False)
      #embed.add_embed_field(name="Time Taken", value=f"{ftaken}", inline=False)
      embed.add_embed_field(name="IP", value=ip, inline=False)
      final = ""
      score = 0
      maximum = 0

      responses = [username,db[username][3],ip]
      responses.append(starttime)
      responses.append(endtime)

      for i in range(0,len(problems)):
        s = f"Q{i}"
        res = req.get(s)
        inputs.append(res)
        if res.replace(" ", "") == answers[i]:
          final += "✅"
          det = "⎮✅"
          score += points[i]
        else:
          final += "❌"
          det = "⎮❌"

        if req.get(s) != None:
          embed.add_embed_field(name=f"A{i+1}", value=(req.get(s) + " ‍  "+det))
          responses.append(req.get(s))
        else:
          embed.add_embed_field(name=f"A{i+1}", value=("BLANK   "+det))
          responses.append(req.get(s))


        maximum += points[i]

      responses.append(final)
      responses.append(score)
      embed.add_embed_field(name="Correction Distribution", value=final, inline=False)
      embed.add_embed_field(name="Score", value=f"**{score}**/{maximum}", inline=False)

      webhook.add_embed(embed)
      response = webhook.execute()

      sc = f"**{score}**/{maximum}"




      info = [db[username][0], "False", "False", db[username][3], db[username][4], db[username][5]+token, db[username][6], db[username][7]]
      db[username] = info
      
      return render_template('contest/submitted.html', username=username, av=av(session["Username"]))
  return render_template('contest/message.html', msg="Error!", av=av(session["Username"]))
"""



@app.route('/contest/<cref>', methods=["POST"])
def contestsubs(cref):
  cref = cref.replace("#","")
  if cref in availableC:
    if request.method == "POST":
        username = session["Username"]
        i = availableC.index(cref)
        cname = nameC[i]
        dedline = endC[i]
        req = request.form
        firstname = req.get("firstname").strip()
        lastname = req.get("lastname").strip()
        grade = req.get("grade")
        ansList = []
        userList = []
        p = 0
        with open(f"contest/answers/{cref}.txt", "r") as f:
            lines = f.readlines()
            for m in lines:
              ansList.append(m)
              p += 1
        for i in range(0,p):
          userList.append(req.get(f"Q{i}").strip())
        l = db[username]
        email = l[3]
        j = db[f"db/c/{cref}"]
        rk0 = j[0]
        rk1 = j[1]
        rk2 = j[2]
        ind = rk0.index(username)
        starttime = rk1[ind]
        supposedendtime = rk2[ind]
        actualendtime = datetime.now().strftime(dformat)
        rk2[ind] = "ENDED"
        db[f"db/c/{cref}"] = [rk0,rk1,rk2]
        finallist = ["Finished",username,firstname,lastname,grade,starttime,supposedendtime,actualendtime,email]
        for an in userList:
          finallist.append(an)
        try:
          gsheet = gcs.open(sprdbnm)
          wsheet = gsheet.worksheet(f"{cref}")
          val = wsheet.col_values(1)
          wsheet.insert_row(finallist, len(val)+1)
        except:
          try:
            gsheet = gcc.open(sprdbnm)
            wsheet = gsheet.worksheet(f"{cref}")
            val = wsheet.col_values(1)
            wsheet.insert_row(finallist, len(val)+1)
          except:
            try:
              gsheet = agcs.open(sprdbnm)
              wsheet = gsheet.worksheet(f"{cref}")
              val = wsheet.col_values(1)
              wsheet.insert_row(finallist, len(val)+1)
            except:
              try:
                gsheet = agcc.open(sprdbnm)
                wsheet = gsheet.worksheet(f"{cref}")
                val = wsheet.col_values(1)
                wsheet.insert_row(finallist, len(val)+1)
              except:
                try:
                  gsheet = gcp.open(sprdbnm)
                  wsheet = gsheet.worksheet(f"{cref}")
                  val = wsheet.col_values(1)
                  wsheet.insert_row(finallist, len(val)+1)
                except:
                  try:
                    gsheet = agcp.open(sprdbnm)
                    wsheet = gsheet.worksheet(f"{cref}")
                    val = wsheet.col_values(1)
                    wsheet.insert_row(finallist, len(val)+1)
                  except:
                    try:
                      gsheet = gcs.open(sprdbnm)
                      wsheet = gsheet.worksheet(f"{cref}")
                      val = wsheet.col_values(1)
                      wsheet.insert_row(finallist, len(val)+1)
                    except:
                      gsheet = admingc.open(sprdbnm)
                      wsheet = gsheet.worksheet(f"{cref}")
                      val = wsheet.col_values(1)
                      wsheet.insert_row(finallist, len(val)+1)  

        try:
          if datetime.now() > dedline:
            username += "   [Late Submit]"
        except Exception as e:
          print(e)
        try:
                webhook = DiscordWebhook(url="https://discord.com/api/webhooks/893328184991445023/w5_o2V_H1O2mT6xv85FBxP5uab5eC8TmjSbwVNueFZg1wbmvYGmFVPaTBE-KcHAZiTMz", username="Contest Logs")
                embed = DiscordEmbed(
                  title=f"Finished Contest - {username}", description=f"{firstname} {lastname} from grade {grade} finished {cname}!", color=0x3498db
                )

                embed.set_footer(text=f"{cname}")
                embed.set_timestamp()

                webhook.add_embed(embed)
                response = webhook.execute()
        except:
                print("")

        distribution = ""
        score = 0
        for tarp in range(0,len(userList)):
          if userList[tarp].replace(" ","").replace("\r","").replace("\n","").lower() == ansList[tarp].replace(" ","").replace("\r","").replace("\n","").lower():
            distribution += "✅"
            score += 1
          else:
            distribution += "❌"

        try:
          webhook2 = DiscordWebhook(url="https://discord.com/api/webhooks/893328184991445023/w5_o2V_H1O2mT6xv85FBxP5uab5eC8TmjSbwVNueFZg1wbmvYGmFVPaTBE-KcHAZiTMz", username="Score Report")
          embed2 = DiscordEmbed(
          title=f"Score Report - {email} - {username}", description=f"{firstname} {lastname} from grade {grade} finished the contest \"{cname}\", and here is the score report at the time of submission: ", color=0x3498db
          )
          embed2.add_embed_field(name="Name", value=f"{firstname} {lastname}", inline=True)
          embed2.add_embed_field(name="Username", value=f"{username}  ", inline=True)
          embed2.add_embed_field(name="Grade", value=f"{grade}  ", inline=True)
          embed2.add_embed_field(name="Email", value=f"{email} ", inline=True)
          embed2.add_embed_field(name="Distribution", value=distribution, inline=False)
          embed2.add_embed_field(name="Score", value=f"**{score}**/{len(userList)}", inline=False)
          for dna in range(1,len(userList)+1):
            embed2.add_embed_field(name=f"Answer {dna}", value=f"Answer: {userList[dna-1]}", inline=True)
          embed2.set_footer(text=f"{cname} ")
          embed2.set_timestamp()

          webhook2.add_embed(embed2)
          response2 = webhook2.execute()
        except Exception as e:
          print(e)
                
        if "Trial" in cname:
          print("")

        #return render_template('contest/submitted.html', username=username, av=av(username), cname=cname)
        return redirect("/success/5d365f9b-14c1-49e7-ad64-328b61c0d8a7")

@app.route('/success/<k>',methods=["GET"])
def successkey(k):
  username = session["Username"]
  return render_template('contest/submitted.html', username=username, av=av(username))



@app.route('/checkpoint/<cname>', methods=["GET","POST"])
def checkpoint(cname):
  if cname in availableC:
    username = session["Username"]
    i = availableC.index(cname)
    if request.method == "GET":
      return render_template('contest/checkpoint.html', username=username, av=av(session["Username"]), cname=nameC[i], cref=cname)
    if request.method == "POST":
        username = session["Username"]
        req = request.form
        firstname = req.get("firstname").strip()
        lastname = req.get("lastname").strip()
        grade = req.get("grade")
        dedline = endC[i]
        try:
          if not ((datetime.now() + timedelta(minutes=2) >= startC[i] and datetime.now() <= endC[i]) or (username in adminList)):
            return render_template('contest/message.html', msg=f"No early starts!", username=username, av=av(session["Username"]))
        except:
          print("")
        if (datetime.now() + timedelta(minutes=2) >= startC[i] and datetime.now() <= endC[i]) or (username in adminList):
            """if cname == "team":
              oo = db[f"db/c/{cname}"]
              lim = db["db/teams"]
              rtemp = []
              for m in range(0,len(lim)):
                if username in lim[m][1]:
                  for k in lim[m][1]:
                    rtemp.append(k)
              for lol in rtemp:
                if lol in oo[0]:
                  return render_template('contest/message.html', msg=f"The user <a href=\"/user/{lol}\">{lol}</a> already began the test, so you cannot login!", username=username, av=av(session["Username"]))"""


            rn = datetime.now()
            timern = rn.strftime(dformat)
            timelimit = datetime.now() + timedelta(hours=timeC[i])
            duetime = timelimit.strftime("%Y-%m-%dT%H:%M:%SZ")

            j = list(db[f"db/c/{cname}"])
            if username not in j[0]:
              l0 = j[0]
              l0.append(username)
              l1 = j[1]
              l1.append(timern)
              l2 = j[2]
              l2.append(duetime)
              db[f"db/c/{cname}"] = [l0,l1,l2]
            l = db[f"db/c/{cname}"]
            ind = l[0].index(username)
            if l[2][ind] != "ENDED":
              ps = []
              with open(f"contest/problems/{cname}.txt", "r") as f:
                lines = f.readlines()
                for m in lines:
                  ps.append(m)

              try:
                webhook = DiscordWebhook(url="https://discord.com/api/webhooks/893328184991445023/w5_o2V_H1O2mT6xv85FBxP5uab5eC8TmjSbwVNueFZg1wbmvYGmFVPaTBE-KcHAZiTMz", username="Contest Logs")
                embed = DiscordEmbed(
                  title=f"Started Contest - {username}", description=f"{firstname} {lastname} from grade {grade} started {nameC[i]}!", color=0x3498db
                )

                embed.set_footer(text=f"{nameC[i]}")
                embed.set_timestamp()

                webhook.add_embed(embed)
                response = webhook.execute()
              except:
                print("")

              
              kk = db[f"db/c/{cname}"][2][ind]
              kk1 = datetime.strptime(kk,"%Y-%m-%dT%H:%M:%SZ")
              ofin = kk
              if kk1 > dedline:
                ofin = dedline.strftime("%Y-%m-%dT%H:%M:%SZ")
              else:
                ofin = kk

              return render_template('contest/contest.html', problems = ps, qname = None, username = username, duetime = ofin, av=av(session["Username"]), cref=cname, cname=nameC[i], firstname=firstname, lastname=lastname, grade=grade)
            else:
              return render_template('contest/message.html', msg="You already submitted the test...", username=username, av=av(session["Username"]))
        


@app.route('/profile', methods = ['GET', 'POST'])
def profile():
  #addRef()
  username = session["Username"]
  olist = db[username][7]
  if request.method == "POST":
    #print(session['apptheme'])
    newlist = []
    req = request.form
    determine = req.get("determine")
    appearance = ""
    appearance = req.get("appearance").strip()
    #session.permanent = True
    print("o.o.o.o.o.o")
    stat = req.get("stat")
    if determine == "yes":
      newlist.append("True")
    elif determine == "no":
      newlist.append("False")
    newlist.append(stat)
    newlist.append(olist[2])
    info = [db[username][0],db[username][1],db[username][2],db[username][3],db[username][4],db[username][5],db[username][6],newlist]
    db[username] = info
    session['apptheme'] = appearance
    session.permanent = True
    appear = session["apptheme"]
    return redirect('/profile')


  status = db[username][4]

  listpref = db[username][7]
  oldstat = listpref[1]


  ident = ""
  tag = ""
  avurl = ""
  if username in adminList:
    a = "🔵 "
  else:
    a = ""
  if db[username][6] == "":
    des = False
  else:
    des = True

  if db[username][6] != "":
    try:
      discord = OAuth2Session(client_id, token=db[username][6])
      response = discord.get(base_discord_api_url + '/users/@me')
      ident = response.json()['id']
      av1 = response.json()['avatar']
      avurl = "https://cdn.discordapp.com/avatars/" + ident + "/" + av1
      tag = response.json()['username'] + "#" + response.json()['discriminator']
    except Exception as e:
      print("Error in Logging in with Discord!")
      des = False

  ang = "Sync"
  if 'apptheme' in session:
    ang = session['apptheme']
  else:
    ang = "Sync"


  return render_template('contest/profile.html', status=status,email=db[username][3],username=username, prefix=a, avatar=avurl, tag=tag, des=des, oldstat=oldstat, av=av(session["Username"]), ident=ident, ang=ang)



@app.errorhandler(404)
def page_not_found(e):
    #addRef()
    return render_template('/main/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    #addRef()
    return render_template('/main/500.html'), 500

#code to initiate new reaper season
#db["db/reaper/s1"] = []
# START A NEW REAPER GAME
#db["db/reaper/s1"] = [["Game Started!",0,datetime.strftime(datetime.now(), rdformat)]]


def verifyReaperAccess(u):
  k = ""
  t = ""
  for i in db["db/reaper/s1"]:
    k = i[0]
    if u == i[0]:
      t = i[2]
  if t == "":
    return True
  if k == "":
    return True
  if k == u:
    return False
  if (datetime.utcnow() -  datetime.strptime(t, rdformat)).total_seconds() < reaperDiff:
    return False
  return True

def generateLb():
  uList = []
  fuser = []
  fscore = []
  favg = []
  final = []
  for k in db["db/reaper/s1"]:
    if k[0] not in uList:
      if k[0] != "Game Started!":
        uList.append(k[0])
  
  for n in uList:
    s = 0
    t = 0
    for k in db["db/reaper/s1"]:
      if n == k[0]:
        s += k[1]
        t += 1
    fuser.append(n)
    fscore.append(s)
    favg.append(s/t)
  
  suser = sort_list(fuser,fscore)
  savg = sort_list(favg,fscore)
  fscore.sort()

  for k in range(0,len(suser)):
    final.append([suser[k],round(savg[k],3),fscore[k]])
  return final

@socketio.on("reaper verify")
def reaperverify(json):
  username = session["Username"]
  if verifyReaperAccess(username):
    #emit('reaper verify', {"result":"True"})
    return {"status": True}
  else:
    #emit('reaper verify', {"result":"False"})
    return {"status": False}
#[username, score, time]

def reaperEnded():
  k = generateLb()
  k.reverse()
  for m in k:
    if m[2] >= reaperLimit:
      return True
  return False

@socketio.on("reaper ended")
def reaperend(json):
  username = session["Username"]
  if reaperEnded():
    return {"status": True}
  else:
    return {"status": False}



@socketio.on("modresponse")
def modresponse(json):
  try:
    if session["Username"] == json['name']:
        course=json['course']
        if course in courseRef:
          ind = courseRef.index(course)
          username = session["Username"]
          capi = S1(courseClassDb[ind])
          modList = capi.get("modlist")
          if username in modList:
            #if capi.get("modstatus") == "false":
            classnum = capi.get("classnum")
            cnum = classnum[len(classnum)-1]
            if json['show'] == "true":
              a = capi.get(f"class{cnum}")
              l = []
              for i in range(0,len(a)):
                if i != json['index']:
                  l.append(a[i])
                else:
                  l.append([a[i][0],a[i][1],"true",a[i][3]])
              capi.set(f"class{cnum}",l)
              msgname = a[json['index']][0]
              msgmessage = a[json['index']][1]
              emit("response",{"name":msgname,"message":msgmessage,"mod":"true", "course":json['course']}, broadcast=True)
              emit("changetick",json,broadcast=True)
            if json['show'] == "false":
              print("donzo")
              a = capi.get(f"class{cnum}")
              l = []
              for i in range(0,len(a)):
                if i != json['index']:
                  l.append(a[i])
                else:
                  l.append([a[i][0],a[i][1],"false",a[i][3]])
              capi.set(f"class{cnum}",l)
              msgname = a[json['index']][0]
              msgmessage = a[json['index']][1]
              emit("removemsg",{"name":msgname,"message":msgmessage,"mod":"false", "course":json['course']}, broadcast=True)
              emit("changetick",json,broadcast=True)
            #else:
            #  classnum = capi.get("classnum")
            #  cnum = classnum[len(classnum)-1]
            #  a = capi.get(f"class{cnum}")
            #  a.append([f"{json['name']}",f"{json['message']}","false",""])
            #  capi.set(f"class{cnum}",a)
            #  emit("modresponse",{"name":json['name'],"message":json['message'],"mod":"false", "course":json['course']}, broadcast=True)
  except:
    print("error")







@socketio.on("changemodstatus")
def changemodstatus(json):
  try:
    if session["Username"] == json['name']:
        course=json['course']
        if course in courseRef:
          ind = courseRef.index(course)
          username = session["Username"]
          capi = S1(courseClassDb[ind])
          modList = capi.get("modlist")
          if username in modList:
            
            
            if json['mod'] == "true":
              a = capi.get("modstatus")
              if a != "true":
                capi.set("modstatus","true")
                emit("changemodstatus",{"mod":"true", "course":json['course'], "name":json['name']}, broadcast=True)
            if json['mod'] == "false":
              a = capi.get("modstatus")
              if a != "false":
                capi.set("modstatus","false")
                emit("changemodstatus",{"mod":"false", "course":json['course'], "name":json['name']}, broadcast=True)       

  except:
    print("error")



@socketio.on("updateclassconfig")
def updateclassconfig(json):
  try:
    if session["Username"] == json['name']:
        course=json['course']
        if course in courseRef:
          ind = courseRef.index(course)
          username = session["Username"]
          capi = S1(courseClassDb[ind])
          modList = capi.get("modlist")
          if username in modList:
            finalmods = []
            finalbans = []
            newmods = json['moderator'].replace(" ","").replace("\t","").replace("\r","").split("\n")
            newbans =  json['banned'].replace(" ","").replace("\t","").replace("\r","").split("\n")
            for i in newmods:
              if i != "":
                finalmods.append(i)
            for j in newbans:
              if j != "":
                finalbans.append(j)

            ##SOCKET SENDING FOR MOD/BANNED AND UPDATING THE DB
            if username in adminList:
              capi.set("bannedlist",finalbans)
              capi.set("modlist",finalmods)
              retbans = capi.get("bannedlist")
              retmods = capi.get("modlist")

              sbans = ""
              smods = ""
              for i in retbans:
                sbans += i
                sbans += "\n"
              for i in retmods:
                smods += i
                smods += "\n"

              emit("changeclasslists",{"newlist":retbans, "course":json['course'], "type":"ban", "s":sbans, "name":json['name']}, broadcast=True)
              emit("changeclasslists",{"newlist":retmods, "course":json['course'], "type":"mod", "s":smods, "name":json['name']}, broadcast=True)

            currclassnum = capi.get("classnum")
            currcnum = currclassnum[len(currclassnum)-1]
            newnumber = int(json['classnumber'])
            if newnumber != currcnum:
              currclassnum.append(newnumber)
              capi.set("classnum",currclassnum)
              if f"class{newnumber}" not in capi.get_keys():
                capi.set(f"class{newnumber}",[])
              newmessages = capi.get(f"class{newnumber}")
              emit("changeclassnum",{"newmessages":newmessages, "course":json['course'], "num":f"{newnumber}", "name":json['name']}, broadcast=True)



  except Exception as e:
    print(e)





@socketio.on("message")
def message(json):
  try:
    #print(str(json))
    if session["Username"] == json['name'] and len(json['message']) != 0:
      course=json['course']
      if course in courseRef:
        ind = courseRef.index(course)
        capi = S1(courseClassDb[ind])
        modList = capi.get("modlist")
        if (len(json['message']) <= 256) or (session["Username"] in modList):
          allowedList = courseSignups[ind]
          username = session["Username"]
          if username in allowedList or username in modList:
            
            capi = S1(courseClassDb[ind])
            if capi.get("modstatus") == "false" or username in modList:
              classnum = capi.get("classnum")
              cnum = classnum[len(classnum)-1]
              a = capi.get(f"class{cnum}")
              a.append([f"{json['name']}",f"{json['message']}","true",""])
              capi.set(f"class{cnum}",a)
              emit("response",{"name":json['name'],"message":json['message'],"mod":"true", "course":json['course']}, broadcast=True)
              emit("modresponse",{"name":json['name'],"message":json['message'],"mod":"true", "course":json['course']}, broadcast=True)
            else:
              classnum = capi.get("classnum")
              cnum = classnum[len(classnum)-1]
              a = capi.get(f"class{cnum}")
              a.append([f"{json['name']}",f"{json['message']}","false",""])
              capi.set(f"class{cnum}",a)
              emit("modresponse",{"name":json['name'],"message":json['message'],"mod":"false", "course":json['course']}, broadcast=True)
  except:
    print("error")






@socketio.on("modmessage")
def modmessage(json):
  try:
    if session["Username"] == json['name'] and len(json['message']) != 0:
      course=json['course']
      if course in courseRef:
        ind = courseRef.index(course)
        capi = S1(courseClassDb[ind])
        modList = capi.get("modlist")
        if (session["Username"] in modList):
          username = session["Username"]
          if username in modList:
              emit("modmessage",{"name":json['name'],"message":json['message'], "course":json['course']}, broadcast=True)
  except:
    print("error")


@socketio.on("dmuser")
def dmuser(json):
  try:
    if session["Username"] == json['name'] and len(json['message']) != 0:
      course=json['course']
      if course in courseRef:
        ind = courseRef.index(course)
        capi = S1(courseClassDb[ind])
        modList = capi.get("modlist")
        if (session["Username"] in modList):
          username = session["Username"]
          if username in modList:
              emit("dmuser",{"name":json['name'],"message":json['message'], "course":json['course'], "target":json['target']}, broadcast=True)
  except:
    print("error")  














@socketio.on("iconnected")
def iconnected(json):
  try:
    #print(str(json))
    if session["Username"] == json['name']:
      course=json['course']
      if course in courseRef:
        ind = courseRef.index(course)
        allowedList = courseSignups[ind]
        capi = S1(courseClassDb[ind])
        modList = capi.get("modlist")
        username = session["Username"]
        if username in allowedList or username in modList:
          
#          if json['name'] not in modList:
          emit("iconnected",json, broadcast=True)
#          else:
#            emit("iconnected",{'name':f'<i class=\"fas fa-crown\"></i> {json["name"]}', 'course':json['course']}, broadcast=True)
#
          capi = S1(courseClassDb[ind])
          a = capi.get(f"userlist")
          if json['name'] not in a:
#            if json['name'] in modList:
#              a.append(f'<i class=\"fas fa-crown\"></i> {json["name"]}')
#            else:
              a.append(json['name'])
          capi.set(f"userlist",a)
  except:
    print("error")

@socketio.on("idisconnected")
def idisconnected(json):
  try:
    #print(str(json))
    if session["Username"] == json['name']:

      course=json['course']
      if course in courseRef:
        ind = courseRef.index(course)
        allowedList = courseSignups[ind]
        capi = S1(courseClassDb[ind])
        modList = capi.get("modlist")
        username = session["Username"]
        if username in allowedList or username in modList:

#          if json['name'] not in modList:
          emit("idisconnected",json, broadcast=True)
#          else:
#            emit("idisconnected",{'name':f'<i class=\"fas fa-crown\"></i> {json["name"]}', 'course':json['course']}, broadcast=True)

          capi = S1(courseClassDb[ind])
          a = capi.get(f"userlist")
          if json['name'] in a:
            while json['name'] in a:
#              if json['name'] in modList:
#                a.remove(f'<i class=\"fas fa-crown\"></i> {json["name"]}')
#              else:
                a.remove(json['name'])
                print(a)
          capi.set(f"userlist",a)

  except:
    print("error")



@socketio.on("shutrest")
def shutrest(json):
  username = session["Username"]
  emit("shutrest", {"user":json["user"]}, broadcast=True, include_self=False)

@socketio.on("ijustreapedlol")
def ijustreapedlol(json):
  #print(str(json))
  rn = datetime.utcnow()
  a = getLatest()
  t = a[2]
  diff = math.floor((rn-datetime.strptime(t,rdformat)).total_seconds())
  username = session['Username']
  if verifyReaperAccess(username) and reaperEnded() == False:
    if verifyReaperAccess(username) and reaperEnded() == False:
        l = db["db/reaper/s1"]
        l.append([username,diff,datetime.strftime(rn,rdformat)])
        db["db/reaper/s1"] = l
        emit("upd",{"name":username,"sec":diff, "newtime":datetime.strftime(rn,rdformat)},broadcast=True)
        s = ""
        m = generateLb()
        m.reverse()
        for k in m:
          s += f"""
              <tr>
                <td>{k[0]}</td>
                <td>{k[1]}</td>
                <td>{k[2]}</td>
              </tr>
          """
        emit("updatelb",{"data":s},broadcast=True)



@socketio.on('onfocus')
def onfocus(json):
      username = session["Username"]
      firstname = json['firstname']
      lastname = json['lastname']
      cname = json['cname']
      webhook = DiscordWebhook(url="https://discord.com/api/webhooks/893328184991445023/w5_o2V_H1O2mT6xv85FBxP5uab5eC8TmjSbwVNueFZg1wbmvYGmFVPaTBE-KcHAZiTMz", username="AntiCheet")
      embed = DiscordEmbed(
      title=f"Back on Focus - {username}", description=f"{firstname} {lastname} is back on focus! \n **Contest Name:** {cname}", color=0x2ecc71
      )

      embed.set_footer(text=f"{cname}")
      embed.set_timestamp()
      #embed.add_embed_field(name="Username", value=username, inline=False)

      webhook.add_embed(embed)
      response = webhook.execute()

@socketio.on('lostfocus')
def lostfocus(json):
      username = session["Username"]
      firstname = json['firstname']
      lastname = json['lastname']
      cname = json['cname']
      webhook = DiscordWebhook(url="https://discord.com/api/webhooks/893328184991445023/w5_o2V_H1O2mT6xv85FBxP5uab5eC8TmjSbwVNueFZg1wbmvYGmFVPaTBE-KcHAZiTMz", username="AntiCheet")
      embed = DiscordEmbed(
      title=f"Lost Focus - {username}", description=f"{firstname} {lastname} lost focus! \n **Contest Name:** {cname}", color=0xe74c3c
      )

      embed.set_footer(text=f"{cname}")
      embed.set_timestamp()
      #embed.add_embed_field(name="Username", value=username, inline=False)

      webhook.add_embed(embed)
      response = webhook.execute()







#app.run(host='0.0.0.0', port=8080)
socketio.run(app, host='0.0.0.0', port=8080)