# src/data_manager.py
import json
import os
from utils import load_env
from filelock import FileLock

env = load_env()
ENVIRONMENT = env['ENVIRONMENT']

data_file_path = os.path.join('data', 'projects.json')
lock_file_path = data_file_path + '.lock'

def load_data():
    if ENVIRONMENT == 'test':
        with FileLock(lock_file_path):
            with open(data_file_path, 'r') as f:
                return json.load(f)
    elif ENVIRONMENT == 'production':
        # TODO: Implement Airtable data fetching
        pass
    else:
        raise ValueError("Invalid ENVIRONMENT value in .env file.")

def save_data(data):
    if ENVIRONMENT == 'test':
        with FileLock(lock_file_path):
            with open(data_file_path, 'w') as f:
                json.dump(data, f, indent=4)
    elif ENVIRONMENT == 'production':
        # TODO: Implement Airtable data saving
        pass
    else:
        raise ValueError("Invalid ENVIRONMENT value in .env file.")