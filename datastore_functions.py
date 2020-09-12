# Imports the Google Cloud client library
from google.cloud import datastore

def addClass(classcode):
    datastore_client = datastore.Client()
    task = datastore.Entity(datastore_client.key('Class', classcode))
    task.update({
        'Users:': {}    #username: instrument
    })

    datastore_client.put(task)

def addUserToClass(classcode, username, instrument):
    datastore_client = datastore.Client()
    
    key = datastore_client.key('Class', classcode)
    task = datastore_client.get(key)
    
    
    user = datastore_client.get(datastore_client.key('Username', username))
    
    task['Users'][username] = instrument
    datastore_client.put(task)

    
    user['Classes'][classcode] = instrument
    datastore_client.put(user)
    


def addUser(username, password):
    if "." in username:
        return False
    
    datastore_client = datastore.Client()
    task = datastore.Entity(datastore_client.key('Username', username))

    task.update({
        'Username': username,
        'Password': password,
        'Classes': {}   #classcode: instrument
        })

    datastore_client.put(task)

def verifyLogin(username, password):
    
    datastore_client = datastore.Client()
    task = datastore_client.get(datastore_client.key('Username', username))

    if task['Password'] != password:
        return False    #Incorrect password
    else:
        return True
    
def removeUserFromClass(classcode, username):
    datastore_client = datastore.Client()
    key = datastore_client.key('Class', classcode)
    task = datastore_client.get(key)

    if username not in task['Users']:
        return False    #User not in class
    else:
        task['Users'].pop(username)

    datastore_client.put(task)

    user = datastore_client.get(datastore_client.key('Username', username))
    user['Classes'].pop(classcode)
    datastore_client.put(user)

def removeClass(classcode):
    datastore_client = datastore.Client()
    task = datastore_client.get(datastore_client.key('Class', classcode))

    for username in task['Users']:
        user = datastore_client.get(datastore_client.key('Username', username))
        user['Classes'].pop(classcode)

    datastore_client.delete(datastore_client.key('Class', classcode))

def removeUser(username):
    datastore_client = datastore.Client()
    user = datastore_client.get(datastore_client.key('Username', username))

    for classcode in user['Classes']:
        task = datastore_client.get(datastore_client.key('Class', classcode))
        task['Users'].pop(username)

    datastore_client.delete(datastore_client.key('Username', username))
