# twitter_archive

## Description

twitterのフォロワーが一杯なのだが、中には更新が無いアカウントがたくさんある。
- 一定期間更新が無いアカウントはリストを作成してその中に移動し、フォローを外す。

- 諸事情によりtweetできないケースもあるので、フォローを外したリストを検索して、ttweetが再開されたアカウントに対して再度フォローをした上でリストから外す。

- バッチは月1度走る事とする。（cronかLambdaで設定）

- n日以内にtweetが無いケースでリスト化する。

- リスト命名は「archive_YYYYMMDD」とする。

- 複数のtwitterアカウントに対応する。

