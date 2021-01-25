import json
import os
import pymongo
import subprocess
import platform

def print_mongo(*args):
    print('[mongodb]', *args)

class MongoDB:
    def __init__(self):
        self.process = None
        self.client = None
        self.db = None

    def start(self):
        process = ''
        client = pymongo.MongoClient(serverSelectionTimeoutMS=500)
        operating_system = platform.system()
        args = ''

        try:
            client.admin.command('ismaster')
            print_mongo('server is running')

        except ConnectionFailure:
            if operatin_system == 'Linux':
                process = 'mongo'

            if operating_system == 'Darwin':
                process = 'mongod'
                args = '--dbpath=/data/db'

            if operating_system == 'Windows':
                process = 'C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongod.exe'
                args = '--dbpath="C:\\data\\db"'

            self.process = subprocess.Popen([process, args])
            print_mongo('server started')

    def connect(self):
        self.client = pymongo.MongoClient()
        print_mongo('client connected:', self.client)

        try:
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print_mongo('server is not available')

    def connect_db(self, db):
        if self.get_status() is None:
            print_mongo('please connect to the client first')
        else:
            self.db = self.client[db]
            print_mongo('connected to database:', db)

    # does only check if data in collection exists
    def add_json_data(self, device):
        Collection = self.db[device]

        path_to_json = '../data/'

        if Collection.count() == 0:
            for file_name in [file for file in os.listdir(path_to_json) if file.startswith(device) and file.endswith('.json')]:
                with open(path_to_json + file_name) as json_file:
                    data = json.load(json_file)
                    res = Collection.insert_one(data)
                    print('data inserted for', file_name, 'inserted:', res.acknowledged)
        else:
            print_mongo('collection for', device, 'already exists')

    def get_status(self):
        if self.client is not None:
            return self.client.admin.command('serverStatus')
        else:
            print_mongo('no client connection')
