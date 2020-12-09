# celery-handson
## 目次
1. [概要](#anchor1)
1. [Step1](#anchor2)
1. [Step2](#anchor3)

<a id="anchor1"></a>
## 概要
 Celeryの使い方を理解するためのハンズオン資料です。
  
<a id="anchor2"></a>
## Step.1
### 概要
単純なリクエストエンドポイントを叩いて、ロジックの実行をX秒待たせる<br>
X秒間レスポンス待ちが発生することを確認する<br>
今回は、動作の説明のために、djangoのserverを **シングルスレッド** かつ **1プロセス** での動作を行っている。

### 手順
1. 以下のブランチをチェックアウトする
```shell
git checkout -b step1 oring/step1
```

2. 環境を立ち上げる
```
$docker-compose build
$docker-compose up
```

3. ブラウザで`localhost:8000/handson`にアクセスし、ボタンを押してみる。この時、chromeであればデベロッパーツールでレスポンスをチェックできるようにしておく。
<img width="500" src="https://user-images.githubusercontent.com/2268153/101653395-a1d23700-3a82-11eb-8219-a07154ed878d.png">

4. Buttonをクリックして、レスポンスが返るまで10秒以上かかることを確認する

### 解説
views.pyにて、ボタンを押した際のエンドポイントが`TaskStep1` クラスで定義されており、このクラス内でレスポンスを返す前に10秒sleepしている処理があることがわかる。<br>
```
    def post(self, request, *args, **kwargs):
        # レスポンスを10秒待つ
        time.sleep(10)
        return redirect(reverse("base"))
```

ボタンを押したあと、別tabで`localhost:8000/handson`にアクセスしようとするとレスポンスが返ってこないことも確認できる。

<a id="anchor3"></a>
## Step.2
### 概要
処理時間がかかるような処理をフロントで待ち続けないように & フロントエンドサーバのリソースを食いつぶさないためにも、別コンテナでの非同期処理を導入する<br>
celery + redisの登場<br>
構成イメージは以下の通り<br>
<img width="500" src="https://user-images.githubusercontent.com/2268153/101657990-e3191580-3a87-11eb-8518-604e66f03830.png">

今回も、動作の説明のために、djangoのserverを **シングルスレッド** かつ **1プロセス** での動作を行っている。

### 手順
1. 以下のブランチをチェックアウトする
```shell
git checkout -b step2 oring/step2
```
