#
# twitterアカウントのフォロー一覧を取得する
# 取得した一覧の最新のツイートのタイムスタンプを取得する
# リストを作成する
# 更新が無いアカウントをリストに登録し、フォローを外す
# リスト一覧を取得する
# 命名規則にあうリストがあれば、そのリストの中を検索する
# もし更新があったアカウントがあれば、フォローしなおして、リストから除外する
#

import json

file=open('config/app.settings.json','r')
app = json.load(file)
file=open('config/owners.settings.json','r')
owners = json.load(file)


print(owners["account"])

#for owner in owners:
#  print(owner["account"])

