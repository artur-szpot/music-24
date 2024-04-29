import json

from execute.db.io import create_directory


def create_test():
    create_directory('db')
    with open('db/test.json', mode='w') as file:
        file.write(json.dumps({'value': 'test'}))
