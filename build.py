import PyInstaller.__main__

exclude_args = []

for module in [
    "PySide6.QtQuick",
    "PySide6.QtPdf",
    "PySide6.QtQml",
    "PySide6.QtDBus",
    "PySide6.QtNetwork",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DAnimation",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineQuick",
    "PySide6.QtWebEngineWidgets",
]:
    exclude_args.extend(["--exclude", module])

PyInstaller.__main__.run(
    [
        "src/tomatoclock/__main__.py",
        "--noconfirm",
        "--windowed",
        "--name=TomatoClock",
        "--noconsole",
        "--optimize=2",
        "--collect-data=tomatoclock",
        "--icon=./src/tomatoclock/tomato.ico",
    ]
    + exclude_args
)
