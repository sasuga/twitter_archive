# -*- coding: utf-8 -*-
import sys
import datetime
import time
import pprint
import json
from time import sleep
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta

API_LIMIT = 429
API_CORRECT = 200
API_CANNOT_ADD = 403
API_CANNOT_REMOVE = 400


def file_read(f):
    try:
        config = open(f, 'r')
    except IndexError:
        print("config file not found.")
    except IOError:
        print("config file not found.")
    else:
        return config


def twitter_auth(owner):
    # TODO: 例外処理を組み込む
    oauth = OAuth1Session(owner["TWI_CK"],
                          owner["TWI_CS"],
                          owner["TWI_AT"],
                          owner["TWI_ATS"])
    return oauth


def lists_read(owner, app, oauth):
    params = {"screen_name": owner["screen_name"],
              "count": app["list"]["count"]}
    # TODO: 例外処理を組み込む
    return oauth.get(app["end_point"]["find_list"], params=params)


def create_list(listname, app, oauth):
    params = {"name": listname,
              "mode": app["list"]["mode"],
              "description": "twitter_archives auto create"
              }
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["create_list"], params=params)

    if res.status_code == API_LIMIT:
        pause_service()
        res = oauth.post(app["end_point"]["create_list"], params=params)
    if res.status_code == API_CORRECT:
        pprint.pprint(res)
        body = json_loads(res.text)
        return body["id"]
    else:
        api_res_error(sys._getframe().f_code.co_name, res)
    # TODO: リスト作成エラーが起きた時の対処


def archive_friend(app, user_id, list_id, oauth):
    params = {"list_id": list_id,
              "user_id": user_id}
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["put_friend_list"], params=params)
    if res.status_code == API_LIMIT:
        pause_service()
        res = oauth.post(app["end_point"]["put_friend_list"], params=params)

    if res.status_code == API_CORRECT:
        # TODO : 例外処理
        params = {"user_id": user_id}
        res = oauth.post(app["end_point"]["remove_friend"], params=params)

        if res.status_code == API_LIMIT:
            pause_service()
            res = oauth.post(app["end_point"]["remove_friend"], params=params)

        if res.status_code != API_CORRECT:
            if res.status_code != API_CANNOT_ADD:
                print("line:84")
                api_res_error(sys._getframe().f_code.co_name, res)
            # else:
            #    # 4DEBUG アーカイブできなかったエラー
            #    error_cnt += 1
    else:
        if res.status_code != API_CANNOT_ADD:
            print("line:91")
            api_res_error(sys._getframe().f_code.co_name, res)


def un_archive_friend(app, user_id, list_id, oauth):
    # フォローする
    params = {"user_id": user_id,
              "follow": app["friends"]["follow"]}
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["add_friend"], params=params)
    if res.status_code == API_LIMIT:
        pause_service()
        res = oauth.post(app["end_point"]["add_friend"], params=params)

    if res.status_code == API_CORRECT:
        # TODO: 例外処理を組み込む
        # TODO : とりあえず全て成功したとみなそう
        params = {"user_id": user_id,
                  "list_id": list_id}
        res = oauth.post(app["end_point"]["remove_friend_list"], params=params)

        if res.status_code == API_LIMIT:
            pause_service()
            res = oauth.post(
                app["end_point"]["remove_friend_list"], params=params)

        if res.status_code != API_CORRECT:
            if res.status_code != API_CANNOT_REMOVE:
                print("line:118")
                api_res_error(sys._getframe().f_code.co_name, res)
            # else:
            #    error_cnt += 1
    else:
        if res.status_code != API_CANNOT_REMOVE:
            print("line:123")
            api_res_error(sys._getframe().f_code.co_name, res)


def pause_service():
    print("*** sleep.start()")
    sleep(60 * 15)
    print("*** sleep.end()")


def format_time_stamp(created_at):
    struct_time = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    return datetime(*struct_time[:6])


def api_res_error(func, res):
    print(str(res.status_code) + ":" + sys._getframe().f_code.co_name)


def echo_owner_info(cnt, archive_cnt, un_archive_cnt, owner_no, err_cnt):
    # 4DEBUG
    print("------------------------------")
    print(str(owner_no) + "人目のユーザアカウント")
    print("follow:" + str(cnt))
    print("archive:" + str(archive_cnt))
    print("un_archive:" + str(un_archive_cnt))
    print("error_cnt:" + str(err_cnt))
