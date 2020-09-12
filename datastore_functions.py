# Imports the Google Cloud client library
from google.cloud import datastore

def addClass(classcode):
    datastore_client = datastore.Client()
    task = datastore.Entity(datastore_client.key('Class', classcode))
    task.update({
        'Users:': {}    #username: instrument
    })

    datastore_client.put(task)
    return True

def addUserToClass(classcode, username, instrument):
    datastore_client = datastore.Client()
    
    key = datastore_client.key('Class', classcode)
    task = datastore_client.get(key)
    
    user = datastore_client.get(datastore_client.key('Username', username))

    if task is None or user is None:
        return False
    
    task['Users'][username] = instrument
    datastore_client.put(task)

    
    user['Classes'][classcode] = instrument
    datastore_client.put(user)
    
    return True

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
    return True

def verifyLogin(username, password):
    datastore_client = datastore.Client()
    
    
    task = datastore_client.get(datastore_client.key('Username', username))

    if task is not None and task['Password'] != password:
        return False    #Incorrect password
    else:
        return True
    
def removeUserFromClass(classcode, username):
    datastore_client = datastore.Client()
    key = datastore_client.key('Class', classcode)
    task = datastore_client.get(key)

    if task is not None and username not in task['Users']:
        return False    #User not in class
    else:
        task['Users'].pop(username)

    datastore_client.put(task)

    user = datastore_client.get(datastore_client.key('Username', username))
    user['Classes'].pop(classcode)
    datastore_client.put(user)
    return True

def removeClass(classcode):
    datastore_client = datastore.Client()
    task = datastore_client.get(datastore_client.key('Class', classcode))

    if task is None:
        return False
    
    for username in task['Users']:
        user = datastore_client.get(datastore_client.key('Username', username))
        user['Classes'].pop(classcode)

    datastore_client.delete(datastore_client.key('Class', classcode))
    return True

def removeUser(username):
    datastore_client = datastore.Client()
    user = datastore_client.get(datastore_client.key('Username', username))

    if user is None:
        return False
    
    for classcode in user['Classes']:
        task = datastore_client.get(datastore_client.key('Class', classcode))
        task['Users'].pop(username)

    datastore_client.delete(datastore_client.key('Username', username))
    return True

def getClasses(username):
    datastore_client = datastore.Client()
    user = datastore_client.get(datastore_client.key('Username', username))

    if user is None:
        return False
    
    classes = []
    for classcode in user['Classes']:
        classes.append(classcode)

    return classes

def getInstrument(classcode, username):
    datastore_client = datastore.Client()
    classData = datastore_client.get(datastore_client.key('Class', classcode))

    if classData is None:
        return False
    if username in classData['Users'].keys():
        return classData['Users'][username]
    
    return False
