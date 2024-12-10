# src/gui.py
import sys
import os
import logging
from PyQt5 import QtWidgets, QtGui, QtCore
from data_manager import load_data, save_data

# Set up basic logging to stdout
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

class ProjectManagerUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        logging.debug("Initializing ProjectManagerUI...")
        print("ProjectManagerUI: Initializing main window UI.")

        self.setWindowTitle("Project Manager")
        self.resize(800, 600)
        
        # Set application style (Fusion) and dark theme
        self.apply_dark_theme()

        logging.debug("Loading project data...")
        print("Loading project data from data_manager.")
        self.projects_data = load_data().get('projects', [])
        logging.debug(f"Loaded {len(self.projects_data)} projects.")
        print(f"Number of projects loaded: {len(self.projects_data)}")

        logging.debug("Calling init_ui to build the interface.")
        self.init_ui()

    def apply_dark_theme(self):
        logging.debug("Applying dark Fusion theme...")
        QtWidgets.QApplication.setStyle("Fusion")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(45, 45, 45))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 45))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(0, 122, 180))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 122, 180))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        QtWidgets.QApplication.setPalette(palette)

    def init_ui(self):
        logging.debug("Building main UI layout...")
        print("Building the UI layout now.")

        # Main central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        # A toolbar at the top for branding/title
        self.toolbar = QtWidgets.QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

        title_label = QtWidgets.QLabel("Project Manager")
        font = title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: white;")
        title_container = QtWidgets.QWidget()
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0,0,0,0)
        title_layout.addWidget(title_label, 0, QtCore.Qt.AlignCenter)
        self.toolbar.addWidget(title_container)
        self.toolbar.setStyleSheet("QToolBar { background: #2d2d2d; border: none; }")

        # Scroll Area for projects
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(15)

        # Filter projects by type and add sections
        git_projects = [p for p in self.projects_data if p['type'] == 'git']
        logging.debug(f"Found {len(git_projects)} git projects.")
        print(f"Git projects found: {len(git_projects)}")

        if git_projects:
            git_label = QtWidgets.QLabel("Git Projects")
            git_font = git_label.font()
            git_font.setPointSize(12)
            git_font.setBold(True)
            git_label.setFont(git_font)
            git_label.setStyleSheet("color: white;")
            scroll_layout.addWidget(git_label)

            for project in git_projects:
                project_group = self.create_project_group(project)
                scroll_layout.addWidget(project_group)
        else:
            # If no git projects, display a message
            no_git_label = QtWidgets.QLabel("No Git Projects Found")
            no_git_label.setStyleSheet("color: #cccccc;")
            scroll_layout.addWidget(no_git_label)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Status Bar
        self.statusBar().showMessage("Ready")
        logging.debug("UI build complete.")
        print("UI build complete. Main window ready.")

    def create_project_group(self, project):
        logging.debug(f"Creating UI group for project {project.get('name', 'Unnamed')}")
        group_box = QtWidgets.QGroupBox()
        group_box.setStyleSheet("QGroupBox { border: 1px solid #555; border-radius: 5px; margin-top: 10px; }")
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        group_box.setLayout(layout)

        # Project Name
        name_label = QtWidgets.QLabel(project['name'])
        font = name_label.font()
        font.setBold(True)
        name_label.setFont(font)
        name_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(name_label)

        # Spacer
        layout.addStretch()

        # Status
        status_label = QtWidgets.QLabel(f"Status: {project['status']}")
        status_label.setStyleSheet("color: #cccccc;")
        layout.addWidget(status_label)

        # Clone/Open buttons
        clone_button = QtWidgets.QPushButton("Clone")
        open_button = QtWidgets.QPushButton("Open")

        # Use standard icons
        clone_icon = self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogNewFolder)
        open_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton)
        clone_button.setIcon(clone_icon)
        open_button.setIcon(open_icon)

        clone_button.setStyleSheet("QPushButton { background-color: #444; color: #eee; } QPushButton:hover { background-color: #555; }")
        open_button.setStyleSheet("QPushButton { background-color: #444; color: #eee; } QPushButton:hover { background-color: #555; }")

        clone_button.clicked.connect(lambda: self.clone_project(project))
        open_button.clicked.connect(lambda: self.open_project(project))

        # Enable/Disable buttons based on status
        if project['status'] == 'cloned':
            clone_button.setDisabled(True)
        if project['status'] == 'not_cloned':
            open_button.setDisabled(True)

        layout.addWidget(clone_button)
        layout.addWidget(open_button)

        return group_box

    def clone_project(self, project):
        logging.debug(f"Attempting to clone project: {project['name']}")
        from vcs_manager import clone_repo
        success = clone_repo(project)
        if success:
            logging.debug("Clone successful, updating project status.")
            project['status'] = 'cloned'
            save_data({'projects': self.projects_data})
            self.refresh_ui()
        else:
            logging.warning("Clone failed. Check vcs_manager clone_repo function.")

    def open_project(self, project):
        logging.debug(f"Attempting to open project: {project['name']}")
        from launcher import open_unity_project, open_with_ide
        project_path = os.path.join('projects', project['name'])
        if project.get('is_unity', False):
            open_unity_project(project_path, project.get('unity_version', ''))
        else:
            open_with_ide(project_path)
        project['status'] = 'open'
        save_data({'projects': self.projects_data})
        self.refresh_ui()

    def refresh_ui(self):
        logging.debug("Refreshing UI after project status change.")
        print("Refreshing UI after a project action.")
        self.projects_data = load_data().get('projects', [])
        self.init_ui()


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        logging.debug("Initializing tray icon...")
        print("Initializing tray icon...")

        self.setToolTip('Project Manager')
        self.menu = QtWidgets.QMenu(parent)

        show_action = self.menu.addAction('Show Projects')
        exit_action = self.menu.addAction('Exit')

        show_action.triggered.connect(self.show_projects)
        exit_action.triggered.connect(self.exit_app)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_click)
        self.main_window = None

    def show_projects(self):
        logging.debug("Tray icon: show_projects called.")
        print("Tray icon: Attempting to show the main window.")
        if self.main_window is None or not self.main_window.isVisible():
            self.main_window = ProjectManagerUI()
        self.main_window.show()
        self.main_window.activateWindow()

    def exit_app(self):
        logging.debug("Tray icon: exit_app called, quitting.")
        print("Exiting application from tray menu.")
        QtWidgets.QApplication.quit()

    def on_click(self, reason):
        logging.debug(f"Tray icon clicked. Reason: {reason}")
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.show_projects()


