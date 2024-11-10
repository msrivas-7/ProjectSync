# src/service.py
import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import sys
import os
import time

from monitor import monitor_data_file
from data_manager import load_data, save_data
from vcs_manager import clone_repo
from launcher import open_unity_project, open_with_ide

class ProjectManagerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ProjectManagerService"
    _svc_display_name_ = "Project Manager Service"

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)
        logging.info('Service stopping.')
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.main()

    def main(self):
        # Set up logging
        logging.basicConfig(
            filename='logs/service.log',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s:%(message)s'
        )

        logging.info('Service started.')

        # Implement the monitoring functionality
        def data_changed(data):
            logging.info('Data change detected.')
            for project in data['projects']:
                project_name = project['name']
                project_status = project['status']
                auto_clone = project.get('auto_clone', False)

                project_path = os.path.join('projects', project_name)

                if auto_clone and project_status == 'not_cloned':
                    success = clone_repo(project)
                    if success:
                        project['status'] = 'cloned'
                        save_data({'projects': data['projects']})

                if project_status == 'open':
                    if project['is_unity']:
                        open_unity_project(project_path, project.get('unity_version', ''))
                    else:
                        open_with_ide(project_path)
                    logging.info(f"Opened project {project_name}")

        # Load initial data
        data = load_data()
        data_changed(data)

        # Start monitoring in a separate thread
        from threading import Thread
        monitor_thread = Thread(target=monitor_data_file, args=(data_changed,))
        monitor_thread.daemon = True
        monitor_thread.start()

        # Keep the service running
        while self.running:
            time.sleep(1)

        logging.info('Service stopped.')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # When started by the Service Control Manager
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ProjectManagerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # When run with parameters to install/start/etc.
        win32serviceutil.HandleCommandLine(ProjectManagerService)