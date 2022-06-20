# django-docker-redis-tutorial

 django-docker-redis-tutorial 基本教學  📝

* [Youtube Tutorial Part1 - docker 安裝 redis 以及 redis 基本指令](https://youtu.be/BhO2ADEj_EE)

* [Youtube Tutorial Part2 - django-redis 以及 redis api 介紹](https://youtu.be/fX_3UTKgjI8)

* [Youtube Tutorial Part3 - redis 應用場合以及實戰](https://youtu.be/xFNkpyd4Ues)

## 前言

![alt tag](https://i.imgur.com/lVNQWVV.png)

Redis 是 open source，也是 in-memory data structure store ( key-value )，常被使用在 database、cache 、

message broker，像是可以透過 cache 減輕 database 的壓力 ( redis 讀寫速度比一般的 database 快非常多 )，

而 message broker 可以用在像是 Celery 的應用（ Celery 的應用可參考我之前寫的 [django-celery-tutorial](https://github.com/twtrubiks/django-celery-tutorial) 以及

[docker-django-celery-tutorial](https://github.com/twtrubiks/docker-django-celery-tutorial)。

透過這篇文章，你將會學會

* [透過 docker 安裝 redis](https://github.com/twtrubiks/django-docker-redis-tutorial#%E9%80%8F%E9%81%8E-docker-%E5%AE%89%E8%A3%9D-redis)
* [redis 基本指令](https://github.com/twtrubiks/django-docker-redis-tutorial#redis-%E5%9F%BA%E6%9C%AC%E6%8C%87%E4%BB%A4)
* [django-redis 介紹](https://github.com/twtrubiks/django-docker-redis-tutorial#django-redis)
* [透過 low-level cache API 把玩 redis](https://github.com/twtrubiks/django-docker-redis-tutorial#%E9%80%8F%E9%81%8E-low-level-cache-api-%E6%8A%8A%E7%8E%A9-redis)
* [redis 應用場合](https://github.com/twtrubiks/django-docker-redis-tutorial#redis-%E6%87%89%E7%94%A8%E5%A0%B4%E5%90%88)

## 教學

* [Youtube Tutorial Part1 - docker 安裝 redis 以及 redis 基本指令](https://youtu.be/BhO2ADEj_EE)

在開始教學前，建議大家可以先閱讀官方的 [Redis Persistence](https://redis.io/topics/persistence) ，

裡面詳細的介紹了 **RDB persistence** 以及 **AOF persistence** 的觀念，這兩個觀念很重要:+1:

### 透過 docker 安裝 redis

[docker redis](https://hub.docker.com/_/redis/)

請在命令提示字元 ( cmd ) 直接執行以下指令

```cmd
docker run --name some-redis  -p 6379:6379  -d redis redis-server --appendonly yes
```

如果要設定密碼

```cmd
docker run --name some-redis  -p 6379:6379  -d redis redis-server --appendonly yes --requirepass "changeme"
```

以上這段指令，比較需要特別解釋的就是 `--appendonly`，當如果你沒有設定時，

假如今天斷電或是不小心意外終止 redis，可能會遺失當下的資料，如果我們設定了 Append-only file ( AOF )，

AOF 預設的 policy 是每秒寫入一次 ( 當然，還是有可能會遺失一秒的資料，但相對比 RDB ( Snapshotting，

因為預設的是存在硬碟上，binary file 為 dump.rdb，所以稱為 RDB )，AOF 比起 RDB 有更好的 Persistence 。

當選擇使用 AOF 時 ，如果重起 redis，會依照 AOF 去重新建立狀態。

更多詳細資料可參考 [append-only-file](https://redis.io/topics/persistence#append-only-file)。

或是直接使用 [docker-compose.yml](docker-compose.yml).

### redis 基本指令

確認建立完成後，即可使用 redis-cli 開始玩 redis

```cmd
docker exec -it <container name> redis-cli
```

如果你有設定密碼要加上 `-a`

```cmd
docker exec -it <container name> redis-cli -a changeme
```

更多 redis 可參考 [redis command](https://redis.io/commands/) 以及支援的 [redis data-types](https://redis.io/docs/manual/data-types/)。

```cmd
127.0.0.1:6379> ping
PONG
```

set key

```cmd
127.0.0.1:6379> set id twtrubiks
OK
```

get key

```cmd
127.0.0.1:6379> get id
"twtrubiks"
```

exists key，更多可參考 [EXISTS key](https://redis.io/commands/exists)

```cmd
# if the key exists.
127.0.0.1:6379> exists id
(integer) 1
# if the key does not exist.
127.0.0.1:6379> exists not_exist
(integer) 0
```

設定 key 一個有效時間 ( Redis 常常拿來當做是 Cache )，更多可參考 [EXPIRE key seconds](https://redis.io/commands/expire)

```cmd
127.0.0.1:6379> set name twtrubiks
OK
127.0.0.1:6379> get name
"twtrubiks"
127.0.0.1:6379> expire name 10
(integer) 1
127.0.0.1:6379> get name
"twtrubiks"
# Wait for 10 seconds and try again
127.0.0.1:6379> get name
(nil)
```

刪除 key，更多可參考 [DEL key](https://redis.io/commands/del)

```cmd
127.0.0.1:6379> set num 1
OK
127.0.0.1:6379> del num
(integer) 1
127.0.0.1:6379> get num
(nil)
```

一次刪除全部的 key

```cmd
127.0.0.1:6379> flushall
OK
```

得到目前全部的 keys，更多可參考 [KEYS pattern](https://redis.io/commands/keys)

```cmd
keys *
```

TTL key，查看目前還剩多久時間會 timeout，

更多可參考 [TTL key](https://redis.io/commands/ttl)

```cmd
127.0.0.1:6379> set name twtrubiks_ttl
OK
127.0.0.1:6379> expire name 10
(integer) 1
# Wait for 4 seconds and try again
127.0.0.1:6379> ttl name
(integer) 6
```

PERSIST key，將 key 從 volatile ( a key with an expire set )  轉變成

persistent ( a key that will never expire as no timeout is associated )，

說白話一點，就是將 key 轉變成永遠不會過期 ( timeout )，更多可參考 [PERSIST key](https://redis.io/commands/persist)

```cmd
127.0.0.1:6379> set mykey hello
OK
127.0.0.1:6379> expire mykey 20
(integer) 1
# Wait for 5 seconds and try again
127.0.0.1:6379> ttl mykey
(integer) 15
127.0.0.1:6379> persist mykey
(integer) 1
127.0.0.1:6379> TTL mykey
(integer) -1
#  -1 if the key exists but has no associated expire.
```

選擇資料庫，有 16 個資料庫 ( 0-15 )，預設是第 0 個資料庫，

如下方範例為切換到第一個資料庫，

```cmd
127.0.0.1:6379> select 1
OK
127.0.0.1:6379[1]>
```

redis 非常適合投票這種使用情境，可參考以下範例

```cmd
# 投給 a 一票
127.0.0.1:6379> zincrby vote 1 a
"1"
# 投給 b 兩票
127.0.0.1:6379> zincrby vote 2 b
"2"
# 投給 a 三票
127.0.0.1:6379> zincrby vote 3 a
"4"
# 查看 a 總投票數
127.0.0.1:6379> zscore vote a
"4"
# 得到 a 排名 ( 由高到低 )
127.0.0.1:6379> zrevrank vote a
(integer) 0
# 得到 b 排名 ( 由高到低 )
127.0.0.1:6379> zrevrank vote b
(integer) 1
# 得到前10名 ( 由高到低 )
127.0.0.1:6379> zrevrange vote 0 9
1) "a"
2) "b"
# 得到前10名以及對應的分數 ( 從高到低 )
127.0.0.1:6379> zrevrange vote 0 9 withscores
1) "a"
2) "4"
3) "b"
4) "2"
```

由於 redis command 很多，這邊不可能一一介紹，所以更詳細的可參考 [commands](https://redis.io/commands/):smile:

## django-redis

* [Youtube Tutorial Part2 - django-redis 以及 redis api 介紹](https://youtu.be/fX_3UTKgjI8)

接下來和大家介紹 [django-redis](https://github.com/jazzband/django-redis) 這個套件，

我將簡單介紹他的使用方法，請先安裝套件

```python
pip install django-redis
```

接著在 [settings.py](https://github.com/twtrubiks/django-docker-redis-tutorial/blob/master/django_docker_redis_tutorial/settings.py) 中加入下方程式碼

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

Django 預設的 session 是存放在 database 中，但這邊要將他修改成 redis ，

修改的方式很簡單，只需要將 SESSION_ENGINE 改成 `django.contrib.sessions.backends.cache` 即可，

Configure as session backend，在 [settings.py](https://github.com/twtrubiks/django-docker-redis-tutorial/blob/master/django_docker_redis_tutorial/settings.py) 中加入下方程式碼

```python
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

詳細的 Session 參數介紹，可參考 Django 官網的 [sessions](https://docs.djangoproject.com/en/4.0/topics/http/sessions/) 文件，

設定完成後，Session 將會儲存在 redis 中（ 速度更快 ），

如果你不了解 Session ，可以參考我之前寫的這篇 [Session](https://github.com/twtrubiks/CSRF-tutorial#session)，

Session 存在 redis 中的範例，後面我會再介紹給各位。

有時候我們可能需要 access 原生的 Redis 功能，所以這時候就需要採用下面的方式使用 redis，

```python
>>> from django_redis import get_redis_connection
>>> con = get_redis_connection("default")
>>> con
<redis.client.StrictRedis object at 0x2dc4510>
```

可參考 [Raw client access](https://github.com/jazzband/django-redis#raw-client-access)

## 透過 low-level cache API 把玩 redis

官方文件可參考 [The low-level cache API](https://docs.djangoproject.com/en/4.0/topics/cache/#the-low-level-cache-api)，

直接使用 Python Console 操作以下指令，

`set(key, value, timeout)`

```python
>>> from django.core.cache import cache
>>> cache.set('my_key', 'hello, world!')
True
>>> cache.get('my_key')
'hello, world!'
```

`set(key, value, timeout)` and `get(key)`

timeout 如果沒設定或是設定為 None 時，資料將為 forever

```python
>>> from django.core.cache import cache
>>> cache.set('my_key', 'hello, world!')
True
>>> cache.get('my_key')
'hello, world!'
```

設定 timeout 為 10 秒

```python
>>> from django.core.cache import cache
>>> cache.set('key_test', 'hello, world test !',10)
True
## if key_test has expired ( not exist ) , show has expired
>>> cache.get('key_test', 'has expired')
'hello, world test !'
## Wait 10 seconds for 'my_key' to expire...
>>> cache.get('key_test', 'has expired')
'has expired'
```

`add()`

如果這個 key 不存在，就會設定指定的 key，如果 key 已經存在，則**不會更新**既有的 key 值

```python
>>> cache.set('my_key', 'hello, world!')
True
>>> cache.get('my_key')
'hello, world!'
>>> cache.add('my_key','demo')
>>> cache.get('my_key')
'hello, world!'
>>> cache.add('my_key_2','test2')
True
```

`get_or_set()`

可以使用這個來取得 ( 設定 ) key 值 ， 假如這個 key 不存在 ，就設定 key 值 ，如果存在就將 key 值顯示出來

```python
>>> cache.get('my_new_key')
>>> cache.get_or_set('my_new_key', 'my new value')
'my new value'
```

`set_many()` and `get_many()`

```python
>>> cache.set_many({'a': 1, 'b': 2, 'c': 3})
>>> cache.get_many(['a', 'b', 'c'])
OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```

`delete()` and `delete_many()`

```python
>>> cache.delete('a')
1
>>> cache.delete_many(['a', 'b', 'c'])
2
```

`clear()`

```python
>>> cache.clear()
```

`incr()` and `decr()`

```python
>>> cache.set('num', 1)
True
>>> cache.incr('num')
2
>>> cache.incr('num', 10)
12
>>> cache.decr('num')
11
cache.decr('num',2)
9

# A ValueError will be raised if you attempt to increment or decrement a nonexistent cache key
cache.get('test')
cache.decr('test',2)
>>> ValueError: Key ':1:tst' not found
```

### Cache versioning

[Cache versioning](https://docs.djangoproject.com/en/4.0/topics/cache/#cache-versioning)

`incr_version()` and `decr_version()`

```python
# default version =1
>>> cache.set('my_key', 'hello world!')
True
>>> cache.get('my_key',version=1)
'hello world!'
>>> cache.get('my_key',version=2)

# incr_version
>>> cache.incr_version('my_key')
2
>>> cache.get('my_key',version=2)
'hello world!'
>>> cache.get('my_key',version=1)

>>> cache.set('my_key', 'test', version=1)
True
>>> cache.get('my_key',version=1)
'test'
>>> cache.get('my_key',version=2)
'hello world!'
```

接著可以使用 redis-cli 觀看，

```cmd
127.0.0.1:6379> keys *
1) ":1:my_key"
2) ":2:my_key"
```

有沒有發現一件事情，我們明明設定的是 `cache.set('my_key', 'test', version=1)`，

但為什麼透過 django 設定的 key 都會變成  `":1:my_key"` 這樣的格式呢 ？

原因是因為 django cache 本身的機制，

[default.py#L706](https://github.com/jazzband/django-redis/blob/master/django_redis/client/default.py#L706)

```python
def make_key(
    self, key: Any, version: Optional[Any] = None, prefix: Optional[str] = None
) -> CacheKey:
    if isinstance(key, CacheKey):
        return key

    if prefix is None:
        prefix = self._backend.key_prefix

    if version is None:
        version = self._backend.version

    return CacheKey(self._backend.key_func(key, prefix, version))
```

django 使用 make_key 建立新的 key ，原始的 key 在 `_backend.key_func` 裡。

[base.py#L31](https://github.com/django/django/blob/main/django/core/cache/backends/base.py#L31)

```python
def default_key_func(key, key_prefix, version):
    """
    Default function to generate keys.
    Construct the key used by all other methods. By default, prepend
    the `key_prefix`. KEY_FUNCTION can be used to specify an alternate
    function with custom key making behavior.
    """
    return "%s:%s:%s" % (key_prefix, version, key)


def get_key_func(key_func):
    """
    Function to decide which key function to use.
    Default to ``default_key_func``.
    """
    if key_func is not None:
        if callable(key_func):
            return key_func
        else:
            return import_string(key_func)
    return default_key_func


class BaseCache:
    _missing_key = object()

    def __init__(self, params):
        timeout = params.get("timeout", params.get("TIMEOUT", 300))
        if timeout is not None:
            try:
                timeout = int(timeout)
            except (ValueError, TypeError):
                timeout = 300
        self.default_timeout = timeout

        options = params.get("OPTIONS", {})
        max_entries = params.get("max_entries", options.get("MAX_ENTRIES", 300))
        try:
            self._max_entries = int(max_entries)
        except (ValueError, TypeError):
            self._max_entries = 300

        cull_frequency = params.get("cull_frequency", options.get("CULL_FREQUENCY", 3))
        try:
            self._cull_frequency = int(cull_frequency)
        except (ValueError, TypeError):
            self._cull_frequency = 3

        self.key_prefix = params.get("KEY_PREFIX", "")
        self.version = params.get("VERSION", 1)
        self.key_func = get_key_func(params.get("KEY_FUNCTION"))
```

這也就是為什麼透過 django 設定的 key 都會變成 `%s:%s:%s` 這樣的格式了。

## redis 應用場合

* [Youtube Tutorial Part3 - redis 應用場合以及實戰](https://youtu.be/xFNkpyd4Ues)

redis 可以應用的場合真的非常的多，這次的 demo 將使用到以下情境 ( 其他的情境大家可以再自行 google 了解 )，

* 統計頁面點擊數

當需要記錄頁面的瀏覽次數（ 或點擊數 ）時，就非常適合使用 redis，為什麼不使用 db 呢 ？

因為假如有非常大量的人瀏覽（ 或點擊 ）網頁時，可能會導致 db 的鎖互搶，影響到效能。

關於鎖這部份，可以稍微參考一下我之前寫的 [django-transactions-tutorial](https://github.com/twtrubiks/django-transactions-tutorial)，裡面有稍微

提到部分的概念。

images/[views.py](https://github.com/twtrubiks/django-docker-redis-tutorial/blob/master/images/views.py) 中片段程式碼

```python
cache.get_or_set('click', 0, timeout=None)
total_views = cache.incr('click')
```

這段程式碼相當簡單，當你瀏覽到這個頁面時，就將 `click` 這個 key 加一，

然後就可以統計出目前有多少人瀏覽過你的頁面 ( 聰明的你現在一定想到，

那我就一直瘋狂 F5 不就可以一直刷瀏覽數量了嗎 ？沒錯，但這個問題大家

可以自行想想，這邊只是帶給大家簡單的概念 )。

* 排行榜

前面介紹 redis 適合投票這種情境，當然，也適合排行榜這種使用情境，

images/[views.py](https://github.com/twtrubiks/django-docker-redis-tutorial/blob/master/images/views.py) 中片段程式碼

```python
def index(request):
    ......
    rank = con.zrevrange(name='images', start=0, end=9, withscores=True, score_cast_func=int)
    rank_seq = [
        {"url": str(r[0], 'utf-8'),
         "value": r[1]}
        for r in rank
    ]

    return render(request, 'images/index.html', {
        'images': images_seq,
        'total_views': total_views,
        'ranks': rank_seq,
    })


def detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    total_views = con.zincrby(name='images', amount=1 ,value=image.url)
    return render(request,
                  'images/detail.html', {
                      'image': image,
                      'total_views': int(total_views)
                  })

```

在 `detail` 中，我們將圖片的 url 存到 images 這個 key 值中，並且給他加一，

在 `index` 中，透過 `zrevrange` 這個方法統計目前圖片被瀏覽次數的排名。

* Session Cache

為了方便介紹，這邊直接使用登入 admin 後台來觀察 session，直接瀏覽 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) ，

預設的帳號密碼為 ( twtrubiks / password123 )，

登入後你會發現，你的 redis 多了 session 的 key 值（ 而 database 中沒有增加 ），如下圖

redis 中多了 session 的 key

![alt tag](https://i.imgur.com/5KwryHN.png)

![alt tag](https://i.imgur.com/sb9esxq.png)

如果沒特別另外設定，django 預設是存放在 database  ( django_session 表格 )，

這邊是空的很正常，因為我們已經設定 redis 了，

![alt tag](https://i.imgur.com/TjdAq8y.png)

* 減輕 database 壓力

這邊和大家簡單說明如何減輕 database 的壓力:satisfied:

可參考 musics/[views.py](https://github.com/twtrubiks/django-docker-redis-tutorial/blob/master/musics/views.py)

```python
# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def list(self, request, **kwargs):
        if self.request.version == '1.0':
            if 'musics' in cache:
                # from cache get musics
                musics = cache.get('musics')
            else:
                musics = Music.objects.all()
                serializer = MusicSerializer(musics, many=True)
                musics = serializer.data
                # store data to cache
                cache.set('musics', musics, timeout=None)
        else:
            musics = Music.objects.all()
            serializer = MusicSerializer(musics, many=True)
            musics = serializer.data
        return Response(musics, status=status.HTTP_200_OK)
```

假設 database 的 music 這張表格中有一萬筆資料，然後如果每個人每次發送 request 過來都要重新撈這一萬筆資料，

會對資料庫造成很大的壓力，也沒什麼效率，這時候就可以透過 redis 來幫助我們。

程式其實很簡單，當 redis 中沒有 musics 這個 key 的時候，我就去資料庫撈，然後將撈到的資料存進 redis 中，

這樣當下一次我還需要時，就可以直接從 redis 中取得資料（ 不需要再重新從資料庫中撈資料 ）。

你可能會問我為什麼要用 `self.request.version` ，原因是等等我們模擬簡單壓力測試要使用的:grinning:

Django 的 version 使用方法可參考我之前寫的 [django-rest-framework-tutorial#versioning](https://github.com/twtrubiks/django-rest-framework-tutorial#versioning)。

以下是兩個的比較，

第一次執行會從資料庫撈一萬筆的資料

![alt tag](https://i.imgur.com/4cmFeBD.png)

第二次開始，都會從 **redis** 撈一萬筆的資料 ( 速度快很多 )

![alt tag](https://i.imgur.com/UqR0Tst.png)

從秒數來看，速度至少快了 16 倍，你可能會說，其實還好阿:confused:

不過，假設今天有 100 個人呢？ 相信就非常有感了:smirk:

讓我們透過數據說話，使用 [loadtest](https://www.npmjs.com/package/loadtest) 來簡單模擬，

先安裝 [loadtest](https://www.npmjs.com/package/loadtest)

```cmd
npm install --location=global loadtest
```

使用方法

```cmd
loadtest [-n requests] [-c concurrency] [-k] URL
```

先來測試 **沒有 redis** 的情況 ( 50 個 request )

```cmd
loadtest -H "Authorization: Basic dHd0cnViaWtzOnBhc3N3b3JkMTIz" -n 50 -k  http://127.0.0.1:8000/api/musics/
```

如下圖，慢到我不想等他跑完 :sweat: ( 還在 38%)

![alt tag](https://i.imgur.com/8FLqtpS.png)

再來測試 **有 redis** 的情況 ( 50 個 request )

```cmd
loadtest -H "Authorization: Basic dHd0cnViaWtzOnBhc3N3b3JkMTIz" -H "Accept: application/json;version=1.0" -n 50 -k  http://127.0.0.1:8000/api/musics/
```

如下圖，很快就跑完了，而且花最久的時間是 229ms

![alt tag](https://i.imgur.com/aPvSww8.png)

可以發現，有 redis 的情況下，效能好很多:heart_eyes:

後面我有再補充另一段 code, [musics/views.py](https://github.com/twtrubiks/django-docker-redis-tutorial/blob/master/musics/views.py)

```python
def list_lock(self, request, **kwargs):
    if self.request.version == '1.0':
        if 'musics' in cache:
            # from cache get musics
            musics = cache.get('musics')
        else:
            if con.set("my_key", "secret", nx=True, px=1000):
                musics = Music.objects.all()
                serializer = MusicSerializer(musics, many=True)
                musics = serializer.data
                cache.set('musics', musics, timeout=None)
                print('store data to cache')
            else:
                print("pending")
                while 1:
                    time.sleep(0.5)
                    print('sleep')
                    if 'musics' in cache:
                        musics = cache.get('musics')
                        print('break')
                        break
    ......
    return Response(musics, status=status.HTTP_200_OK)
```

主要是透過 redis 的鎖, 確保當下只有一個 request 可以進 db 拿資料,

剩下的 request 全部 pending, 直到 redis 有資料.

請搭配以下測試

```cmd
loadtest -H "Authorization: Basic dHd0cnViaWtzOjEyMw==" -H "Accept: application/json;version=1.0" -n 15 -c 15 -k http://127.0.0.1:8000/api/musics/
```

(要多測幾次, 確保有顯示 "pending" )

![alt tag](https://i.imgur.com/nT6Ar8C.png)

相信這時候大家又會問，不過這樣子 redis 裡面的資料有很高的機會是舊的，沒錯，所以更好的方法，

可以搭配 Celery 設定排成 （ Celery 可以參考我之前寫的 [docker-django-celery-tutorial](https://github.com/twtrubiks/docker-django-celery-tutorial) ），一天或

一段時間更新一次 ( 將 db 裡的資料讀出來寫進 redis 中 )，這樣就可以確保 redis 裡面的資料盡量和 db 裡面一樣。

## 執行畫面

請直接瀏覽 [http://127.0.0.1:8000/images/](http://127.0.0.1:8000/images/)，你會發現有一個 View Count : 1

![alt tag](https://i.imgur.com/e6w8ufP.png)

如果你一直重新整理 ( 狂按 F5 )，會發現 View Count 一直增加

![alt tag](https://i.imgur.com/ivf4HFr.png)

可以點選自己喜歡的圖片進去觀看，也會有屬於這張照片的 View Count

![alt tag](https://i.imgur.com/8pXNI7z.png)

如果你一直重新整理 ( 狂按 F5 )，也會發現 View Count 一直增加

![alt tag](https://i.imgur.com/fFYdLjm.png)

回到首頁 ( [http://127.0.0.1:8000/images/](http://127.0.0.1:8000/images/) )，你會發現多了一個排行榜

![alt tag](https://i.imgur.com/0sRMqjK.png)

當瀏覽越多圖片，排行榜就會向下面這樣 (也顯示每張圖片的 View Count )

![alt tag](https://i.imgur.com/MKH0XBG.png)

## 後記

這次帶大家了解 redis 的一些基礎應用，相信大家一定覺得 redis 真的很有趣，然後 redis 可以做的事情絕對不只

這次教學所帶給大家的，他可以做的應用真非常的多，本教學只是帶給大家一個基礎，了解到底什麼是 redis，

然後可以做怎麼樣的應用，希望這教學對想了解 redis 多少有幫助，謝謝大家:relaxed:

## 執行環境

* Python 3.8

## Reference

* [Django](https://www.djangoproject.com/)
* [django-redis](https://github.com/jazzband/django-redis)
* [Redis](https://redis.io/)
* [loadtest](https://www.npmjs.com/package/loadtest)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT licens