def run_app():
    logging.debug("Starting application...")
    print("Starting application...")
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Check if system tray is available
    if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
        logging.error("System tray not available on this system.")
        print("System tray not available, cannot proceed.")
        sys.exit(1)

    # Determine base_path depending on whether we're frozen (PyInstaller) or running from source
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # If running from source, go up one directory from src
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    icon_path = os.path.join(base_path, 'assets', 'icon.png')

    if not os.path.exists(icon_path):
        logging.error(f"Icon file not found: {icon_path}")
        print(f"Icon file not found: {icon_path}")
        sys.exit(1)

    tray_icon = TrayIcon(QtGui.QIcon(icon_path))
    tray_icon.show()
    logging.debug("Tray icon shown.")
    print("Tray icon shown in the system tray.")

    # Show notification on first run
    tray_icon.showMessage(
        "Project Manager",
        "The application is running in the system tray. Click the icon to open.",
        QtWidgets.QSystemTrayIcon.Information,
        5000
    )
    logging.debug("Initial tray notification shown.")
    print("Initial notification shown.")

    # Force the main window to appear at startup for debugging
    tray_icon.show_projects()

    logging.debug("Entering application event loop.")
    print("Entering Qt event loop now. If no UI is visible, check the system tray overflow or errors in the terminal.")
    sys.exit(app.exec_())