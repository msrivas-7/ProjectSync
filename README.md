
  
# ProjectSync

  

ProjectSync is a Windows service and GUI application that automates the management of projects, particularly Unity projects, by cloning repositories, opening projects, and monitoring changes.
  

## Features

  

-  **Automated Cloning**: Automatically clone projects based on configuration.

-  **Unity Project Management**: Open Unity projects with the specified Unity version.

-  **IDE Support**: Open non-Unity projects with available IDEs (VSCode, Visual Studio).

-  **System Tray Application**: GUI application with a system tray icon for easy access.

-  **Background Service**: Windows service that runs in the background to perform tasks.

-  **Real-time Monitoring**: Monitors project data for changes and responds accordingly.

  

## Table of Contents

  

- [Installation](#installation)

- [Prerequisites](#prerequisites)

- [Setup](#setup)

- [Running the Application](#running-the-application)

- [Service](#service)

- [GUI Application](#gui-application)

- [Usage](#usage)

- [System Tray Icon](#system-tray-icon)

- [GUI Window](#gui-window)

- [Automatic Actions](#automatic-actions)

- [Troubleshooting](#troubleshooting)

- [Notes](#notes)

- [File Locking](#file-locking)

- [Logging](#logging)

- [Unity Versions](#unity-versions)

- [Future Enhancements](#future-enhancements)

  

## Installation

  

### Prerequisites

  

-  **Operating System**: Windows 10 or later.

-  **Python 3.x**: Ensure Python is installed and added to your PATH.

-  **Git**: Installed and configured.

-  **Unity Editors**: Install the Unity versions specified in your projects.

-  **IDEs**: (Optional) Install Visual Studio Code or Visual Studio for non-Unity projects.

  

### Setup

  

1.  **Clone the repository or copy the project files to your Windows machine.**

  

```cmd

git clone https://github.com/msrivas-7/ProjectSync.git

```

  

2.  **Navigate to the project directory in Command Prompt or PowerShell.**

  

```cmd

cd ProjectSync

```

  

3.  **Create and activate a virtual environment.**

  

```cmd

python -m venv venv

venv\Scripts\activate

```

  

4.  **Install the required dependencies.**

  

```cmd

pip install -r requirements.txt

```

  

5.  **Update the .env file.**

- Edit `config\.env` with the appropriate values for your system.

- Ensure all paths match the installation directories on your machine.

  

6.  **Ensure that the Unity versions specified in `projects.json` are installed.**

  

7.  **Adjust paths in `projects.json` and `.env` if necessary.**

  

## Running the Application

  

### Service

  

1.  **Build the service executable using PyInstaller.**

  

```cmd

pyinstaller --onefile --hidden-import win32timezone --runtime-tmpdir=. src\service.py

```

  

2.  **Navigate to the `dist` directory.**

  

```cmd

cd dist

```

  

3.  **Install the service.**

  

```cmd

service.exe install

```

  

4.  **Set the service to start automatically.**

  

```cmd

service.exe --startup auto install

```

  

5.  **Start the service.**

  

```cmd

service.exe start

```

  

6.  **Verify the service is running.**

- Open the Services management console (`services.msc`).

- Look for **Project Manager Service** and ensure it’s running.

  

### GUI Application

  

1.  **Build the GUI executable using PyInstaller.**

  

```cmd

pyinstaller --onefile --icon=assets/icon.ico src\main.py

```

  

2.  **Create a shortcut for the GUI executable (`main.exe`).**

- Navigate to the `dist` folder.

- Right-click on `main.exe` and select **Create shortcut**.

  

3.  **Add the shortcut to the Startup folder.**

- Press `Win + R`, type `shell:startup`, and press **Enter**.

- Copy the shortcut into the Startup folder.

  

4.  **Restart your computer or log out and back in to ensure the GUI starts automatically.**

  

## Usage

  

### System Tray Icon

  

-  **Accessing the GUI**: The application runs in the system tray. Left-click the tray icon to open the main GUI window.

-  **Context Menu**: Right-click the tray icon to access options like **Show Projects** and **Exit**.

-  **Visibility**: If the tray icon is not visible, check the hidden icons or adjust taskbar settings to always display it.

  

### GUI Window

  

-  **Project List**: View all projects and their statuses.

-  **Clone Projects**: Click the **Clone** button to clone a project.

-  **Open Projects**: Click the **Open** button to open a project in Unity or an IDE.

-  **Status Indicators**: Projects display statuses like `not_cloned`, `cloned`, or `open`.

  

### Automatic Actions

  

-  **Service Monitoring**: The service monitors `projects.json` for changes.

-  **Auto Cloning**: Projects with `"auto_clone": true` will be cloned automatically by the service.

-  **Auto Opening**: Projects with `"status": "open"` will be opened automatically by the service.


## Troubleshooting
  

-  **Service Issues**:

- Check `logs/service.log` for errors.

- Ensure the service is running in the Services management console.

  

-  **GUI Issues**:

- If the tray icon is not visible, check hidden icons or taskbar settings.

- Ensure the GUI application is running by checking the Task Manager.

  

-  **Project Cloning Issues**:

- Verify Git credentials in the `.env` file.

- Ensure network connectivity and access to the repositories.

  

-  **Unity Project Issues**:

- Verify that the specified Unity version is installed.

- Check the Unity editor paths in the `.env` file.

  

## Notes

  

### File Locking

  

-  **Concurrency Management**: The application uses file locking to prevent simultaneous access to `projects.json` by the service and GUI.

-  **Implementation**: Utilizes the `filelock` library to manage file locks.

  

### Logging

  

-  **Service Logs**: Located at `logs/service.log`.

-  **GUI Logs**: Located at `logs/app.log`.

-  **Logging Levels**: Adjust logging levels in the code if necessary.

  

### Unity Versions

  

-  **Version Specification**: Unity versions are specified per project in `projects.json`.

-  **Executable Path**: The application constructs the Unity executable path based on `UNITY_EDITORS_PATH` and `unity_version`.

-  **Installation**: Ensure all required Unity versions are installed via Unity Hub.

  

## Future Enhancements

  

-  **Airtable Integration**: Replace local `projects.json` with Airtable for remote data management.

-  **Plastic SCM Support**: Extend functionality to handle projects from Plastic SCM.

-  **User Notifications**: Implement system notifications for actions like cloning completion.

-  **Settings Menu**: Add a GUI section for adjusting settings and preferences.

-  **Error Handling**: Improve exception handling and user feedback.