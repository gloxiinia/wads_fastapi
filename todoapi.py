from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

todo_app = FastAPI()


# defining the User class
class User(BaseModel):
    name: str
    email: str
    authProvider: str
    todos: list


class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    authProvider: Optional[str] = None

# defining the Todo class
class Todo(BaseModel):
    uid: str
    text: str
    completed: bool

class UpdateTodo(BaseModel):
    uid: Optional[str] = None
    text: Optional[str] = None
    completed: Optional[bool] = None  

# defining the user dictionary

users = {
    "4b092564-e9c1-11ed-a05b-0242ac120003": User(name = "Jeorge", email = "helloworld@gmail.com", authProvider = "Google", todos = ["3827a48c-e9cd-11ed-a05b-0242ac120003",
                                                                                                                                    "3827aa9a-e9cd-11ed-a05b-0242ac120003"]),
    "4b092938-e9c1-11ed-a05b-0242ac120003": User(name = "Yung", email = "byebye@gmail.com", authProvider = "Google", todos = []),
    "4b092af0-e9c1-11ed-a05b-0242ac120003": User(name = "Petra", email = "hola@gmail.com", authProvider = "Google", todos = []),
    "4b092cbc-e9c1-11ed-a05b-0242ac120003": User(name = "Lily", email = "realreal@yahoo.com", authProvider = "Twitter", todos = [])
}

# # defining the todo dictionary

todos = {
    "3827a48c-e9cd-11ed-a05b-0242ac120003": Todo(uid = "4b092564-e9c1-11ed-a05b-0242ac120003", text = "Buy groceries", completed = False), 
    "3827aa9a-e9cd-11ed-a05b-0242ac120003": Todo(uid = "4b092564-e9c1-11ed-a05b-0242ac120003", text = "Read books idk", completed = False),
    "ae485986-e9d2-11ed-a05b-0242ac120003": Todo(uid = "4b092938-e9c1-11ed-a05b-0242ac120003", text = "Watch Ghost in the Shell", completed = True),
    "ae485eb8-e9d2-11ed-a05b-0242ac120003": Todo(uid = "4b092938-e9c1-11ed-a05b-0242ac120003", text = "Prep dinner", completed = False),
    "ae484f22-e9d2-11ed-a05b-0242ac120003": Todo(uid = "4b092af0-e9c1-11ed-a05b-0242ac120003", text = "Clean room", completed = True)

}

# defining the error dictionary

errors = {
    1 : "User does NOT exist.",
    2 : "User already exists.",
    3 : "User has NO todos.",
    4 : "Todo already exists.",
    5 : "Todo does NOT exist."
}


# GET METHODS
@todo_app.get("/get-user/{uid}")
def get_user(uid: str = Path (description = "The id of the user you want to view.")):
    return users[uid]

@todo_app.get("/get-user-by-name")
def get_user(name: Optional[str] = None):
    for uid in users:
        if users[uid].name == name:
            return users[uid]
    return {"error" : errors[1]}

    
@todo_app.get("/get-user-by-email")
def get_user(email: Optional[str] = None):
    for uid in users:
        if users[uid].email == email:
            return users[uid]
    return {"error" : errors[1]}

@todo_app.get("/get-user-todos")
def get_todo(uid: str):
    count = 1
    user_todos = {}
    for todo_id in todos:
        if todos[todo_id].uid == uid:
            user_todos.update({ count: todos[todo_id]})
            count += 1
    if user_todos:
        return user_todos
    else:
        return {"error" : errors[3]}  

# POST METHODS

@todo_app.post("/create-user/{uid}")
def add_user(uid : str, user : User):
    if uid in users:
        return {"error" : errors[2]}
    else:
        users[uid] = user
        return users[uid]
    
@todo_app.post("/create-todo")
def add_todo(todo_id : str, todo : Todo):
    if todo_id in todos:
        return {"error" : errors[4]}
    else:
        todos[todo_id] = todo
        return todos[todo_id]
    
# PUT METHODS
    
@todo_app.put("/update-user/{uid}")
def update_user(uid : str, user : UpdateUser):
    if uid not in users:
        return {"error" : errors[1]}
    
    if user.name != None:
        users[uid].name = user.name
    
    if user.email != None:
        users[uid].email = user.email

    return users[uid]

@todo_app.put("/update-todo/{todo_id}")
def update_todo(todo_id : str, todo : UpdateTodo):
    if todo_id not in todos:
        return {"error" : errors[5]}
    
    if todo.uid != None:
        todos[todo_id].uid = todo.uid
    
    if todo.text != None:
        todos[todo_id].text = todo.text

    if todo.completed != None:
        todos[todo_id].completed = todo.completed

    return todos[todo_id]

# DELETE METHOD

@todo_app.delete("/delete-user/{uid}")
def delete_user(uid: str):
    if uid not in users:
        return {"error" : errors[1]}
    del users[uid]
    return {"Data" : "Deleted successfully."}

@todo_app.delete("/delete-todos")
def delete_task(todo_id : str):
    if todo_id not in todos:
        return {"error" : errors[3]}
    del todos[todo_id]
    return { "Data" : "Deleted successfully."}
    
        
