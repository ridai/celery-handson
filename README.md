# celery-handson
### 概要
 Celeryの使い方を理解するためのハンズオン資料です。
  
### Step.1
#### 概要
単純なリクエストエンドポイントを叩いて、ロジックの実行をX秒待たせる<br>
X秒間レスポンス待ちが発生することを確認する<br>

#### 手順
1. 以下のブランチをチェックアウトする
```shell
git checkout -b step1 oring/step1
```
1. 環境を立ち上げる
```
$docker-compose build
$docker-compose up
```
1. ブラウザで`localhost:8000/handson`にアクセスし、ボタンを押してみる。この時、chromeであればデベロッパーツールでレスポンスをチェックできるようにしておく。
