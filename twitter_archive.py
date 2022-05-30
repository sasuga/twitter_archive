# -*- coding: utf-8 -*-
#
# *リストを作成する
# *twitterアカウントのフォロー一覧を取得する
# 取得した一覧の最新のツイートのタイムスタンプを取得する
# 更新が無いアカウントをRリストに登録し、フォローを外す
# リスト一覧を取得する
# 命名規則にあうリストがあれば、そのリストの中を検索する
# もし更新があったアカウントがあれば、フォローしなおして、リストから除外する
# memo
#	app.archive.interval
#	app.list.header
#	app.list.modeIsPublic
#       app.list.end_point.create_list
#       app.list.end_point.xxxxxxxxxx
##

import json
import sys
import pprint # 4DEBUG:

from datetime import datetime

import funcs #original


file = funcs.file_read('config/app.settings.json')
app = json.load(file)
file = funcs.file_read('config/owners.settings.json.dev')
owners = json.load(file)
accounts = owners["accounts"]

for owner in accounts:
    #リスト作成処理
    oauth=funcs.twitter_auth(owner)
    listname = funcs.create_list_name(app["list"]["header"])

    res = funcs.lists_read(owner,app,oauth)
    if funcs.is_response_ok(res):
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
            # TODO: 例外処理を組み込む
            res = oauth.post(app["end_point"]["create_list"],params)
            if res.status_code!=200:
                sys.exit("強制終了：エラーコード："+str(res.status_code))

    #フォロー一覧取得処理
    # TODO: 良い感じにリファクタリングしたい
    params = {  "screen_name":owner["screen_name"],
                "count":app["friends"]["count"],
                "stringify_ids":app["friends"]["stringify_ids"]}
    # TODO: 例外処理を組み込む
    res = oauth.get(app["end_point"]["get_friend_list"],params=params)
    if funcs.is_response_ok(res):
        body = json.loads(res.text)
        friends = []
        friends.extend(body["ids"])

        while body['next_cursor'] != 0:
            params = {  "screen_name":owner["screen_name"],
                        "count":app["friends"]["count"],
                        "stringify_ids":app["friends"]["stringify_ids"],
                        "cursor":body["next_cursor"]
                    }
            res = oauth.get(app["end_point"]["get_friend_list"],params=params)
            # TODO: 例外処理を組み込む
            if funcs.is_response_ok(res):
                body = json.loads(res.text)
                friends.extend(body["ids"])


    #フォロワーの最新のツイートを取得する
    for user_id in friends:
        params = {  "user_id":user_id,
                    "count":app["tweet"]["count"],
                    "exclude_replies":app["tweet"]["exclude_replies"],
                    "include_rts":app["tweet"]["include_rts"]
                }
        # TODO: 例外処理を組み込む
        res = oauth.get(app["end_point"]["get_friend_tweet"],params=params)

        if funcs.is_response_ok(res):
            body = json.loads(res.text)

            # body["created_at"]のコンバートで失敗している。

            #created_at = datetime.strptime(body["created_at"], '%a %b %d %H:%M:%S %z %Y')
            #print(created_at)
            #print(str(body["created_at"]))
            #print(json.dumps(body, indent=2))
            sys.exit()

#print(json.dumps(data, indent=2))
