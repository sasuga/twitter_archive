# twitter_archive

## Description

- twitterでフォローをしているが、tweetが無いアカウントがある。一定期間tweetが無いアカウントはリストfriend_archivesを作成してその中に移動し、一旦フォローを外す。

- 諸事情によりtweetできないケースもあるので、フォローを外したリストを検索して、tweetが再開されたアカウントに対して再度フォローをした上でリストから外す。

- バッチは月1度走る事とする。（cronかLambdaで設定）

- n日以内にtweetが無いケースでリスト化する。（default:90日）

- リスト命名は「friend_archives」とする。

- 複数のtwitterアカウントに対応する。

## 進捗メモ
- Pythonを学びながら実装を開始
- 進捗率90％
- 鍵垢対策をしなければいけない。リストには追加するが、removeはしない事にしよう。
- loggerを組み込みたい
- このプログラミングが終わったら、俺、Django立ち上げて、twitterソーシャルログインで誰でも使えるようにするんだ…

## Issue
- logger埋め込み
- protect user対策
- API error 403対応
