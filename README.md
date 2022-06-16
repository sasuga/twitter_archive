# twitter_archive

## Description

- twitterでフォローをしているが、tweetが無くなるアカウントがある。一定期間tweetが無いアカウントはリストfriend_archivesを作成してその中に移動し一旦フォローを外す。（フレンド数上限対策）

- 諸事情によりtweetできないケースもあるので、フォローを外したリストを検索して、tweetが再開されたアカウントに対して再度フォローをした上でリストからは外す。

- バッチは月1度走る事とする。（cronかLambdaで設定予定）

- n日以内にtweetが無いケースでリスト化する。（default:90日）

- リスト命名は「friend_archives」とする。

- 複数のtwitterアカウントに対応する。

## Memo
- Pythonを学びながら実装を開始
- 進捗率90％

## Issue
- logger埋め込み
- リトライ実装
