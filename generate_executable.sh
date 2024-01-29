#! /bin/sh
pyinstaller --noconfirm --onefile --windowed --add-data "$(pwd)/scenes:scenes/" --add-data "$(pwd)/data:data/"  "$(pwd)/main.py"
