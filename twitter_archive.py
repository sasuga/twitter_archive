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
import sys
import functions #original

file = functions.fileRead('config/app.settings.json')
app = json.load(file)
file = functions.fileRead('config/owners.settings.json.dev')
owners = json.load(file)
accounts = owners["accounts"]

for owner in accounts:
    oauth=functions.twitterauth(owner["TWI_CK"] ,
                                owner["TWI_CS"] ,
                                owner["TWI_AT"] ,
                                owner["TWI_ATS"])
    listname = functions.createlistname(app["list"]["header"])

    params = {  "screen_name":owner["screen_name"],
                "count":app["list"]["count"],
                "reverse":app["list"]["reverse"]}

    #TODO:例外処理を組み込む
    res = oauth.get(app["endpoint"]["find_list"],params=params)

    if res.status_code==200:
        #リスト
        has_identical_name=False
        body = json.loads(res.text)
        body = body["lists"]

        for i,listlist in enumerate(body):
            if listlist["name"]==listname:
                has_identical_name=True
        if has_identical_name==False:
            params = {  "name":listname,
                        "mode":app["list"]["mode"],
                        "description":"twitter_archive auto create"
                        }
            #TODO 例外処理を組み込む
            res = oauth.post(app["endpoint"]["create_list"],params)
            if res.status_code!=200:
                sys.exit()
    else:
        sys.exit()





        #data = json.loads(res)
        #print(json.dumps(data, indent=2))


    #res = oauth.post(app["endpoint"]["create_list"],params)
    #if res.status_code==200:
    #    print("OK")
    #else:
    #    print("NG")
