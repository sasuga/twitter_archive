#
# twitterアカウントのフォロー一覧を取得する
# 取得した一覧の最新のツイートのタイムスタンプを取得する
# 更新が無いアカウントをリストに登録し、フォローを外す
# リスト一覧を取得する
# 命名規則にあうリストがあれば、そのリストの中を検索する
# もし更新があったアカウントがあれば、フォローしなおして、リストから除外する
# memo
#	app.archive.interval
#	app.list.header
#	app.list.modeIsPublic
#       app.list.endpoint.create_list
#       app.list.endpoint.xxxxxxxxxx
##

import json
import datetime
from requests_oauthlib import OAuth1Session

file=open('config/app.settings.json','r')
app = json.load(file)
#file=open('config/owners.settings.json','r')
file=open('config/owners.settings.json.dev','r')
owners = json.load(file)
accounts = owners["accounts"]

for owner in accounts:
  CK = owner["TWI_CK"]
  CS = owner["TWI_CS"]
  AT = owner["TWI_AT"]
  ATS= owner["TWI_ATS"]
  oauth=OAuth1Session(CK,CS,AT,ATS)

  now = datetime.datetime.now()
  str_now=now.strftime('%Y%m%d') 
  params = {"name":app["list"]["header"]+str_now,
            "mode":app["list"]["mode"],
            "description":"twitter_archive auto create at "+str_now
           }

  res = oauth.post(app["endpoint"]["create_list"],params)
  if res.status_code==200:
    print("OK")
  else:
    print("NG")

