# celery-handson
### 概要
 Celeryの使い方を理解するためのハンズオン資料です。
  
### Step.1
#### 概要
単純なリクエストエンドポイントを叩いて、ロジックの実行をX秒待たせる<br>
X秒間レスポンス待ちが発生することを確認する<br>
今回は、動作の説明のために、djangoのserverを **シングルスレッド** かつ **1プロセス** での動作を行っている。

#### 手順
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
<img width="500" alt="スクリーンショット 2020-12-10 0 56 29" src="https://user-images.githubusercontent.com/2268153/101653395-a1d23700-3a82-11eb-8219-a07154ed878d.png">

4. Buttonをクリックして、レスポンスが返るまで10秒以上かかることを確認する

#### 解説
views.pyにて、ボタンを押した際のエンドポイントが`TaskStep1` クラスで定義されており、このクラス内でレスポンスを返す前に10秒sleepしている処理があることがわかる。<br>
```
    def post(self, request, *args, **kwargs):
        # レスポンスを10秒待つ
        time.sleep(10)
        return redirect(reverse("base"))
```

ボタンを押したあと、別tabで`localhost:8000/handson`にアクセスしようとするとレスポンスが返ってこないことも確認できる。
