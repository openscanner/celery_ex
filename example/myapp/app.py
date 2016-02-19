#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""app.py

Usage:

   (window1)$ python app.py worker -l info

   (window2)$ python
   from myapp import add
   add.delay(16, 16).get()
   32


You can also specify the app to use with the `celery` command,
using the `-A` / `--app` option::

    $ celery -A app worker -l debug --config=config.cson

"""


from celery import Celery

app = Celery(
    'test',
    loader="celery_ex.loader:AppExLoader",
    # broker='redis://localhost:6379/1',
)


@app.task()
def add(x, y):
    return x + y


if __name__ == '__main__':
    app.start()
