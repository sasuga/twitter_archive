# -*- coding: utf-8 -*-
import sys
import datetime
from time import sleep
from requests_oauthlib import OAuth1Session
API_LIMIT = 429
API_CORRECT = 200


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


def is_response_ok(response):
    if response.status_code != API_CORRECT:
        if response.status_code == API_LIMIT:
            pause_service()
    else:
        return True


def lists_read(owner, app, oauth):
    params = {"screen_name": owner["screen_name"],
              "count": app["list"]["count"]}
    # TODO: 例外処理を組み込む
    return oauth.get(app["end_point"]["find_list"], params=params)


# TODO: 要動作確認
def api_access(ep, type, auth, params):
    if type == "GET":
        response = auth.get(ep, params=params)
    else:
        response = auth.post(ep, params=params)

    if response.status_code == API_CORRECT:
        return json.loads(respons.text)
    else:
        return False


def create_list(listname, app, oauth):
    params = {"name": listname,
              "mode": app["list"]["mode"],
              "description": "twitter_archives auto create"
              }
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["create_list"], params)
    if res.status_code != API_CORRECT:
        if res.status_code == API_LIMIT:
            pause_service()
    body = json_loads(res.text)
    return body["id"]


def archive_friend(app, user_id, list_id, oauth):

    # リストに突っ込む
    params = {"list_id": list_id,
              "user_id": user_id}
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["put_friend_list"], params=params)
    if res.status_code == API_LIMIT:
        pause_service()
    if res.status_code == API_CORRECT:
        # TODO : とりあえず全て成功したとみなそう
        params = {"user_id": user_id}
        # TODO: 例外処理を組み込む
        # TODO : とりあえず全て成功したとみなそう
        res = oauth.post(app["end_point"]["remove_friend"], params=params)
        if res.status_code == API_LIMIT:
            pause_service()


def un_archive_friend(app, user_id, list_id, oauth):
    # フォローする
    params = {"user_id": user_id,
              "follow": app["friends"]["follow"]}
    # TODO: 例外処理を組み込む
    res = oauth.post(app["end_point"]["add_friend"], params=params)
    if res.status_code == API_LIMIT:
        pause_service()
    if res.status_code == API_CORRECT:
        # TODO : とりあえず全て成功したとみなそう

        # TODO: 例外処理を組み込む
        # TODO : とりあえず全て成功したとみなそう
        # リストから外す
        params = {"user_id": user_id,
                  "list_id": list_id}
        res = oauth.post(app["end_point"]["remove_friend_list"], params=params)
        if res.status_code == API_LIMIT:
            pause_service()


def pause_service():
    print("sleep mode start:")
    print(datetime.datetime.now())
    sleep(60 * 15)
    print("sleep mode end:")
    print(datetime.datetime.now())
