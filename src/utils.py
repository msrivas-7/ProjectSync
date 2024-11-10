# src/utils.py
from dotenv import load_dotenv
import os

def load_env():
    load_dotenv(dotenv_path=os.path.join('config', '.env'))
    env = {
        'ENVIRONMENT': os.getenv('ENVIRONMENT', 'test'),
        'COMPUTER_NAME': os.getenv('COMPUTER_NAME'),
        'GIT_USERNAME': os.getenv('GIT_USERNAME'),
        'GIT_PASSWORD': os.getenv('GIT_PASSWORD'),
        'UNITY_EDITORS_PATH': os.getenv('UNITY_EDITORS_PATH'),
        'VSCODE_PATH': os.getenv('VSCODE_PATH'),
        'VISUAL_STUDIO_PATH': os.getenv('VISUAL_STUDIO_PATH'),
    }
    return env