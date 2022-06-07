# -*- coding: utf-8 -*-

import json
import sys
# import pprint  # 4DEBUG:
import time
from datetime import datetime, timedelta
import funcs  # original

counter = 0
archive_count = 0
list_id = 0
friends = []


def init4owner():
    counter = 0
    archive_count = 0
    list_id = 0
    friends = []


# 設定ファイル読み込み
file = funcs.file_read('config/app.settings.json')
app = json.load(file)
file = funcs.file_read('config/owners.settings.json.dev')
#file = funcs.file_read('config/owners.settings.json')
owners = json.load(file)
accounts = owners["accounts"]
listname = app["list"]["name"]


for owner in accounts:
    init4owner()
    oauth = funcs.twitter_auth(owner)

    # リストが無ければ作成
    res = funcs.lists_read(owner, app, oauth)
    if res.status_code == funcs.API_LIMIT:
        funcs.pause_service()
    if res.status_code == funcs.API_CORRECT:
        # リスト
        body = json.loads(res.text)
        lists = body["lists"]

        for i, listlist in enumerate(lists):
            if listlist["name"] == listname:
                list_id = listlist["id"]
        if list_id == 0:
            list_id = funcs.create_list(listname, app, oauth)
    else:
        funcs.api_res_error(sys._getframe().f_code.co_name, res)
    # フォロー一覧取得処理
    params = {"screen_name": owner["screen_name"],
              "count": app["friends"]["count"],
              "stringify_ids": app["friends"]["stringify_ids"]}
    # TODO: 例外処理を組み込む
    res = oauth.get(app["end_point"]["get_friend_list"], params=params)
    if res.status_code == funcs.API_LIMIT:
        funcs.pause_service()
    if res.status_code == funcs.API_CORRECT:
        body = json.loads(res.text)
        friends.extend(body["ids"])
        # フレンドが5000人以上の時の処理
        while body['next_cursor'] != 0:
            params["cursor"] = body["next_cursor"]
            res = oauth.get(app["end_point"]["get_friend_list"], params=params)
            # TODO: 例外処理を組み込む
            if res.status_code == funcs.API_LIMIT:
                funcs.pause_service()
            if funcs.status_code == funcs.API_CORRECT:
                body = json.loads(res.text)
                friends.extend(body["ids"])
            else:
                funcs.api_res_error(sys._getframe().f_code.co_name, res)
    # フォロワーの最新のツイートを取得する
    for user_id in friends:
        counter += 1
        params = {"user_id": user_id,
                  "count": app["tweet"]["count"],
                  "exclude_replies": app["tweet"]["exclude_replies"],
                  "include_rts": app["tweet"]["include_rts"]
                  }
        # TODOs: 例外処理を組み込む
        res = oauth.get(app["end_point"]["get_friend_tweet"], params=params)
        if res.status_code == funcs.API_LIMIT:
            funcs.pause_service()
        if res.status_code == funcs.API_CORRECT:
            body = json.loads(res.text)
            if len(body) == 0:
                archive_count += 1
                funcs.archive_friend(app, user_id, list_id, oauth)
            else:
                last_tw_dt = funcs.format_time_stamp(body[0]["created_at"])
                if datetime.now() > last_tw_dt + timedelta(days=app["archive"]["interval"]):

                    params = {
                        "user_id": user_id
                    }
                    res = oauth.get(
                        app["end_point"]["get_user_profile"], params=params)
                    if res.status_code == funcs.API_LIMIT:
                        funcs.pause_service()
                    if res.status_code == funcs.API_CORRECT:
                        body = json.loads(res.text)
                        if body["protected"] == False:
                            archive_count += 1
                            funcs.archive_friend(app, user_id, list_id, oauth)
                        # else:
                        #    funcs.api_res_error(sys._getframe().f_code.co_name,res)
                    else:
                        funcs.api_res_error(
                            sys._getframe().f_code.co_name, res)
        else:
            funcs.api_res_error(sys._getframe().f_code.co_name, res)

    # リストのタイムラインを取得する
    params = {
        "list_id": list_id,
        "count": app["list"]["count"],
        "include_rts": app["list"]["include_rts"],
        "include_entities": app["list"]["include_entities"]
    }
    res = oauth.get(app["end_point"]["get_list_timeline"], params=params)
    if res.status_code == funcs.API_LIMIT:
        funcs.pause_service()
    if res.status_code == funcs.API_CORRECT:
        body = json.loads(res.text)

        for tweet in body:
            last_tw_dt = funcs.format_time_stamp(tweet["created_at"])
            if datetime.now() < last_tw_dt + timedelta(days=app["archive"]["interval"]):
                funcs.un_archive_friend(app, user_id, list_id, oauth)
            else:
                break
    else:
        funcs.api_res_error(sys._getframe().f_code.co_name, res)

    print("account:" + owner["screen_name"] + "  friends count:" +
          str(counter) + "  archive:" + str(archive_count))
