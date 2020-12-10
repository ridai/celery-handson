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
構成イメージは以下の通り<br>
<img width="500" src="https://user-images.githubusercontent.com/2268153/101658520-72262d80-3a88-11eb-828c-0ae43bf433a3.png"><br>
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
<img width="500" src="https://user-images.githubusercontent.com/2268153/101657990-e3191580-3a87-11eb-8518-604e66f03830.png"><br>
taskを実行するbackendサーバに、djangoに組み込むことが用意な`Celery`を利用している。<br>
非同期処理を実行するbackendサーバにtaskの実行命令をpushするために、brokerと呼ばれるメッセージのqueueingシステムが必要になる。今回は`Redis`を利用している。<br>
backendサーバでのtask実行結果を格納する必要がある。今回は`Redis`を利用しているが、`MySQL`等も選択可能である。<br>

また、今回も、動作の説明のために、djangoのserverを **シングルスレッド** かつ **1プロセス** での動作を行っている。

### 手順
1. 以下のブランチをチェックアウトする
```shell
git checkout -b step2 oring/step2
```

2. 環境を立ち上げる
```
$docker-compose build
$docker-compose up
```

3. ブラウザで`localhost:8000/handson`にアクセスし、ボタンを押してみる。この時、chromeであればデベロッパーツールでレスポンスをチェックできるようにしておく。
<img width="500" src="https://user-images.githubusercontent.com/2268153/101653395-a1d23700-3a82-11eb-8219-a07154ed878d.png">

4. Buttonをクリックして、レスポンスが即時返ることを確認する

### 解説
1. 非同期処理の導入手順
    1. Redisをbrokerとして利用するため、redis serviceを用意する。
    docker-composeを以下のように修正。
    ```
    redis:
        image: redis:6.0.9
    ```
    また、djangoにおいて、brokerとして認識させる。
    appのsettings.pyに以下設定を追加。
    ```
    CELERY_BROKER_URL = "redis://redis:6379/1"
    ```
    2. Celeryの利用にあたっては
        1. taskロジック自体はdjangoに組み込まれているため、handson-webapp serviceと同じく、djangoのimageをbuildしたcelery serviceを用意する。
        docker-composeを以下のように修正。
        ```
          celery:
            build:
              context: ./handson-webapp
              args:
                BUILD_TAG: 3.7
        ```
        1. 非同期処理を実行するプロセスをdaemonとして立ち上げるためには、celeryの機能を使って以下コマンドを叩く。
        docker-composeを以下のように修正。
        ```
            command: celery -A app worker --concurrency=1 -l info
        ```
        concurrencyは並列処理数。今回はお試しなので 1。
    3. 実行結果の格納先情報を記載する。
    appのsettings.pyに以下設定を追加。
    ```
    CELERY_RESULT_BACKEND = 'redis://redis:6379'
    ```
2. 非同期スクリプトの実装方法
    1. celery用のdecolaterを事前に読み込むために、`app.__init__.py`に以下内容を記述する
    ```
    from __future__ import absolute_import, unicode_literals

    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery import app as celery_app

    __all__ = ('app',)
    ```
    2. appディレクトリ配下に、celery.py, tasks.pyを用意する
    3. celery.pyは以下の内容で記述。アプリケーションによって、変更と書かれている場所を修正すること。
    ```
    # celery.py
    from __future__ import absolute_import, unicode_literals

    import os

    from celery import Celery

    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'app.settings' # 変更1: アプリケーションのsettingsを指定
    )

    app = Celery('app')  # 変更2: appに変更

    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    app.config_from_object(
        'django.conf:settings',
        namespace='CELERY'
    )

    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()


    @app.task(bind=True)
    def debug_task(self):
        print('Request: {0!r}'.format(self.request))

    ```
    4. tasks.pyには、非同期で実行させたいpythonコードを好きに書く。この時、`@shared_task`デコレータを指定することで非同期スクリプトであると明示する必要がある。
    ```
    from __future__ import absolute_import, unicode_literals
    from celery import shared_task

    import time

    @shared_task
    def hello(proj_id):
        time.sleep(10)
        print('hello')
    ```
    5. 上記のtasks.pyをviews.pyから呼び出す。この時、`hoge.delay(args)`と書くことで非同期処理が実行される。
    ```
        def post(self, request, *args, **kwargs):
        hello.delay('hello world') # 非同期処理を呼び出す場合はdeleyメソッドを叩く
        return redirect(reverse("base"))
    ```
