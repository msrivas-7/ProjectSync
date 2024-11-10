# src/monitor.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from data_manager import load_data
import logging

class DataChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_modified(self, event):
        if os.path.basename(event.src_path) == 'projects.json':
            logging.info('Detected changes in projects.json')
            data = load_data()
            self.callback(data)

def monitor_data_file(callback):
    event_handler = DataChangeHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path='data', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()