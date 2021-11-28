# Splitwise REST Interface - Python/Django 

REST based interface for Splitwise
___
**NOTE**

names have been used as unique ids just for the sake of presentation, real world app should be based on UUID.

---

## Setup

1. Docker Based
   #### Prerequisites
    1. Docker
    2. run command

```shell
docker-compose --build
docker-compose up -d
```
This will expose 0.0.0.0:8000 port for API.

2. Local Setup
   ### Prerequisites
   1. Python 3.9
   2. Pip
```shell
pip install -r requirements.txt
```

   3. Run the command
```python manage.py makemigrations && python manage.py migrate && python manage.py runserver 8000```
    This will start the server at localhost:8000

### For Usage - Use postman collection provided alongside code
Import the collection to postman and you will be able to see the endpoints and use them
Also set an environment variable in postman 

Variable Name = url

Variable Value = http://127.0.0.1:8000/api [local setup] or http://0.0.0.0:8000/api [for docker setup]

## The API Supports the below operations though rest endpoints:
1. Create User [/createUser]
2. Create Group [/createGroup]
3. Add member to group [/addUserToGroup]
4. Add personal expense between 2 existing users [/addExpense]
5. Add group expense [/addExpense]
6. Show Group Expenses [/groupDetails]
7. Show Group Members [/showGroupMembers]
8. Show the user details [/userDetails]
9. Record a personal payment [/recordPayment]
10. Record a group payment [/recordPayment]
11. Delete a user [/deleteUser]
12. Delete a group [/deleteGroup]

## Test Cases
Test cases are available in ```splitwise/tests.py```

To run the test cases, run the command ```python manage.py test```