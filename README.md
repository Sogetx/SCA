# SCA(Spy Cat Agency) Project

Test Task for company [DevelopsToday](https://img.shields.io/badge/License-Apache%202.0-blue.svg](https://jobs.develops.today/)). 

## Contents
- [Requirements](#requirements)
- [Install](#install)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Create and activate a virtual environment](#2-create-and-activate-a-virtual-environment)
  - [3. Install dependencies](#3-install-dependencies)
  - [4. Set up environment variables](#4-set-up-environment-variables)
  - [5. Apply migrations](#5-apply-migrations)
  - [6. Start the server](#6-start-the-server)
- [Endpoints Check](#endpoints-check)
- [Examples](#examples)
  - [Create a spy cat](#create-a-spy-cat)
  - [Check for invalid breed](#check-for-invalid-breed)
  - [List spy cats](#list-spy-cats)
  - [Update spy cat salary](#update-spy-cat-salary)
  - [Create mission](#create-mission)
  - [Assign a spy cat to a mission](#assign-a-spy-cat-to-a-mission)
  - [Mark mission as completed](#mark-mission-as-completed)

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
py -3 -m venv venv
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
python manage.py makemigrations core
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

## Examples

### Create a spy cat
Creates a new spy cat. The breed field is validated through an external API (TheCatAPI). You cannot create a spy cat with an invalid breed.
`POST /api/cats/`
```json
{
  "name": "Charly",
  "years_of_experience": 5,
  "breed": "American Shorthair",
  "salary": 1000.00
}
```
Result:
```json
{
    "id": 5,
    "name": "Charly",
    "years_of_experience": 5,
    "breed": "American Shorthair",
    "salary": 1000.0
}
```
### Check for invalid breed
Example when user try to create cat with invalid breed
`POST /api/cats/`
```json
{
    "name": "Michael",
    "years_of_experience": 5,
    "breed": "United",
    "salary": 1000.00
}
```
Result:
```json
[
    "Invalid breed."
]
```
### List spy cats
For all cats: `GET /api/cats/`
Result:
```json
[
    {
        "id": 1,
        "name": "astro",
        "years_of_experience": 5,
        "breed": "Abyssinian",
        "salary": 2000.0
    },
    {
        "id": 5,
        "name": "Charly",
        "years_of_experience": 5,
        "breed": "American Shorthair",
        "salary": 1000.0
    },
    {
        "id": 8,
        "name": "Charly",
        "years_of_experience": 5,
        "breed": "Persian",
        "salary": 1000.0
    },
    {
        "id": 9,
        "name": "Homer",
        "years_of_experience": 6,
        "breed": "Persian",
        "salary": 50.0
    }
]
```
For one cat: `GET /api/cats/8/` num is cat id
Result:
```json
{
    "id": 8,
    "name": "Charly",
    "years_of_experience": 5,
    "breed": "Persian",
    "salary": 1000.0
}
```
### Update spy cat salary
`PATCH /api/cats/8/update_salary/` num is cat id
```json
{
  "salary": 400.0
}
```
Result:
```json
{
    "status": "Salary updated",
    "new_salary": 200.0
}
```
### Create mission
Creates a new mission, including associated targets. Each mission contains information about the spy cat, targets, and the completion state.
`POST /api/missions/`
```json
{
    "spy_cat": 8,
    "status": "in_progress",
    "completed": false,
    "targets": [
        {
            "name": "Target 1",
            "country": "Greece",
            "notes": "First target",
            "completed": false
        },
        {
            "name": "Target 2",
            "country": "USA",
            "notes": "Second target",
            "completed": false
        }
    ]
}
```
Result:
```json
{
    "id": 3,
    "spy_cat": 8,
    "status": "in_progress",
    "completed": false,
    "targets": [
        {
            "id": 9,
            "name": "Target 1",
            "country": "Greece",
            "notes": "First target",
            "completed": false,
            "mission": 3
        },
        {
            "id": 10,
            "name": "Target 2",
            "country": "USA",
            "notes": "Second target",
            "completed": false,
            "mission": 3
        }
    ]
}
```
### Assign a spy cat to a mission
Assigns a spy cat to an **existing** mission.
`POST /api/missions/3/assign_cat/` num is mission id
```json
{
    "cat_id": 1
}
```
Result:
```json
{
    "status": "cat assigned"
}
```
### Mark mission as completed
Marks the mission as completed if it is not completed yet.
`PATCH /api/missions/3/mark_completed/` num is mission id
Result:
```json
{
    "status": "mission completed"
}
```

All examples can be explored hands-on by importing the provided Postman [collection](https://api.postman.com/collections/39445059-1ea57a23-4f98-456a-97c2-593dafda3040?access_key=PMAT-01JCRBJ6J1BMJGE1PPPE7BZQ49).
