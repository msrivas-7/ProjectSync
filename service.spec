# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\service.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src\\\\monitor.py', '.'),
        ('src\\\\data_manager.py', '.'),
        ('src\\\\vcs_manager.py', '.'),
        ('src\\\\launcher.py', '.'),
	('src\\utils.py', '.')
    ],
    hiddenimports=[
        'watchdog',  # Watchdog for file system events
    	'watchdog.observers',
	'watchdog.events',
        'git',       # GitPython module
        'gitdb',     # GitPython dependency
        'smmap',     # Another GitPython dependency
        'pefile',    # PE File parsing library
        'pywin32',   # Windows-specific extensions
        'pywin32-ctypes',  # Pywin32 ctypes for Windows
        'packaging',  # Packaging module for versioning etc.
        'win32timezone',  # Hidden import for win32timezone
        'win32serviceutil',  # Hidden import for win32serviceutil
        'win32service',  # Hidden import for win32service
        'win32event',  # Hidden import for win32event
        'servicemanager',  # Hidden import for servicemanager
        'monitor',  # Hidden import for monitor
        'data_manager',  # Hidden import for data_manager
        'vcs_manager',  # Hidden import for vcs_manager
        'launcher',  # Hidden import for launcher
        'utils',
    	'dotenv',
	'filelock',
    ],  # Add any missing or hidden imports here    
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='service',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='.',
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
