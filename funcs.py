# -*- coding: utf-8 -*-
import datetime
import sys
from requests_oauthlib import OAuth1Session

def file_read(f):
  try:
      config = open(f,'r')
  except IndexError:
      print("config file not found.")
  except IOError:
      print("config file not found.")
  else:
      return config

def twitter_auth(owner):
    # TODO: 例外処理を組み込む
    oauth=OAuth1Session(owner["TWI_CK"],
                        owner["TWI_CS"],
                        owner["TWI_AT"],
                        owner["TWI_ATS"])
    return oauth

def create_list_name(header):
    now = datetime.datetime.now()
    str_now=now.strftime('%Y%m%d')
    return header+str_now

def is_response_ok(response):
    if(response.status_code!=200):
        print("強制終了：エラーコード："+str(response.status_code))
        sys.exit()
    else:
        return True

def lists_read(owner,app,oauth):
    params = {  "screen_name":owner["screen_name"],
                "count":app["list"]["count"]}
    # TODO: 例外処理を組み込む
    return oauth.get(app["end_point"]["find_list"],params=params)

#def findlist(ownerid):
