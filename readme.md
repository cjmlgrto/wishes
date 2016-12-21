# ★ Wishes

<img src="https://raw.githubusercontent.com/cjmlgrto/wishes/master/static/assets/screenshot.png" width="320"/>

**Problem**: So you've organised a kris-kringle with your entire extended family. You already know who you're buying a gift for— *but you don't know what they want*! Also, you have an idea of *you yourself* want. You wanna make sure people are buying the right things for each other.

**Solution**: Wishes! This webapp is a shared family wishes manager that allows you to populate your own personal wishlist, and check what other people in your family want! *Bonus feature*— you can anonymously ‘cross off’ items in other people's wishlists, that way you can avoid duplicate gifts!

### Requirements

- Python
- [Flask](http://flask.pocoo.org)
- [Peewee](https://github.com/coleifer/peewee)

### How to Run

- Execute `app.py`. If you're using bash, run `python app.py`.

### How to Deploy

- Create a Heroku account if you haven't already
- Follow the short video tutorial over at [heroku.com/python](https://www.heroku.com/python)
- Install the [Clear DB MySQL](https://devcenter.heroku.com/articles/cleardb) Add-on
- Replace the following line in `models.py`:

```python
db = SqliteDatabase('members.db')
```

- With the following lines:

```python
import os

DB_URL = os.environ['CLEARDB_DATABASE_URL']
DB = DB_URL[65:]
HOST = DB_URL[32:64]
USER = DB_URL[8:22]
PWD = DB_URL[23:31]

db = MySQLDatabase(DB, host=HOST, port=3306, user=USER, passwd=PWD)
```

- Push the changes to Heroku using `git push heroku master`
- If you want to change the family members, replace the `groups` dictionary in `app.py`.
