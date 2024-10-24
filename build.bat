@echo off

if "%1" == "cli" (
    pyinstaller --name="tkforge-cli" --onefile --strip --paths=env/Lib/site-packages tkforge.py --icon=assets/icon.png
) else (
    pyinstaller --name="TkForge" --onefile --strip --paths=env/Lib/site-packages --add-data="assets;assets" gui.py --noconsole --icon=assets/icon.png
)
