# -*- coding: utf-8 -*-
#
# *リストを作成する
# *twitterアカウントのフォロー一覧を取得する
# *取得した一覧の最新のツイートのタイムスタンプを取得する
# *更新が無いアカウントをRリストに登録し、フォローを外す
# *リスト一覧を取得する
# *命名規則にあうリストがあれば、そのリストの中を検索する
# *もし更新があったアカウントがあれば、フォローしなおして、リストから除外する

import json
import sys
import pprint  # 4DEBUG:
import time
from datetime import datetime, timedelta
import funcs  # original

file = funcs.file_read('config/app.settings.json')
app = json.load(file)
file = funcs.file_read('config/owners.settings.json.dev')
owners = json.load(file)
accounts = owners["accounts"]

for owner in accounts:
    # リスト作成処理
    oauth = funcs.twitter_auth(owner)
    listname = app["list"]["name"]

    res = funcs.lists_read(owner, app, oauth)
    if funcs.is_response_ok(res):
        # リスト
        list_id = 0
        body = json.loads(res.text)
        body = body["lists"]

        for i, listlist in enumerate(body):
            if listlist["name"] == listname:
                list_id = listlist["id"]
        if list_id == 0:
            list_id = funcs.create_list(listname, app, oauth)

    # フォロー一覧取得処理
    # TODO: 良い感じにリファクタリングしたい
    params = {"screen_name": owner["screen_name"],
              "count": app["friends"]["count"],
              "stringify_ids": app["friends"]["stringify_ids"]}
    # TODO: 例外処理を組み込む
    res = oauth.get(app["end_point"]["get_friend_list"], params=params)
    if funcs.is_response_ok(res):
        body = json.loads(res.text)
        friends = []
        friends.extend(body["ids"])

        while body['next_cursor'] != 0:
            params["cursor"] = body["next_cursor"]
            res = oauth.get(app["end_point"]["get_friend_list"], params=params)
            # TODO: 例外処理を組み込む
            if funcs.is_response_ok(res):
                body = json.loads(res.text)
                friends.extend(body["ids"])

    # フォロワーの最新のツイートを取得する
    counter = 0
    archive_count = 0
    for user_id in friends:
        # print(user_id)
        counter += 1
        params = {"user_id": user_id,
                  "count": app["tweet"]["count"],
                  "exclude_replies": app["tweet"]["exclude_replies"],
                  "include_rts": app["tweet"]["include_rts"]
                  }
        # TODO: 例外処理を組み込む
        res = oauth.get(app["end_point"]["get_friend_tweet"], params=params)


        if funcs.is_response_ok(res):
            body = json.loads(res.text)
            if len(body) == 0:
                archive_count += 1
                funcs.archive_friend(app, owners, user_id, list_id,oauth)
            else:
                struct_time = time.strptime(
                    body[0]["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
                last_tw_dt = datetime(*struct_time[:6])
                if datetime.now() > last_tw_dt + timedelta(days=90):
                    archive_count += 1
                    funcs.archive_friend(app, owners, user_id, list_id,oauth)

    print("count:" +
          str(counter) +
          "  archive:" +
          str(archive_count))
#print(json.dumps(data, indent=2))
