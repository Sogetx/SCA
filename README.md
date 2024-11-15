# SCA(Spy Cat Agency) Project

Test Task for company [DevelopsToday](https://img.shields.io/badge/License-Apache%202.0-blue.svg](https://jobs.develops.today/)). 

Details will be soon, please wait.

## Requirements
- Python 3.x
- Django 5.x
- Django REST Framework
- SQLite (default for Django)

## Install 
### 1. Clone the repository
```
git clone https://github.com/Sogetx/SCA.git
cd SCA
```
### 2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
On Windows use
```
venv\Scripts\activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Set up environment variables
Create .env file and enter there your key:
```
SECRET_KEY=your_secret_key_here
```
### 5. Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
### 6. Start the server
```
python manage.py runserver
```

That’s all! The next step is to visit the **Endpoints Check** chapter, import the Postman collection, and try it out.

**Note!** Before testing other endpoints, make sure to create a spy cat and mission object.
## Endpoints Check
Import collection via paste this [link](https://api.postman.com/collections/39445059-1ea57a23-4f98-456a-97c2-593dafda3040?access_key=PMAT-01JCRBJ6J1BMJGE1PPPE7BZQ49).
