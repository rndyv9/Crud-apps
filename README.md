Contact CRUD Web App

Overview

Simple web-based CRUD application to save name and phone number.

Features

- Save name and phone number
- Update phone number (same name, different phone number)
- Delete
- View all
- Export contacts to CSV
- Automated API testing

---

Tech Stack

- FastAPI
- Uvicorn
- SQLAlchemy + SQLite
- pytest
- HTML + JavaScript

---

1. Clone Repository

```
git clone https://github.com/rndyv9/Crud-app
```
```
cd Crud-app
```

---

2. Create Virtual Environment

Linux / Mac
```
python3 -m venv venv
```
```
source venv/bin/activate
```

Windows

```
python -m venv venv
```
```
venv\Scripts\activate
```

---

3. Install Dependencies
```
pip install -r requirements.txt
```

---

4. Run Application
```
uvicorn app.main:app --reload
```

Open:
```
http://127.0.0.1:8000
```
API Docs:
```
http://127.0.0.1:8000/docs
```
---

5. Run Tests
```
pytest
```

---

API Endpoints

Create / Update Contact

POST /contact?name={name}&phone={phone}

- Insert if name does not exist
- Update if name exists with different phone number

---

Read All Contacts

GET /contacts

---

Delete Contact

DELETE /contact/{name}

---

Export CSV

GET /export/csv

---

Notes

- Name is unique (primary key)
- SQLite database ("contacts.db") is created automatically
- Tests are independent and repeatable

---

Example

Input:

Name: Luck
Phone: 007

Output:

Name   | Phone
-------|------
Luck   | 007
