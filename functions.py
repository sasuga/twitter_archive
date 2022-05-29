# -*- coding: utf-8 -*-
import datetime
from requests_oauthlib import OAuth1Session

def fileRead(f):
  try:
      config = open(f,'r')
  except IndexError:
      print("config file not found.")
  except IOError:
      print("config file not found.")
  else:
      return config

def twitterauth(CK,CS,AT,ATS):
    oauth=OAuth1Session(CK,CS,AT,ATS)
    return oauth

def createlistname(header):
    now = datetime.datetime.now()
    str_now=now.strftime('%Y%m%d')
    return header+str_now
