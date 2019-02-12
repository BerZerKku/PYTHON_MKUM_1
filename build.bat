pyrcc4 -o resources_rc.py resources.qrc
pyinstaller --onefile --windowed mkum.py
rmdir /s /q .\build
copy /Y MkUM.dat .\dist