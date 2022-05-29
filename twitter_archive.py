# -*- coding: utf-8 -*-
#
# twitterアカウントのフォロー一覧を取得する
# 取得した一覧の最新のツイートのタイムスタンプを取得する
# 更新が無いアカウントをRリストに登録し、フォローを外す
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
import functions #original

file = functions.fileRead('config/app.settings.json')
app = json.load(file)
file = functions.fileRead('config/owners.settings.json')
owners = json.load(file)
accounts = owners["accounts"]

for owner in accounts:
    oauth=functions.twitterauth(owner["TWI_CK"] ,
                                owner["TWI_CS"] ,
                                owner["TWI_AT"] ,
                                owner["TWI_ATS"])
    listname = functions.createlistname(app["list"]["header"])

  #既に同じ名前のリストが無いか確認


    params = {  "name":listname,
                "mode":app["list"]["mode"],
                "description":"twitter_archive auto create"
                }

    res = oauth.post(app["endpoint"]["create_list"],params)
    if res.status_code==200:
        print("OK")
    else:
        print("NG")
