# Commands to Intialize Database

Step -1: Open python shell in the project directory(folder)
Step -2: Run below commands
```
from bookmanager import db, app
with app.app_context():
  db.create_all()
  exit()
```
