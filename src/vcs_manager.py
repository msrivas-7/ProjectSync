# src/vcs_manager.py
from git import Repo
import os
from utils import load_env
import logging

env = load_env()
GIT_USERNAME = env['GIT_USERNAME']
GIT_PASSWORD = env['GIT_PASSWORD']

def clone_repo(project):
    repo_url = project['source_link']
    project_name = project['name']
    project_path = os.path.join('projects', project_name)

    if not os.path.exists(project_path):
        # Include authentication in the URL if necessary
        if GIT_USERNAME and GIT_PASSWORD:
            repo_url = repo_url.replace('https://', f'https://{GIT_USERNAME}:{GIT_PASSWORD}@')
        try:
            Repo.clone_from(repo_url, project_path)
            logging.info(f"Cloned repository {repo_url} into {project_path}")
            return True
        except Exception as e:
            logging.error(f"Error cloning repository {repo_url}: {e}")
            return False
    else:
        logging.info(f"Repository {project_name} already exists at {project_path}")
        return False

def pull_updates(project):
    project_name = project['name']
    project_path = os.path.join('projects', project_name)
    if os.path.exists(project_path):
        try:
            repo = Repo(project_path)
            origin = repo.remotes.origin
            origin.pull()
            logging.info(f"Pulled updates for repository {project_name}")
        except Exception as e:
            logging.error(f"Error pulling updates for {project_name}: {e}")
    else:
        logging.warning(f"Repository {project_name} does not exist at {project_path}")