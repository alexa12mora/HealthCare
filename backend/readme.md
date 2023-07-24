# Backend readme file

### Make the initial project Setup:
Navigate to the `backend/health_care` folder

Migrate the changes
```bash
python3 manage.py migrate
```

Make migrations
```bash
 python3 manage.py makemigrations 
```

Then start the local server:
```bash
python3 manage.py runserver --settings=review_engine.settings.<env>
```

Create a super-user:
```bash
python3 manage.py createsuperuser --settings=review_engine.settings.<env>
```

Run project
```bash
python3 manage.py runserver --settings=review_engine.settings.<env>
```