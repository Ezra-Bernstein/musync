# Imports the Google Cloud client library
from google.cloud import datastore

def addClass(classcode):
    datastore_client = datastore.Client()
    task = datastore.Entity(datastore_client.key('Class', classcode))
    task.update({
    })

    datastore_client.put(task)

def addUserToClass(classcode, username, instrument):
    datastore_client = datastore.Client()
    key = datastore_client.key('Class', instrument)
    task = datastore_client.get(key)
    task[username] = instrument

    datastore_client.put(task)

