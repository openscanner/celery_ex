# celery 扩展 (celery extension)

添加如下功能:

1. 配置支持从配置文件读取(json/cson)格式 - (如果用 docker, 直接利用 celery 本身支持的环境变量也是个好方法)


## install
```pip install https://github.com/openscanner/celery_ex/zipball/master```

## Usage

```python
from celery import Celery

app = Celery(
    'tasks',
    loader="celery_ex.loader:AppExLoader", # change default AppLoader
)


@app.task()
def add(x, y):
    return x + y
```

Now: celery configuration file support cson/json file, you could used as below:
```sh
celery -A app worker -l debug --config=config.cson
```
