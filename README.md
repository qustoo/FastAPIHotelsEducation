
# Hotel bookings PET-project

**A FastAPI pet project for working with API aggregators of hotels.**

_Stack:_ FastAPI,Docker,Redis,PostgreSQL,Celery,Grafana,Pytest,SQlAlchemy ORM, black,flake8,pyright,
***
# Installation 
## 1.Clone repository
---
```bash
git clone https://github.com/qustoo/FastAPIHotelsEducation
```
## 2. Set values in .env
---
```
MODE=DEV
LOG_LEVEL=INFO

DB_HOST=XXX
DB_PORT=XXX
DB_USER=XXX
DB_PASS=XXX
DB_NAME=XXX
...
```
## 3. Start project, inside in app directory
---
```
uvicorn main:app --host = 0.0.0.0 --reload
```
## 4. Visit http://localhost:8000 on localy, and http://localhost:7777 if u using docker
## 5. Screenshots
---
![get all hotels](files_to_readme/all_hotels.png)
## 6. Build in docker,  inside in app directory
---
```
docker-compose up -d
```