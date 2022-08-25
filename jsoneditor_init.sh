#!/bin/bash

sudo cp JSONEditor /opt/JSONEditor -r

touch /home/$USER/Desktop/JSONEditor.desktop

echo "[Desktop Entry]
Name=JSONEditor
Name[ru]=JSONEditor
Type=Application
Exec=sudo /usr/bin/python3 /opt/JSONEditor/jsoneditor.py
Icon=/opt/JSONEditor/utils/images/ui/main_window.png
Terminal=false
Encoding=UTF-8
" >| /home/$USER/Desktop/JSONEditor.desktop

sudo chmod +x /opt/JSONEditor/jsoneditor.py 
