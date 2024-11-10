# src/gui.py
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from data_manager import load_data, save_data
import logging

class ProjectManagerUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Manager')
        self.setGeometry(300, 300, 600, 400)
        self.init_ui()

    def init_ui(self):
        self.projects = load_data()['projects']

        # Create main layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create sections for Git projects
        git_projects = [p for p in self.projects if p['type'] == 'git']

        # Add Git projects to the UI
        git_label = QtWidgets.QLabel('Git Projects')
        main_layout.addWidget(git_label)
        for project in git_projects:
            project_widget = self.create_project_widget(project)
            main_layout.addWidget(project_widget)

    def create_project_widget(self, project):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        # Project Name
        name_label = QtWidgets.QLabel(project['name'])
        layout.addWidget(name_label)

        # Status
        status_label = QtWidgets.QLabel(project['status'])
        layout.addWidget(status_label)

        # Clone/Open buttons
        clone_button = QtWidgets.QPushButton('Clone')
        open_button = QtWidgets.QPushButton('Open')

        clone_button.clicked.connect(lambda: self.clone_project(project))
        open_button.clicked.connect(lambda: self.open_project(project))

        # Enable/Disable buttons based on status
        if project['status'] == 'cloned':
            clone_button.setDisabled(True)
        if project['status'] == 'not_cloned':
            open_button.setDisabled(True)

        layout.addWidget(clone_button)
        layout.addWidget(open_button)

        return widget

    def clone_project(self, project):
        from vcs_manager import clone_repo
        success = clone_repo(project)
        if success:
            project['status'] = 'cloned'
            save_data({'projects': self.projects})
            self.refresh_ui()

    def open_project(self, project):
        from launcher import open_unity_project, open_with_ide
        project_path = os.path.join('projects', project['name'])
        if project['is_unity']:
            open_unity_project(project_path, project.get('unity_version', ''))
        else:
            open_with_ide(project_path)
        project['status'] = 'open'
        save_data({'projects': self.projects})
        self.refresh_ui()

    def refresh_ui(self):
        # Refresh the UI to reflect changes
        self.close()
        self.__init__()
        self.show()

class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip('Project Manager')
        self.menu = QtWidgets.QMenu(parent)

        # Add options to the tray icon's context menu
        show_action = self.menu.addAction('Show Projects')
        exit_action = self.menu.addAction('Exit')

        show_action.triggered.connect(self.show_projects)
        exit_action.triggered.connect(self.exit_app)

        self.setContextMenu(self.menu)

        # Handle click on the tray icon
        self.activated.connect(self.on_click)

        # Keep a reference to the main window
        self.main_window = None

    def show_projects(self):
        if self.main_window is None or not self.main_window.isVisible():
            self.main_window = ProjectManagerUI()
        self.main_window.show()
        self.main_window.activateWindow()

    def exit_app(self):
        QtWidgets.QApplication.quit()

    def on_click(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            # Left click on the tray icon
            self.show_projects()

def run_app():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Set up the tray icon
    icon_path = os.path.join('assets', 'icon.png')  # Use your actual icon file
    tray_icon = TrayIcon(QtGui.QIcon(icon_path))
    tray_icon.show()

    # Show notification on first run
    tray_icon.showMessage(
        "Project Manager",
        "The application is running in the system tray. Click the icon to open.",
        QtWidgets.QSystemTrayIcon.Information,
        5000  # Duration in milliseconds
    )

    sys.exit(app.exec_())