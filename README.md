# Dashboard

- The dashboard collect and show info

# How to Run

- Step 1 : Download the Repo
```
git clone https://github.com/sentrysk/Sentrysk-Backend
```
- Step 2 : Change the Database Connection Properties in **config.ini**
```
[Database]
; Replace with your database host
HOST = 127.0.0.1
; Replace with your database host
PORT = 27017
; Replace with your database name
DB = dashboard
; Replace with your database username
USERNAME = admin
; Replace with your database password
PASSWORD = your_mongo_admin_password
```

# Agents
In this section you can create,update,delete,list **Agents**

Endpoint prefix: **/agent**

| Action      | Endpoint | Method |
| ----------- | ----------- | ----------- |
| Get         | /           | GET |
| Get by ID   | /id         | GET |
| Create      | /register   | POST |
| Delete      | /<id>       | DELETE |
| Update      | /<id>       | PUT |


# Users
In this section you can register,login,logout **Users**

Endpoint prefix: **/user**

| Action      | Endpoint | Method |
| ----------- | ----------- | ----------- |
| Get         | /           | GET |
| Get by ID   | /id         | GET |
| Register    | /register   | POST |
| Login       | /register   | POST |
| Logout      | /logout     | POST |

# System Data
In this section you can register and list **System Data**

Endpoint prefix: **/data**

| Action      | Endpoint | Method |
| ----------- | ----------- | ----------- |
| Get All     | /           | GET |
| Get by ID   | /id         | GET |
| Register    | /           | POST |
