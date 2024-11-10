# src/launcher.py
import os
import subprocess
from utils import load_env
import logging

env = load_env()
UNITY_EDITORS_PATH = env['UNITY_EDITORS_PATH']
VSCODE_PATH = env['VSCODE_PATH']
VISUAL_STUDIO_PATH = env['VISUAL_STUDIO_PATH']

def open_unity_project(project_path, unity_version):
    unity_exe_path = os.path.join(
        UNITY_EDITORS_PATH,
        unity_version,
        'Editor',
        'Unity.exe'
    )
    if os.path.exists(unity_exe_path):
        try:
            subprocess.Popen([unity_exe_path, '-projectPath', project_path])
            logging.info(f"Opened Unity project at {project_path} with Unity version {unity_version}")
        except Exception as e:
            logging.error(f"Error opening Unity project: {e}")
    else:
        logging.error(f"Unity version {unity_version} not found at {unity_exe_path}")

def open_with_ide(project_path):
    if os.path.exists(VSCODE_PATH):
        try:
            subprocess.Popen([VSCODE_PATH, project_path])
            logging.info(f"Opened project at {project_path} with VSCode")
        except Exception as e:
            logging.error(f"Error opening project with VSCode: {e}")
    elif os.path.exists(VISUAL_STUDIO_PATH):
        try:
            subprocess.Popen([VISUAL_STUDIO_PATH, project_path])
            logging.info(f"Opened project at {project_path} with Visual Studio")
        except Exception as e:
            logging.error(f"Error opening project with Visual Studio: {e}")
    else:
        logging.error("No supported IDE found.")