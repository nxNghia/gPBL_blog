# gPBL program
## Hanoi, Aug 2022
## Music team
- Nguyen Xuan Nghia (leader)
- Honda Rika (本田りか) (sub leader)
- Dang Linh Chi
- Murata Hikaru (村田晃琉)
## Prerequisite
- Python v2.x, v3.x
- pipenv
- Flask v1.1.2
- Flask-SQLAlchemy
## Installation
- Clone the repository
```
git clone https://github.com/nxNghia/gPBL_blog.git
```
- Create database (use python)
```
>>> from blog import db
>>> db.create_all()
```
- Run the server
```
python server.py
```
or (in case you use python3)
```
python3 server.py
```