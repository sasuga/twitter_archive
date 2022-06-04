# twitter_archive

## Description

- twitterでフォローをしているが、tweetが無いアカウントがある。一定期間tweetが無いアカウントはリストfriend_archivesを作成してその中に移動し、一旦フォローを外す。

- 諸事情によりtweetできないケースもあるので、フォローを外したリストを検索して、tweetが再開されたアカウントに対して再度フォローをした上でリストから外す。

- バッチは月1度走る事とする。（cronかLambdaで設定）

- n日以内にtweetが無いケースでリスト化する。（default:90日）

- リスト命名は「friend_archives」とする。

- 複数のtwitterアカウントに対応する。

## memo
- リストfriend_archivesを作成する
- twitterアカウントのフォロー一覧を取得する
- 取得した一覧の最新のツイートのタイムスタンプを取得する
- 更新が無いアカウントをリストに登録し、フォローを外す
- リスト-タイムラインを取得する
- 最新のtweetから日付比較を行い、n日以内にtweetがあったアカウントをフォローしなおしてリストからは除外する。

## 進捗メモ
- Pythonを学びながら実装を開始
- 進捗率70％
- API制限かかるようになってきた…
- 1000人のフォロアーに対してプログラムをかけ、998人はアーカイブ対象ってのは、どこか判定がおかしいのでデバッグしている
- このプログラミングが終わったら、俺、Django立ち上げて、twitterソーシャルログインで誰でも使えるようにするんだ…
