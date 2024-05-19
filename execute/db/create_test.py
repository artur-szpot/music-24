import json

from execute.db.MusicFile import MusicFile
from execute.db.io import create_directory


def create_test():
    create_directory('db')
    test_file = MusicFile({
        'authors': ['Datphoria'],
        'genres': ['Electro', 'Dubstep'],
        'title': "Sin Ti",
        'path': "D:/music/dat - sinti.mp3",
        'length': 420,
        'rating': 7,
        'is_mlp': False,
        'is_dad': False,
        'is_ready': True
    })
    with open('db/0.json', mode='w') as file:
        file.write(json.dumps(test_file.to_dict()))
    return ['created test file']
