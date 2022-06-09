# -*- coding: utf-8 -*-
import sys
import datetime
import time
import pprint
from time import sleep
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta

API_LIMIT = 429
API_CORRECT = 200
API_CANNOT_ADD = 403


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
    if res.status_code == API_CORRECT:
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

    sleep(3)

    if res.status_code == API_LIMIT:
        pause_service()
    if res.status_code == API_CORRECT:
        # TODO : とりあえず全て成功したとみなす
        params = {"user_id": user_id}
        # TODO: 例外処理を組み込む
        # TODO : とりあえず全て成功したとみなそう
        res = oauth.post(app["end_point"]["remove_friend"], params=params)

        sleep(3)

        if res.status_code == API_LIMIT:
            pause_service()
        if res.status_code != API_CORRECT:
            if res.status_code != API_CANNOT_ADD:
                api_res_error(sys._getframe().f_code.co_name, res)
    else:
        api_res_error(sys._getframe().f_code.co_name, res)


def un_archive_friend(app, user_id, list_id, oauth):
    # フォローする
    params = {"user_id": user_id,
              "follow": app["friends"]["follow"]}
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["add_friend"], params=params)

    sleep(3)

    if res.status_code == API_LIMIT:
        pause_service()
    if res.status_code == API_CORRECT:
        # TODO: 例外処理を組み込む
        # TODO : とりあえず全て成功したとみなそう
        params = {"user_id": user_id,
                  "list_id": list_id}
        res = oauth.post(app["end_point"]["remove_friend_list"], params=params)

        sleep(3)

        if res.status_code == API_LIMIT:
            pause_service()
        if res.status_code != API_CORRECT:
            api_res_error(sys._getframe().f_code.co_name, res)
    else:
        api_res_error(sys._getframe().f_code.co_name, res)


def pause_service():
    sleep(60 * 15)


def format_time_stamp(created_at):
    struct_time = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    return datetime(*struct_time[:6])


def api_res_error(func, res):
    print("[warn]" + func + " status_code:" + str(res.status_code))
    #print("error_code:" + format(res.text["errors"]["code"]) + " error_msg:" + format(res.text["errors"]["message"]))


def api_request(res):
    if res.status_code == API_LIMIT:
        pause_service()
    if res.status_code == API_CORRECT:
        return True
    else:
        api_res_error(sys._getframe().f_code.co_name, res)
        return False
